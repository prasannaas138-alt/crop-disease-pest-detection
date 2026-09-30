"""Dataset and DataLoader construction.

STATUS: STUB — NOT IMPLEMENTED.

Pipeline steps 3 (label analysis) and 4 (train/val/test split).
Nothing here reads from disk, because no dataset has been downloaded yet.

Design notes
------------
Leakage is the main correctness risk in this project. Leaf datasets commonly
contain near-duplicate images of the *same individual leaf*; a naive random
split inflates accuracy and produces a model that fails on real input. The
planned split is therefore:

  1. group by plant/leaf instance ID when the dataset provides one,
  2. otherwise group perceptual-hash near-duplicates together,
  3. stratify by class,
  4. fix a random seed and persist the split to CSV for reproducibility.

Class imbalance is expected in plant datasets. Planned handling: class-weighted
loss and/or a balanced sampler — chosen only after seeing the real distribution.

Planned label spaces (see ml/README.md section 4):
  A. crop
  B. condition  (healthy / disease / pest)
  C. disease or pest
  D. stage or severity  — ONLY if genuinely labelled, otherwise omitted

To be implemented in a later task, after the dataset is available.
"""

from __future__ import annotations

IMPLEMENTED = False


def discover_classes(root: str) -> list[str]:
    """Scan a folder-per-class dataset layout and return the sorted class names.

    Not implemented. Planned behaviour: discover ``root/<class_name>/*.jpg``
    and return the sorted list of class names. The ordering must be persisted
    to ``classes.json`` so inference uses the identical index mapping.
    """
    raise NotImplementedError(
        "discover_classes() is not implemented yet. This requires a dataset. "
        "See ml/data/README.md section 7 for what we need from the team."
    )


def build_label_map(classes: list[str]) -> dict[str, int]:
    """Build the ``class name -> index`` mapping.

    Not implemented. This mapping is the contract between training and
    inference; it must be saved and reloaded, never re-derived by chance.
    """
    raise NotImplementedError(
        "build_label_map() is not implemented yet. See ml/README.md section 5 "
        "(step 4)."
    )


def build_splits(root: str, val_ratio: float = 0.2, test_ratio: float = 0.1, seed: int = 42):
    """Create a grouped, stratified train/val/test split and save it to CSV.

    Not implemented. Must record whether the split was grouped or random, since
    that materially changes how the resulting metrics should be interpreted.
    """
    raise NotImplementedError(
        "build_splits() is not implemented yet. Leakage-safe splitting is a "
        "correctness requirement — see ml/data/README.md section 5."
    )


def analyse_labels(root: str) -> "object":
    """Produce a class-distribution and imbalance report.

    Not implemented. Returns per-class counts, a crop x disease matrix, and
    flags for long-tail classes and any class with too few samples.
    """
    raise NotImplementedError(
        "analyse_labels() is not implemented yet. See ml/README.md section 5 "
        "(step 3)."
    )


def build_dataloaders(batch_size: int = 32, num_workers: int = 0):
    """Return ``(train_loader, val_loader, test_loader)`` for PyTorch training.

    Not implemented. Requires the splits to exist first.
    """
    raise NotImplementedError(
        "build_dataloaders() is not implemented yet. Depends on build_splits() "
        "and on the preprocessing transforms."
    )
