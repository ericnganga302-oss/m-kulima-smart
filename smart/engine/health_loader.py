import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "health_sensors.csv"

def load_health_data(animal_id):
    df = pd.read_csv(DATA_PATH)
    df = df[df["animal_id"] == animal_id]
    return df[["temperature", "activity", "feed_intake"]].values
