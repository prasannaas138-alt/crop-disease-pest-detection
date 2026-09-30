"""Inference / prediction entry point.

STATUS: STUB — NOT IMPLEMENTED. THIS MODULE CANNOT PREDICT ANYTHING.

Pipeline step 15 (build inference/prediction function), feeding step 16
(backend integration).

Integrity rules enforced by design
----------------------------------
This module will NEVER:
  * return a hardcoded, random, or placeholder prediction,
  * return a fake confidence value,
  * invent a stage or severity label that the model was not trained to predict,
  * silently fall back to a "best guess" when the real model is missing.

If the weights file is absent, it raises. That is the correct behaviour. A demo
that shows invented output is worse than a demo that honestly reports
"model not trained yet".

Planned output shape (once a real model exists)
-----------------------------------------------
A JSON-serialisable dict, one key per required output:

    {
      "crop":          {"name": "...", "confidence": 0.0},
      "condition":     {"name": "healthy | disease | pest", "confidence": 0.0},
      "disease_pest":  {"name": "...", "confidence": 0.0},
      "stage":         {"name": null, "confidence": null,
                        "supported": false},
      "confidence":    0.0,
      "risk_level":    "low | medium | high",
      "recommendation":"...",
      "disclaimer":    "AI-assisted early screening, not a confirmed diagnosis."
    }

The ``stage.supported`` field is the machine-readable form of the rule in
``ml/data/README.md`` section 4: if the dataset has no stage labels, the stage
head is not built and the API says ``supported: false`` instead of inventing a
stage. Risk and recommendation will be derived from the real predicted class
via an explicit, reviewable mapping table — not guessed per call.

To be implemented in a later task, after a real model has been trained.
"""

from __future__ import annotations

IMPLEMENTED = False

DISCLAIMER = (
    "AI-assisted early screening result, not a confirmed agricultural "
    "diagnosis. Verify with an agronomist or local extension officer."
)


def load_model(weights_path: str):
    """Load trained weights plus the saved class map and preprocess config.

    Not implemented. Will raise ``FileNotFoundError`` if the weights do not
    exist — it will not fabricate a randomly-initialised model and present its
    output as a prediction.
    """
    raise NotImplementedError(
        "load_model() is not implemented yet, and no trained weights exist in "
        "ml/models/. This will not be faked."
    )


def predict(image_path: str, weights_path: str) -> dict:
    """Run end-to-end inference on one image and return the A-E result dict.

    Not implemented. See the planned output shape in this module's docstring.
    """
    raise NotImplementedError(
        "predict() is not implemented yet. No model has been trained, so there "
        "is no real prediction to return. See ml/README.md section 10."
    )


def build_recommendation(condition: str, disease_pest: str) -> dict:
    """Map a real predicted class to a risk level and a recommendation.

    Not implemented. This will use an explicit, reviewable lookup table owned by
    the team rather than generated text, so agronomic advice stays consistent
    and reviewable.
    """
    raise NotImplementedError(
        "build_recommendation() is not implemented yet. The mapping from class "
        "to advice is team content, not something to be invented."
    )


def main() -> None:
    """CLI entry point: ``python -m src.predict --image leaf.jpg --weights ml/models/<name>.pt``

    Not implemented.
    """
    raise NotImplementedError(
        "Inference is not implemented yet because no model has been trained."
    )


if __name__ == "__main__":  # pragma: no cover
    main()
