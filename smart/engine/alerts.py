"""
smart.engine.alerts
------------------
Notification layer (SMS / WhatsApp / Email ready)
"""

def send_alert(animal_id, message, channel="console"):
    """
    Send alert to farmer.
    channel: console | sms | whatsapp
    """

    if channel == "console":
        print(f"[ALERT] Animal {animal_id}: {message}")

    # Future integrations
    elif channel == "sms":
        pass  # Twilio / Africa's Talking

    elif channel == "whatsapp":
        pass  # WhatsApp Business API
