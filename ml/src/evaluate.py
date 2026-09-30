"""Model evaluation and metrics reporting.

STATUS: STUB — NOT IMPLEMENTED. NO METRICS HAVE BEEN COMPUTED.

Pipeline steps 9-13: validation, evaluation, confusion matrix, per-class
precision/recall/F1, and the final test-set run.

There are no accuracy, precision, recall, F1, or mAP numbers anywhere in this
project yet. Any such number appearing before a real training run would be
fabricated, so none has been written down.

Planned reporting
-----------------
- Top-1 accuracy, plus top-3 accuracy once class count justifies it
- Macro-averaged precision / recall / F1 (macro, not weighted — weighted
  accuracy can hide a model that has completely failed on rare classes)
- Per-class precision/recall/F1/support, saved as CSV
- Confusion matrix, saved as PNG and CSV
- Learning curves from the training history
- Confidence calibration, to decide the low-confidence abstain threshold

Why macro-average matters here
------------------------------
Plant disease datasets are long-tailed: a few common diseases, many rare ones.
A model that ignores the rare classes can still show a high weighted average.
For a farmer-facing screening tool, missing a disease is the costly error, so
recall on rare classes is reported explicitly rather than averaged away.

The final test-set evaluation (step 13) is run exactly once, after the
architecture and hyperparameters are frozen, to avoid test-set overfitting.

To be implemented in a later task, after a model has actually been trained.
"""

from __future__ import annotations

IMPLEMENTED = False


def evaluate_split(model, dataloader, device: str = "cpu") -> dict:
    """Compute loss and classification metrics over one data split.

    Not implemented. ``model`` must be a real trained model; there is no
    untrained fallback that returns plausible-looking numbers.
    """
    raise NotImplementedError(
        "evaluate_split() is not implemented yet. It requires a trained model — "
        "none exists. See ml/README.md section 5 (steps 9-10)."
    )


def confusion_matrix_report(model, dataloader, class_names: list[str]) -> dict:
    """Return the confusion matrix and save it to ``ml/outputs/``.

    Not implemented. Planned output: PNG figure plus CSV matrix.
    """
    raise NotImplementedError(
        "confusion_matrix_report() is not implemented yet. See ml/README.md "
        "section 5 (step 11)."
    )


def per_class_report(model, dataloader, class_names: list[str]) -> dict:
    """Return per-class precision/recall/F1/support and save to CSV/JSON.

    Not implemented. See ml/README.md section 5 (step 12).
    """
    raise NotImplementedError(
        "per_class_report() is not implemented yet. See ml/README.md section 5 "
        "(step 12)."
    )


def final_test_evaluation(model_path: str, test_split_csv: str) -> dict:
    """Single authoritative evaluation on the untouched test split.

    Not implemented. Must be run exactly once, after freezing the model.
    """
    raise NotImplementedError(
        "final_test_evaluation() is not implemented yet. See ml/README.md "
        "section 5 (step 13)."
    )


def main() -> None:
    """CLI entry point: ``python -m src.evaluate --weights ml/models/<name>.pt``

    Not implemented.
    """
    raise NotImplementedError(
        "Evaluation is not implemented yet because no model has been trained."
    )


if __name__ == "__main__":  # pragma: no cover
    main()
