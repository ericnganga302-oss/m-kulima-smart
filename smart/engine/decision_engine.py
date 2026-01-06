def market_decision(
    current_weight,
    forecast,
    health_status,
    target_weight=400
):
    if health_status == -1:
        return {
            "status": "CRITICAL",
            "action": "Health anomaly detected. Check animal immediately.",
            "confidence": "High"
        }

    for day, weight in enumerate(forecast):
        if weight >= target_weight:
            return {
                "status": "READY",
                "action": f"Target weight reached in ~{day} days. Prepare for market.",
                "confidence": "Medium"
            }

    return {
        "status": "WAIT",
        "action": "Continue feeding and monitoring.",
        "confidence": "Medium"
    }
