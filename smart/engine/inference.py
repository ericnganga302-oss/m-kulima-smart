# smart/engine/inference.py
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from smart.engine.diagnosis import diagnose_disease
from smart.engine.data_loader import load_weight_history

def health_status(data):
    """Processes real-time risk assessment."""
    temp = data.get("temperature", 38.5)
    if temp > 39.5: return {"status": "FEVER", "risk": "high", "message": "High Metabolic Heat"}
    return {"status": "STABLE", "risk": "low", "message": "Optimal"}

def disease_prediction(animal_id, temp, activity):
    """Bridge to the Probabilistic Diagnostic AI."""
    return diagnose_disease(animal_id, temp, activity)

def forecast_growth(animal_id, days_ahead):
    """
    AI FORECAST: Linear Regression on historical Supabase data.
    Calculates Average Daily Gain (ADG).
    """
    df = load_weight_history(animal_id)
    
    if len(df) < 3:
        return {"status": "insufficient_data", "message": "Need at least 3 weight logs for AI Regression."}

    # Prepare data for Scikit-Learn
    # Convert dates to 'days since first recording'
    df['date'] = pd.to_datetime(df['date'])
    df['days'] = (df['date'] - df['date'].min()).dt.days
    
    X = df[['days']].values
    y = df['weight'].values

    # Train Linear Model
    model = LinearRegression()
    model.fit(X, y)

    # Predict future
    last_day = df['days'].max()
    future_days = np.array([last_day + i for i in range(1, days_ahead + 1)]).reshape(-1, 1)
    predictions = model.predict(future_days)
    
    adg = model.coef_[0] # The slope of the line is the ADG

    return {
        "status": "success",
        "adg": round(adg, 3),
        "prediction": predictions.tolist(),
        "eta_days": days_ahead
    }