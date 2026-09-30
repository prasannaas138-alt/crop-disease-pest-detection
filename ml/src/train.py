"""Model training entry point.

STATUS: STUB — NOT IMPLEMENTED. NO MODEL HAS BEEN TRAINED.

Pipeline steps 7 (transfer learning) and 8 (model training).

This module deliberately contains no network definition, no optimiser, no
training loop, and no default hyperparameters that could be mistaken for a
working trainer. Running it will raise ``NotImplementedError``.

Nothing in this repository may be read as "the model works". No weights exist
in ``ml/models/`` and no accuracy number has been measured.

Planned approach
----------------
Transfer learning with a lightweight ImageNet-pretrained backbone, because
this must run in real time on CPU for the hackathon demo:

    MobileNetV3-Large   ~5M params   fastest, best for a constrained demo
    EfficientNet-B0     ~5M params   better accuracy per FLOP, still light

Training from scratch is NOT an option for this project: plant datasets are far
too small and it would not converge in hackathon time.

Two-stage schedule (standard practice):
    1. Freeze the backbone, train only the new classification head.
       Fast, stable, and already usually a strong baseline.
    2. Unfreeze the last few backbone blocks and fine-tune at a much lower
       learning rate. Improves accuracy, risks overfitting on a small dataset,
       so it is validated rather than assumed.

Also planned: early stopping on validation loss, a learning-rate schedule, and
class weighting to handle imbalance.

Hyperparameters are NOT hardcoded here. They will live in a config file that is
committed, so a run is reproducible.

To be implemented in a later task, after the dataset is inspected and the
architecture decision (Option A / B / C) is made.
"""

from __future__ import annotations

IMPLEMENTED = False

# Placeholder documentation of the planned backbones. These are strings, not
# loaded models — importing this module downloads nothing.
CANDIDATE_BACKBONES = (
    "mobilenet_v3_large",  # torch.hub / torchvision
    "efficientnet_b0",     # via timm
)


def build_model(backbone: str = "mobilenet_v3_large", num_classes: int = 0, pretrained: bool = True):
    """Construct the classification network with a randomly-initialised head.

    Not implemented. ``num_classes`` must come from the real dataset — it is
    never a default guess.

    For Option B (multi-head), this will return a shared backbone with separate
    heads for crop, condition, disease/pest, and optionally stage.
    """
    raise NotImplementedError(
        "build_model() is not implemented yet. The architecture decision "
        "(Option A/B/C) is pending dataset inspection — see ml/README.md "
        "section 4 and the decision log in section 9."
    )


def train(config_path: str):
    """Run the full training loop and write weights to ``ml/models/``.

    Not implemented. Will write: best checkpoint, training history CSV,
    learning curves, and the preprocessing config.
    """
    raise NotImplementedError(
        "train() is not implemented yet. No model has been trained. See "
        "ml/README.md section 5 (steps 7-8)."
    )


def main() -> None:
    """CLI entry point: ``python -m src.train --config ml/configs/<name>.yaml``.

    Not implemented.
    """
    raise NotImplementedError(
        "Training is not implemented yet and must not be run until the dataset "
        "is inspected and the team has approved the architecture."
    )


if __name__ == "__main__":  # pragma: no cover
    main()
