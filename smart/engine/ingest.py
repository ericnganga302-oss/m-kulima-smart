"""
smart.engine.ingest
------------------
Handles CSV ingestion for weights and sensor data.
"""

import pandas as pd
import sqlite3
from pathlib import Path

from smart.training.retrain import retrain_growth_model

DB_PATH = "smart/data/farm.db"


# -------------------------
# Internal helpers
# -------------------------
def _get_connection():
    Path("smart/data").mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


# -------------------------
# Public ingestion APIs
# -------------------------
def ingest_weight_csv(file):
    """
    Ingest animal weight history CSV

    Required columns:
    - animal_id
    - date
    - weight
    """

    df = pd.read_csv(file)

    required = {"animal_id", "date", "weight"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing columns: {required - set(df.columns)}")

    conn = _get_connection()
    df.to_sql("weights", conn, if_exists="append", index=False)
    conn.close()

    # Safe retraining trigger
    try:
        retrain_growth_model(df)
    except Exception as e:
        print(f"⚠ Retraining skipped: {e}")

    return True


def ingest_sensor_csv(file):
    """
    Ingest animal sensor CSV

    Required columns:
    - animal_id
    - timestamp
    - temperature
    - activity
    """

    df = pd.read_csv(file)

    required = {"animal_id", "timestamp", "temperature", "activity"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing columns: {required - set(df.columns)}")

    conn = _get_connection()
    df.to_sql("sensors", conn, if_exists="append", index=False)
    conn.close()

    return True
