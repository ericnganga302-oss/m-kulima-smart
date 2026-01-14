# smart/engine/diagnosis.py
import numpy as np

class AegisDiagnosticAI:
    def __init__(self):
        # Disease Fingerprints: Weights for [Temp_Score, Activity_Score]
        self.knowledge_base = {
            "East Coast Fever": {"weights": [0.7, 0.3], "threshold": 0.8},
            "Milk Fever": {"weights": [0.4, 0.6], "threshold": 0.75},
            "Mastitis": {"weights": [0.6, 0.4], "threshold": 0.65}
        }

    def compute_probability(self, temp, activity):
        """
        AI CORE: Calculates probability vectors for pathologies.
        Normalization based on biological variance in Dairy Cattle.
        """
        # Normalize Temperature (Standard Dairy: 38.5C)
        # Fever probability follows a sigmoid-like curve
        temp_score = 1 / (1 + np.exp(-(temp - 39.5))) 
        
        # Normalize Activity (Lethargy is a signal)
        # Lower activity = higher score (Max score at 0 steps)
        activity_score = np.clip((100 - activity) / 100, 0, 1)

        results = []
        for disease, config in self.knowledge_base.items():
            # Dot product of current signals and disease weights
            probability = np.dot([temp_score, activity_score], config["weights"])
            
            if probability > 0.4: # Filter noise
                results.append({
                    "disease": disease,
                    "confidence": round(float(probability * 100), 2),
                    "status": "CRITICAL" if probability > config["threshold"] else "MONITOR"
                })
        
        return sorted(results, key=lambda x: x['confidence'], reverse=True)

def diagnose_disease(animal_id, temperature, activity):
    ai = AegisDiagnosticAI()
    predictions = ai.compute_probability(temperature, activity)
    
    if not predictions:
        return {"disease": "Healthy", "confidence": 100, "action": "Vitals Normal."}
    
    top = predictions[0]
    actions = {
        "East Coast Fever": "Immediate Buparvaquone therapy required.",
        "Milk Fever": "IV Calcium Borogluconate needed.",
        "Mastitis": "Intramammary antibiotic infusion."
    }
    
    return {
        "disease": top["disease"],
        "confidence": top["confidence"],
        "action": actions.get(top["disease"], "Consult Vet.")
    }