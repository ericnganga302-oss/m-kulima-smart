"""
smart.engine.inference
---------------------
Central intelligence layer for M-Kulima Smart.

Includes:
- ML-based growth prediction
- Hybrid health intelligence (ML + rules)
- Alert triggering
- Safe fallbacks (NO crashes)
"""

import os
import joblib
import numpy as np

from smart.engine.data_loader import load_weight_history
from smart.engine.alerts import send_alert

# Optional ML health model (safe import)
try:
    from smart.engine.health_ml import predict_health
    HEALTH_ML_AVAILABLE = True
except Exception:
    HEALTH_ML_AVAILABLE = False


# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
MODEL_PATH = "smart/models/growth_model.pkl"
TARGET_WEIGHT = 400  # kg


# ------------------------------------------------------------------
# Growth Prediction (ML + Fallback)
# ------------------------------------------------------------------
def forecast_growth(animal_id, days_ahead=30):
    """
    Predict future weight growth for an animal.
    """

    weights = load_weight_history(animal_id)

    if not weights or len(weights) < 3:
        return {
            "status": "insufficient_data",
            "prediction": [],
            "eta_days": None,
            "message": "Not enough historical data"
        }

    # ---- ML model ----
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)

            X = np.arange(len(weights)).reshape(-1, 1)
            future_X = np.arange(len(weights), len(weights) + days_ahead).reshape(-1, 1)

            preds = model.predict(future_X)

            return {
                "status": "ml",
                "prediction": preds.tolist(),
                "eta_days": _eta_to_target(preds),
            }
        except Exception:
            pass

    # ---- Fallback ----
    daily_gain = np.mean(np.diff(weights))
    preds = [weights[-1] + daily_gain * i for i in range(1, days_ahead + 1)]

    return {
        "status": "fallback",
        "prediction": preds,
        "eta_days": _eta_to_target(preds),
    }


def _eta_to_target(predictions):
    for i, w in enumerate(predictions):
        if w >= TARGET_WEIGHT:
            return i + 1
    return None


# ------------------------------------------------------------------
# HEALTH INTELLIGENCE (THIS IS WHAT YOU ASKED FOR)
# ------------------------------------------------------------------
def health_status(sensor_payload):
    """
    Hybrid health intelligence:
    - Uses ML anomaly detection if available
    - Falls back to rule-based logic
    - Triggers alerts automatically
    """

    animal_id = sensor_payload.get("animal_id", "UNKNOWN")
    temp = sensor_payload.get("temperature")
    activity = sensor_payload.get("activity")

    if temp is None or activity is None:
        return {
            "status": "unknown",
            "risk": "missing_data",
            "message": "Incomplete sensor data"
        }

    # --------------------------------------------------------------
    # 1️⃣ ML-BASED HEALTH ANOMALY DETECTION
    # --------------------------------------------------------------
    if HEALTH_ML_AVAILABLE:
        try:
            anomaly = predict_health({
                "temperature": temp,
                "activity": activity
            })

            if anomaly == -1:
                send_alert(
                    animal_id=animal_id,
                    message="ML anomaly detected: unusual behavior"
                )

                return {
                    "status": "alert",
                    "risk": "high",
                    "message": "ML anomaly detected (possible illness)"
                }

        except Exception:
            pass  # ML failed → fallback below

    # --------------------------------------------------------------
    # 2️⃣ RULE-BASED SAFETY NET
    # --------------------------------------------------------------
    if temp >= 40.5 or activity <= 25:
        send_alert(
            animal_id=animal_id,
            message="Critical health warning: fever or inactivity"
        )

        return {
            "status": "alert",
            "risk": "high",
            "message": "High fever or severe inactivity detected"
        }

    if temp >= 39.5 or activity <= 50:
        return {
            "status": "warning",
            "risk": "medium",
            "message": "Possible early stress or infection"
        }

    return {
        "status": "normal",
        "risk": "low",
        "message": "Animal appears healthy"
    }


# ------------------------------------------------------------------
# Batch Health Scoring (Dashboards / Reports)
# ------------------------------------------------------------------
def batch_health_score(sensor_df):
    """
    Score multiple sensor records at once.
    """

    results = []
    for _, row in sensor_df.iterrows():
        results.append(
            health_status({
                "animal_id": row.get("animal_id"),
                "temperature": row.get("temperature"),
                "activity": row.get("activity")
            })["risk"]
        )

    return results
