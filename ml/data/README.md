# Dataset Requirements

> **No dataset has been downloaded or created yet.** `raw/` and `processed/` are empty.
> No fake or synthetic training images have been generated, and none will be.

---

## 1. What a useful dataset must contain

| Field | Required? | Why it matters |
|-------|-----------|----------------|
| **Image** | ✅ Required | The model's only input. RGB, real photographs. |
| **Crop** | ✅ Required | Output A. Tells us which plant it is. |
| **Disease / pest class** | ✅ Required | Output C. The actual target. |
| **Healthy class** | ✅ Strongly preferred | Output B. Without healthy images the model cannot say "healthy" — a screening tool that never reports "fine" is useless. |
| **Stage / severity** | ⬜ Optional | Output D. **Only if genuinely labelled.** See §4. |
| **Pest vs disease flag** | ⬜ Optional | Output B needs to separate the two. Often inferable from class names. |
| **Location** | ⬜ Optional | Context; can cause spurious shortcut learning if leaked across the split. |
| **Crop growth stage** | ⬜ Optional | Context for recommendations. |
| **Environment / context** | ⬜ Optional | e.g. field vs greenhouse, lighting, camera. Useful for robustness analysis. |
| **Plant / leaf instance ID** | ⬜ Highly recommended | Enables a **grouped split** that prevents train/test leakage (§5). |

### Minimum viable dataset for a first demo
- 2–4 crops
- ~5–12 total disease/pest classes **including healthy**
- A few hundred images per class at minimum (a few thousand total is a better target)
- Consistent image quality and roughly consistent lighting

That is enough for a credible transfer-learning demo. It is **not** enough for clinical
grade accuracy, and we will not claim otherwise.

---

## 2. Hard rules

1. **We do not invent labels.** If a field is absent from the dataset, the model does not
   predict it. We will not derive labels by guessing, by filename heuristics that encode
   our assumptions, or by a human "eyeballing" images and assigning stages.
2. **We do not generate fake training images.** No synthetic disease textures, no
   procedurally drawn leaves, no augmentations saved to disk as if they were data.
   (Augmentations *during training* are fine — see §6. That is different from fabricating
   the dataset.)
3. **We do not download large datasets automatically.** Dataset choice and download are
   approved team decisions, recorded here with source, size, license and citation.
4. **Licence and citation are recorded** before use. A dataset with unclear terms cannot
   go in a public repo or a demo.
5. **Datasets are never committed to Git.** Only the small manifest/label files are tracked
   (see root `.gitignore`).

---

## 3. Candidate datasets to evaluate

To be assessed in the next step — **not yet downloaded, not yet chosen**:

| Dataset | Shape | Strengths | Concerns |
|---------|-------|-----------|----------|
| **PlantVillage** | folder-per-class, ~54k images, 38 classes, 14 crops | Clean, large, well-labelled; the standard baseline | **Lab-style isolated leaves on plain backgrounds** — poor match to real field phone photos. No stage/severity labels. |
| **PlantDoc** | ~2.6k real-field images, 13 crops | Real field conditions, multiple objects per image | Small; multi-label per image |
| **IP102** | ~75k pest images, 102 pest classes w/ crops | Genuine **pest** coverage, large | Small images; pest species may be too fine-grained for our scope |
| Datasets with **severity** gradings | class-per-severity | Would enable output D | Often single crop, small, and "severity" may be subjective |

**Open question for the team:** is the demo's input a *clean isolated leaf photo* or a
*real field phone photo*? This pushes the dataset choice in different directions and is
worth deciding early.

---

## 4. ⚠️ The stage / severity rule — most important section in this file

**We must not invent stage/severity labels. Ever.**

Worked example:

> Suppose the dataset contains only:
>
> ```
> Tomato → Early Blight
> ```
>
> The model **can** learn: *this image is Early Blight.* ✅
>
> The model **cannot** legitimately learn:
>
> ```
> Early Blight → Stage 1 / Stage 2 / Stage 3
> ```
>
> ...because no training image says which stage it was. Any stage we emit would be
> **invented**. Stage 1 and Stage 2 look similar; the difference is mostly *time since
> infection* and *lesion density* — and if we guess, we are presenting a fabricated
> agronomic claim to a farmer with a genuine risk of wrong advice.

Consequences we accept:

- If the dataset has no stage labels, **output D is dropped** and the system reports
  crop, condition, disease/pest, and confidence — and says so plainly in the UI.
- The README and the API response will carry an explicit
  `"stage_supported": false` field rather than silently omitting it.
- If stage labels *are* available, we still verify they are consistent and
  agronomically meaningful before training on them.

**"More spots = more severe" is an assumption, not a label.** We do not ship it as fact.

---

## 5. Split strategy (dataset integrity)

Many leaf datasets contain near-duplicate photos of the *same individual leaf*. A naive
random split places siblings in both train and test and yields a **badly inflated**
accuracy that collapses on real inputs.

Once we have a dataset we will:
- prefer a **grouped split** keyed on plant/leaf instance ID when available,
- otherwise detect near-duplicates (e.g. perceptual hashing) and group them,
- stratify by class and fix a random seed,
- save the split to a CSV so the run is reproducible,
- and **record in the README which split produced which number.**

---

## 6. Directory layout

```
data/
├── raw/          # downloaded / collected originals  (git-ignored, EMPTY)
├── processed/    # generated splits, resized copies   (git-ignored, EMPTY)
├── labels.csv    # small manifest — TRACKED in git
├── classes.json  # label -> index map                 — TRACKED in git
└── splits/       # train/val/test CSVs               — TRACKED in git
```

The rule: **track the metadata, ignore the megabytes.** The team needs the label map
and split files to reproduce a run; nobody needs the image blobs in GitHub.

---

## 7. What we need from the team

1. **Dataset name + download source/link**, or approval to pick one from §3.
2. **Confirmation of the demo input type** (isolated leaf photo vs real field photo).
3. **Crops in scope** — our current proposal: 2–4 (e.g. tomato, rice, corn, potato).
4. **Whether "pest" is required for the demo**, or disease-only is acceptable.
5. **Any severity/stage data** the team already has or can obtain.
6. **Licence confirmation** for whatever we use.

Once we have the dataset, the next step is **inspection only** — count the classes, count
the images, report the imbalance — before any architecture decision.

