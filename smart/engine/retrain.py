"""
smart.training.retrain
---------------------
Handles background retraining of ML models when new data is ingested.
Currently lightweight (stub) but production-safe.
"""

import os
import joblib
from datetime import datetime

MODEL_DIR = "smart/models"
MODEL_PATH = os.path.join(MODEL_DIR, "growth_model.pkl")



from smart.training.train_growth_model import train_growth_model

def retrain_growth_model(training_data=None):
    return train_growth_model()



def retrain_growth_model(training_data=None):
    """
    Retrain the growth prediction model.
    Currently a safe stub that prepares the pipeline.

    Parameters
    ----------
    training_data : pd.DataFrame | None
        Optional new training data

    Returns
    -------
    bool
        True if retraining pipeline completed
    """

    # Ensure model directory exists
    os.makedirs(MODEL_DIR, exist_ok=True)

    # ---- STUB LOGIC (SAFE) ----
    # Later this will:
    # 1. Load historical weights
    # 2. Train ML model
    # 3. Save model to disk

    metadata = {
        "last_retrained": datetime.utcnow().isoformat(),
        "status": "stub",
    }

    joblib.dump(metadata, MODEL_PATH)

    print("✔ Growth model retraining completed (stub)")
    return True
