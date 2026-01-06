import numpy as np
import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "growth_model.pkl"


def explain_growth(weights):
    """
    Explains growth behavior using linear model slope
    """
    if len(weights) < 3 or not MODEL_PATH.exists():
        return {
            "trend": "INSUFFICIENT DATA",
            "rate": 0,
            "confidence": "LOW"
        }

    model = joblib.load(MODEL_PATH)
    slope = model.coef_[0]

    if slope > 0.5:
        trend = "FAST GROWTH"
    elif slope > 0.1:
        trend = "NORMAL GROWTH"
    else:
        trend = "SLOW / STALLED GROWTH"

    confidence = "HIGH" if len(weights) >= 5 else "MEDIUM"

    return {
        "trend": trend,
        "rate": round(slope, 3),
        "confidence": confidence
    }
