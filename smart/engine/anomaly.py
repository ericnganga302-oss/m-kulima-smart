import numpy as np
from sklearn.ensemble import IsolationForest


class HealthAnomalyDetector:
    """
    Learns normal animal behavior and detects anomalies
    """

    def __init__(self):
        self.model = IsolationForest(
            n_estimators=150,
            contamination=0.1,
            random_state=42
        )
        self.trained = False

    def train(self, sensor_matrix):
        """
        sensor_matrix: list of [temperature, activity]
        """
        X = np.array(sensor_matrix)
        self.model.fit(X)
        self.trained = True

    def predict(self, sensor_row):
        """
        sensor_row: [temperature, activity]
        """
        if not self.trained:
            raise RuntimeError("Anomaly model not trained")

        result = self.model.predict([sensor_row])[0]
        return "ANOMALY" if result == -1 else "NORMAL"
