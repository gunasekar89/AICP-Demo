"""Explainable AI utilities leveraging SHAP and LIME visualisations."""

from __future__ import annotations

import numpy as np
import pandas as pd

try:  # pragma: no cover - optional heavy dependencies
    import shap  # type: ignore
except Exception:  # pragma: no cover - fallback stub
    shap = None

try:  # pragma: no cover
    from lime.lime_tabular import LimeTabularExplainer  # type: ignore
except Exception:  # pragma: no cover - fallback stub
    LimeTabularExplainer = None


def generate_sample_features(size: int = 100) -> pd.DataFrame:
    """Generate synthetic feature matrix used for XAI demonstrations."""

    rng = np.random.default_rng(123)
    return pd.DataFrame(
        {
            "behavior_score": rng.uniform(0, 1, size),
            "patch_latency": rng.normal(5, 1, size),
            "identity_anomaly": rng.uniform(0, 1, size),
            "cloud_risk": rng.uniform(0, 1, size),
        }
    )


def shap_summary(model_predict, features: pd.DataFrame):
    """Compute SHAP values when the dependency is available."""

    if shap is None:
        return {"available": False, "reason": "SHAP not installed"}
    explainer = shap.KernelExplainer(model_predict, features)
    shap_values = explainer.shap_values(features, nsamples=20)
    return {"available": True, "values": shap_values.tolist()}


def lime_explanation(model_predict, features: pd.DataFrame):
    """Generate a single LIME explanation for the first sample."""

    if LimeTabularExplainer is None:
        return {"available": False, "reason": "LIME not installed"}
    explainer = LimeTabularExplainer(
        training_data=features.values,
        feature_names=list(features.columns),
        mode="regression",
    )
    explanation = explainer.explain_instance(features.iloc[0].values, model_predict)
    return {"available": True, "weights": explanation.as_map()[1] if 1 in explanation.as_map() else []}
