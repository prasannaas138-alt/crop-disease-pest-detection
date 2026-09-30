# ML — Image-Based Crop Disease & Pest Infestation Early Identification

> **Project status: FOUNDATION ONLY.**
> At the time of writing this file, **no model has been trained, no dataset has been
> downloaded, and no evaluation metrics exist.** Every accuracy/F1 number in this
> project must come from a real training run on a real dataset. Nothing here is a
> placeholder result, an estimate, or a guess.

> **Disclaimer:** This is an AI-assisted **early screening prototype**, not a certified
> agricultural diagnosis system. It exists to demonstrate a technical idea during a
> hackathon. It must never be presented as a guaranteed or authoritative diagnosis,
> and agronomist/extension-officer review remains the only valid confirmation.

---

## 1. What this project is

A user uploads (or captures) a photo of a crop leaf / plant. The system returns:

- the **crop** it most likely is,
- whether it is **healthy**, **diseased**, or **pest-infested**,
- the **specific disease or pest**,
- the **stage / severity**, *if and only if* the dataset genuinely supports it,
- a **confidence score** and a plain-language **risk + recommendation**.

### Target end-to-end flow

```
Input Image
    ↓
Image Preprocessing
    ↓
ML Model
    ↓
Crop Identification
    ↓
Disease / Pest Identification
    ↓
Stage / Severity Identification
    ↓
Confidence Score
    ↓
Risk Assessment
    ↓
Recommendation
```

**The model is the core of this project.** The rest of the system is delivery.

---

## 2. The five things the model is expected to predict

| # | Output | Task type (expected) | Status |
|---|--------|----------------------|--------|
| A | **Crop** — rice, tomato, maize, … | Single- or multi-label classification | Not implemented |
| B | **Condition** — Healthy / Disease / Pest | Multi-class classification | Not implemented |
| C | **Disease/Pest** — e.g. Early Blight, Leaf Miner | Multi-class (or multi-label) classification | Not implemented |
| D | **Stage / Severity** — e.g. Stage 1/2/3, Mild/Moderate/Severe | Classification, *dataset-dependent* | Not implemented |
| E | **Confidence** | Softmax probability from the classifier | Not implemented |

> ⚠️ **D is conditional.** We will only train a stage/severity head if the dataset
> actually contains trustworthy stage labels. See `ml/data/README.md` §4.

---

## 3. Understanding the task types (these are NOT interchangeable)

Getting this terminology right is essential, because it directly constrains the
architecture we can build.

### 3.1 Binary classification
One decision: *is this leaf healthy or not?*
Example: `healthy` vs `diseased`.
Output: 2 probabilities.

### 3.2 Multi-class classification (mutually exclusive)
The image belongs to **exactly one** bucket, and the buckets are exclusive.
Example: `Tomato_Early_Blight` | `Tomato_Late_Blight` | `Tomato_Healthy` | `Rice_Leaf_Blast` | ...

This is the **most likely** shape of our first model, because a standard
folder-per-class dataset (e.g. `PlantVillage`) is naturally multi-class.

- Loss: `CrossEntropyLoss`
- Output layer: `Linear(features, num_classes)`
- Gives a valid probability distribution → confidence is free.

### 3.3 Multi-label classification (non-exclusive)
An image can belong to **several buckets at once**, and buckets can co-occur.
Example: a leaf that is *both* `yellowing` and *has fungal spots`; or a field image
containing corn **and** a weed species.

- Loss: `BCEWithLogitsLoss`
- Output layer: `Linear(features, num_classes)` + independent sigmoid per class
- Confidence must be decided per-label, not from a normalized softmax.

> If our dataset turns out to be multi-label, Option A below is still viable but the
> loss/head changes. This is why we inspect the data first.

### 3.4 Object detection
The model outputs **bounding boxes** around individual instances, e.g. every visible
insect, every individual leaf, every lesion.
- Architectures: YOLO (v8/v11), Faster R-CNN, RetinaNet, DETR.
- Loss: detection loss (e.g. YOLO's box + objectness + class loss).
- Metrics: **mAP@0.5**, not accuracy.

> Only needed for Option C, and only if the goal is *"count and localise the pests"*
> rather than *"classify this plant's health"*. Detection is significantly heavier to
> train and to run — a real cost for a hackathon demo.

### 3.5 Stage / severity prediction
A **conditional** classification layer that refines a disease/pest prediction:

- if disease = `Early Blight` → predict `Stage 1 | Stage 2 | Stage 3`
- or if the dataset uses `Mild | Moderate | Severe`

**Critical:** this is a separate label space. It is *only* valid if the data has real
stage labels. We cannot derive "Stage 2" from "this image has many spots" using a
model — that would be fabricating supervision. See `ml/data/README.md` §4.

### 3.6 Confidence is not a separate model
Confidence comes from the classifier's output probability (softmax max-prob for
multi-class; max sigmoid score for multi-label). We will additionally report a
**calibration measure** and a **low-confidence / abstain band** so the UI can honestly
say *"I'm not sure — retake the photo in better light"*, which is more useful and
more honest than always returning a confident wrong answer.

---

## 4. Architecture options — **DECISION NOT YET MADE**

The dataset decides this. We are deliberately not choosing yet.

### Option A — One multi-class image classification model
A single network, single `CrossEntropyLoss`, one label set combining crop + disease.

```
image → backbone → (crop, condition, disease) single softmax
```

**Pros:** simplest, cheapest to train and serve, easiest to explain, one model to ship.
**Cons:** cannot express a true hierarchy, cannot output severity, and adding a crop
forces retraining.

> Typical of `PlantVillage`-style folder-per-class datasets.

### Option B — Separate models / heads for crop, disease/pest, and severity
One shared backbone with three heads, or three independent models.

```
image → shared backbone (EfficientNet / MobileNet)
          ├─ head 1: crop          (softmax)
          ├─ head 2: condition     (softmax)
          ├─ head 3: disease/pest  (softmax)
          └─ head 4: stage         (softmax, ONLY if labels exist)
```

**Pros:** matches the actual output hierarchy A–E, lets each head be trained/validated
independently, lets us drop the stage head entirely if labels are missing.
**Cons:** needs labels for every head; more validation surface; more work to serve.

> This is our current **leading candidate** because it maps 1:1 onto the five required
> outputs — but it is not confirmed.

### Option C — Object detection for visible pests + classification for disease
```
image → YOLO detector ──→ pest species, count, bounding boxes, per-box confidence
image → classifier     ──→ crop, disease, condition, severity
```

**Pros:** the only option that can *count* pests and show the farmer *where* on the
leaf the problem is — a genuinely strong demo and real agronomic value.
**Cons:** needs a detection dataset (bounding boxes); heavier training and inference;
harder to keep lightweight for the hackathon.

> Worth considering **only** if a suitable annotated detection dataset is available.

### How the decision will be made
After step 2–3 of the pipeline in §5, we will write down, per dataset candidate:
- Are disease classes mutually exclusive? → A or B (not multi-label)
- Are stages/severities labelled? → include or omit the stage head
- Are pests annotated with boxes? → consider C
- How many crops × how many classes? → the hackathon-scope constraint in §7

The decision will be recorded in this file under a "Decision log" section, with the
dataset name as justification. It will not be made by guesswork.

---

## 5. Planned pipeline (documented now, **not** implemented yet)

None of these steps have been implemented. They are the build order for the next tasks.

| # | Step | Deliverable | Status |
|---|------|-------------|--------|
| 1 | **Dataset collection** | Candidate datasets listed, source + license + citation recorded | ⬜ |
| 2 | **Dataset inspection** | `inspect_dataset.py` → counts, image sizes, corrupt files, format | ⬜ |
| 3 | **Label analysis** | Class distribution, per-crop disease matrix, long-tail & imbalance report | ⬜ |
| 4 | **Train/val/test split** | Stratified, grouped (see below), fixed seed, saved to CSV | ⬜ |
| 5 | **Image preprocessing** | Resize, normalize, RGB conversion, leaf/background handling | ⬜ |
| 6 | **Data augmentation** | Flips, rotations, colour jitter, (light) blur/noise | ⬜ |
| 7 | **Transfer learning** | Load ImageNet-pretrained lightweight backbone, freeze → unfreeze | ⬜ |
| 8 | **Model training** | Training loop, early stopping, LR schedule, class weighting | ⬜ |
| 9 | **Validation** | Per-epoch val loss/accuracy, learning curves | ⬜ |
| 10 | **Evaluation** | Accuracy, macro/weighted precision, recall, F1 | ⬜ |
| 11 | **Confusion matrix** | Saved as PNG + CSV, per class | ⬜ |
| 12 | **Per-class precision/recall/F1** | `classification_report` saved to CSV/JSON | ⬜ |
| 13 | **Test-set evaluation** | Single final run on untouched test split | ⬜ |
| 14 | **Save trained model** | Weights + `classes.json` label map + preprocessing config | ⬜ |
| 15 | **Build inference/prediction function** | `predict.py`: image path → full A–E JSON result | ⬜ |
| 16 | **Connect model to backend** | FastAPI endpoint wrapping the inference function | ⬜ |

### Step 4 detail — leakage is the #1 way this project would silently fail
PlantVillage and similar datasets often contain **near-duplicate images of the same
individual leaf**. A naive random split puts sibling images in both train and test and
produces an inflated, meaningless score.

We will therefore use a **grouped split keyed on plant/leaf identity** where the dataset
exposes that identity, stratified by class, and we will record in the README whether the
reported numbers are grouped-split or random-split. This is a correctness requirement,
not a nicety.

---

## 6. Folder structure

```
ml/
├── README.md              ← you are here (design doc + decision log)
├── requirements.txt       ← pinned Python deps
├── data/
│   ├── README.md          ← dataset requirements & rules
│   ├── raw/               ← downloaded/collected data (git-ignored, empty)
│   └── processed/         ← generated splits/arrays (git-ignored, empty)
├── notebooks/             ← EDA notebooks (empty)
├── src/
│   ├── __init__.py
│   ├── preprocessing.py   ← STUB (NotImplementedError)
│   ├── dataset.py         ← STUB
│   ├── train.py           ← STUB
│   ├── evaluate.py        ← STUB
│   └── predict.py         ← STUB
├── models/                ← trained weights (git-ignored, empty)
└── outputs/               ← metrics, plots, logs (git-ignored, empty)
```

> **Every file in `src/` is currently a stub that raises `NotImplementedError`.**
> They exist to fix the module layout and API contract. None of them contains a model,
> a default prediction, or a hardcoded result. This is deliberate.

### Verifying the foundation

```bash
python ml/verify_foundation.py
```

This checks that the folder structure is intact and — importantly — that **every
stubbed function still raises** instead of returning a placeholder value. It is a
guard against someone "fixing" a stub by hardcoding an answer. It does **not**
test any model, because no model exists yet.

---

## 7. Hackathon constraints (agreed scope rules)

The model must be **demonstrable live**, so:

- ✅ Transfer learning — **never** train a large model from scratch.
- ✅ Lightweight backbone — **MobileNetV3** or **EfficientNet-B0** as the leading
  candidates. Must run on CPU in real time for the demo.
- ✅ A **manageable** number of crops and a **manageable** number of
  disease/pest classes.
- ❌ Do **not** attempt to cover every crop and every disease on the planet.
- ❌ Do **not** add a heavy detector unless a detection dataset is genuinely available.

The exact crop list and class list will be chosen **after dataset inspection** and
recorded in §9.

### Expected input
- Single RGB image, leaf/plant close-up, reasonably lit, one dominant subject.
- A phone photo of a real field is a different distribution from a clean lab dataset
  image. If the demo uses phone photos, we should prefer a dataset that includes
  field/background images, or the demo will be embarrassingly wrong in front of judges.

---

## 8. Dependencies

`ml/requirements.txt` pins one deep-learning framework only: **PyTorch**.

**Why PyTorch over TensorFlow:** lighter install on Windows, better transfer-learning
ergonomics via `torchvision.models` + `timm`, and easier to serve later. Installing both
is explicitly out of scope.

**Environment note:** this machine already has `numpy`, `pandas`, `matplotlib`, `pillow`,
`opencv-contrib-python`, `scikit-learn` and `fastapi` installed. `opencv-contrib-python`
already provides the full `cv2` API, so requirements keep that one rather than also
listing `opencv-python` — installing both causes a broken `cv2`. `torch` and
`torchvision` are **not** installed yet and are **not** installed by this task.

---

## 9. Decision log

*No decisions taken yet — this section is intentionally empty.*

| Date | Decision | Dataset justification | Decided by |
|------|----------|----------------------|------------|
| — | Architecture (A / B / C) | pending dataset inspection | — |
| — | Crops in scope | pending | — |
| — | Disease/pest classes in scope | pending | — |
| — | Stage/severity: include or omit | pending | — |
| — | Split strategy (grouped vs random) | pending | — |

---

## 10. What has NOT been done yet

Being explicit so nobody mistakes scaffolding for progress:

- ❌ No dataset downloaded.
- ❌ No model trained, fine-tuned, or loaded.
- ❌ No model weights exist (`ml/models/` is empty).
- ❌ No accuracy, precision, recall, F1, or confusion matrix computed.
- ❌ No prediction function that returns a real result.
- ❌ No API/frontend/backend integration.
- ❌ No architecture decision made.

---

## 11. Next step (requires team-lead approval)

1. Team provides the dataset (name + source + access), or approves downloading one.
2. Run dataset inspection → produce a real class-count report.
3. Fill in §9 and decide Option A / B / C.
4. Only then start writing `src/` for real.

**Wait for team-lead approval before beginning the next ML step.**


