"""ML package for Image-Based Crop Disease & Pest Infestation Early Identification.

STATUS: FOUNDATION ONLY.

No model in this package has been trained, and no module produces a prediction.
The modules below are intentional stubs that raise ``NotImplementedError``.

Design document:  ml/README.md
Dataset rules:   ml/data/README.md

Stage note
----------
Stage/severity prediction is only legitimate if the training data contains real
stage labels. See ml/data/README.md section 4 before implementing any stage
head.
"""

__version__ = "0.1.0"

__all__ = [
    "preprocessing",
    "dataset",
    "train",
    "evaluate",
    "predict",
]
