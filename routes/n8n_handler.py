# routes/n8n_handler.py — n8n Automation Trigger
import requests
from config import N8N_WEBHOOK, NTFY_TOPIC
 
def trigger_n8n(user_message, seia_reply):
    """
    Sends user message to n8n when SEIA is in Agent mode.
    n8n then parses intent and executes the action.
    """
    if not N8N_WEBHOOK:
        return {"status": "n8n not configured"}
    try:
        payload = {
            "message": user_message,
            "seia_reply": seia_reply,
            "source": "seia-agent-mode"
        }
        res = requests.post(N8N_WEBHOOK, json=payload, timeout=15)
        return res.json()
    except Exception as e:
        return {"error": str(e)}
 
def send_ntfy_notification(title, message, tags="bell"):
    """Send a push notification to all devices via ntfy.sh"""
    if not NTFY_TOPIC:
        return False
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            json={
                "topic": NTFY_TOPIC,
                "title": title,
                "message": message,
                "tags": [tags]
            },
            timeout=10
        )
        return True
    except:
        return False
