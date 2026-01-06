import numpy as np
from sklearn.ensemble import IsolationForest

_model = IsolationForest(contamination=0.1)

def train_health_model(sensor_df):
    X = sensor_df[["temperature", "activity"]]
    _model.fit(X)

def predict_health(sensor_payload):
    X = np.array([[sensor_payload["temperature"], sensor_payload["activity"]]])
    return _model.predict(X)[0]  # -1 = anomaly
def predict_health(payload):
    return 1  # safe default
