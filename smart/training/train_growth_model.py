import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from smart.engine.data_loader import load_all_weights

MODEL_PATH = "smart/models/growth_model.pkl"

def train_growth_model():
    data = load_all_weights()
    if data.empty:
        return False

    X = data.groupby("animal_id").cumcount().values.reshape(-1, 1)
    y = data["weight"].values

    model = RandomForestRegressor(n_estimators=200)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    return True
