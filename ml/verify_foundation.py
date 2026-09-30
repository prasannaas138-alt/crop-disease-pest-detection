"""Foundation self-check for the ML project.

Run from the repository root:

    python ml/verify_foundation.py

This is NOT a model test. No model exists yet, so there is nothing to test for
accuracy. This script only verifies the foundation is honest and importable:

  1. every module imports without heavy dependencies installed,
  2. every stubbed function raises NotImplementedError (returns no fake value),
  3. no module claims to be implemented,
  4. the required folder structure exists.

Exit code 0 = foundation is intact. Non-zero = something regressed.
"""

from __future__ import annotations

import sys
from pathlib import Path

ML_DIR = Path(__file__).resolve().parent
REPO_ROOT = ML_DIR.parent

sys.path.insert(0, str(ML_DIR))

EXPECTED_PATHS = [
    "ml/README.md",
    "ml/requirements.txt",
    "ml/data/README.md",
    "ml/data/raw",
    "ml/data/processed",
    "ml/notebooks",
    "ml/src/__init__.py",
    "ml/src/preprocessing.py",
    "ml/src/dataset.py",
    "ml/src/train.py",
    "ml/src/evaluate.py",
    "ml/src/predict.py",
    "ml/models",
    "ml/outputs",
    ".gitignore",
]

STUBBED_CALLS = [
    ("preprocessing", "load_image", ("dummy.jpg",)),
    ("preprocessing", "build_train_transform", ()),
    ("preprocessing", "build_eval_transform", ()),
    ("preprocessing", "load_preprocess_config", ("config.yaml",)),
    ("dataset", "discover_classes", ("data/raw",)),
    ("dataset", "build_label_map", (["a", "b"],)),
    ("dataset", "build_splits", ("data/raw",)),
    ("dataset", "analyse_labels", ("data/raw",)),
    ("dataset", "build_dataloaders", ()),
    ("train", "build_model", ()),
    ("train", "train", ("config.yaml",)),
    ("train", "main", ()),
    ("evaluate", "evaluate_split", (None, None)),
    ("evaluate", "confusion_matrix_report", (None, None, [])),
    ("evaluate", "per_class_report", (None, None, [])),
    ("evaluate", "final_test_evaluation", ("m.pt", "t.csv")),
    ("evaluate", "main", ()),
    ("predict", "load_model", ("m.pt",)),
    ("predict", "predict", ("leaf.jpg", "m.pt")),
    ("predict", "build_recommendation", ("disease", "early_blight")),
    ("predict", "main", ()),
]


def main() -> int:
    import src

    print(f"src package version: {src.__version__}")

    # 1. structure
    print("\n[1] Folder structure")
    missing = [p for p in EXPECTED_PATHS if not (REPO_ROOT / p).exists()]
    for p in EXPECTED_PATHS:
        print(f"    {'OK  ' if (REPO_ROOT / p).exists() else 'MISS'} {p}")

    # 2. modules import + IMPLEMENTED flag
    print("\n[2] Module import and implementation flags")
    from src import dataset, evaluate, predict, preprocessing, train

    modules = [preprocessing, dataset, train, evaluate, predict]
    claimed = [m.__name__ for m in modules if getattr(m, "IMPLEMENTED", False)]

    # 3. stubs must raise, never return a fake value
    print("\n[3] Stub behaviour (all must raise NotImplementedError)")
    leaked = []
    for mod_name, fn_name, args in STUBBED_CALLS:
        module = {
            "preprocessing": preprocessing,
            "dataset": dataset,
            "train": train,
            "evaluate": evaluate,
            "predict": predict,
        }[mod_name]
        try:
            getattr(module, fn_name)(*args)
        except NotImplementedError:
            print(f"    OK   {mod_name}.{fn_name}() raises NotImplementedError")
        except Exception as exc:  # noqa: BLE001
            leaked.append(f"{mod_name}.{fn_name}() raised {type(exc).__name__} instead")
        else:
            leaked.append(f"{mod_name}.{fn_name}() RETURNED A VALUE (fake result!)")

    print("\n" + "=" * 60)
    ok = True
    if missing:
        print(f"FAIL: missing paths -> {missing}")
        ok = False
    if claimed:
        print(f"FAIL: modules claiming IMPLEMENTED while untrained -> {claimed}")
        ok = False
    if leaked:
        for issue in leaked:
            print(f"FAIL: {issue}")
        ok = False
    if ok:
        print("PASS: foundation intact. No model trained, no fake predictions.")
    print("=" * 60)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
