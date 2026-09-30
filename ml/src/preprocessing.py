"""Image preprocessing for the crop disease / pest model.

STATUS: STUB — NOT IMPLEMENTED.

Pipeline step 5 (image preprocessing) and step 6 (data augmentation).
This module defines the API contract only. Every function raises
``NotImplementedError`` so that nothing can silently return a fake result.

Design notes
------------
Preprocessing must be *deterministic and identical* at train time and at
inference time. The transform used in ``ml/src/predict.py`` must be the exact
transform that ``ml/src/train.py`` trained with, otherwise predictions are
meaningless. It is therefore configured from a single saved config file
(``preprocess_config``) rather than written twice.

Planned responsibilities
------------------------
- Load an image from disk and decode to RGB
- Reject/flag unreadable and corrupt images
- Resize to the backbone's expected input resolution
- Normalise with the backbone's ImageNet mean/std
- Optional: background/leaf segmentation to reduce domain gap
- Provide a train-time augmentation pipeline and an eval-time transform

Backbone input resolution (to confirm after dataset inspection):
  MobileNetV3-Large  -> 224 x 224
  EfficientNet-B0    -> 224 x 224

To be implemented in a later task, after the dataset is available.
"""

from __future__ import annotations

# Marker so tests / callers can assert the stub state without importing torch.
IMPLEMENTED = False

# Populated in a later task, once the backbone is chosen.
IMAGE_SIZE: int | None = None
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


def load_image(path: str):
    """Load an image from ``path`` and return it as an RGB array.

    Not implemented. Planned to use Pillow, with an OpenCV fallback, and to
    raise a clear error for corrupt or non-image files.
    """
    raise NotImplementedError(
        "load_image() is not implemented yet. No dataset has been inspected. "
        "See ml/README.md section 5 (step 5) and ml/data/README.md."
    )


def build_train_transform(image_size: int | None = None):
    """Return the augmentation pipeline used during training.

    Not implemented. Planned augmentations: random resized crop, horizontal
    flip, small rotation, colour jitter, and mild blur/noise. Kept
    conservative — heavy augmentation on a small dataset destroys signal.
    """
    raise NotImplementedError(
        "build_train_transform() is not implemented yet. Augmentation strategy "
        "depends on the chosen dataset. See ml/README.md section 5 (step 6)."
    )


def build_eval_transform(image_size: int | None = None):
    """Return the deterministic transform used at validation/inference time.

    Not implemented. Must stay byte-identical to the training-time eval path.
    """
    raise NotImplementedError(
        "build_eval_transform() is not implemented yet. See ml/README.md "
        "section 5 (step 5)."
    )


def load_preprocess_config(config_path: str) -> dict:
    """Load the shared preprocessing config saved alongside the model weights.

    Not implemented. This is how train-time and inference-time preprocessing are
    kept in sync.
    """
    raise NotImplementedError(
        "load_preprocess_config() is not implemented yet. Config is written at "
        "training time (step 14) and read at inference time (step 15)."
    )
