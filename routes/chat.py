from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
import requests as http
from models import db, Message, Mood
from config import OPENROUTER_KEY, FREE_MODEL, MODES, CRISIS_PHRASES, CRISIS_RESPONSE
from routes.n8n_handler import trigger_n8n

chat_bp = Blueprint("chat", __name__)

def detect_mode(text):
    t = text.lower()
    for mode_name, data in MODES.items():
        if mode_name == "friend":
            continue
        for trigger in data["triggers"]:
            if trigger in t:
                return mode_name
    return None

def detect_crisis(text):
    t = text.lower()
    return any(phrase in t for phrase in CRISIS_PHRASES)

def auto_mood_score(text):
    neg = ["sad", "anxious", "depressed", "stressed", "tired", "hopeless",
           "crying", "hate", "awful", "terrible", "miserable", "lonely",
           "worthless", "empty", "numb", "scared", "worried", "overwhelmed"]
    pos = ["happy", "great", "amazing", "excited", "wonderful", "love",
           "fantastic", "good", "blessed", "grateful", "joy", "ecstatic",
           "proud", "calm", "peaceful", "motivated", "energized"]
    t = text.lower()
    n = sum(1 for w in neg if w in t)
    p = sum(1 for w in pos if w in t)
    if n > p:
        return max(1, 5 - n)
    if p > n:
        return min(10, 5 + p)
    return None

@chat_bp.route("/chat")
@login_required
def chat_page():
    mode_info = MODES.get(current_user.current_mode, MODES["friend"])
    return render_template("chat.html", user=current_user,
                           mode_info=mode_info, modes=MODES)

@chat_bp.route("/api/chat", methods=["POST"])
@login_required
def chat_api():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    user = current_user

    # Mode switch detection
    new_mode = detect_mode(user_input)
    mode_switched = False
    if new_mode and new_mode != user.current_mode:
        user.current_mode = new_mode
        db.session.commit()
        mode_switched = True

    # Crisis safety check — always first
    if detect_crisis(user_input):
        db.session.add(Message(user_id=user.id, role="user",
                               content=user_input, mode=user.current_mode))
        db.session.add(Message(user_id=user.id, role="assistant",
                               content=CRISIS_RESPONSE, mode=user.current_mode))
        db.session.commit()
        return jsonify({
            "response": CRISIS_RESPONSE,
            "mode": user.current_mode,
            "mode_label": MODES[user.current_mode]["label"],
            "mode_color": MODES[user.current_mode]["color"],
            "crisis": True,
        })

    # Auto mood from message tone
    score = auto_mood_score(user_input)
    if score:
        db.session.add(Mood(user_id=user.id, score=score,
                            note="auto-detected", auto_detected=True))
        db.session.commit()

    # Build conversation history (last 20 messages)
    history = (Message.query
               .filter_by(user_id=user.id)
               .order_by(Message.id.desc())
               .limit(20)
               .all())
    history.reverse()
    messages = [{"role": m.role if m.role != "assistant" else "assistant",
                 "content": m.content} for m in history]
    messages.append({"role": "user", "content": user_input})

    system = MODES[user.current_mode]["system"]

    # Call OpenRouter
    try:
        res = http.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://seia.onrender.com",
                "X-Title": "SEIA",
            },
            json={
                "model": FREE_MODEL,
                "messages": [{"role": "system", "content": system}] + messages,
            },
            timeout=30,
        )
        if res.status_code != 200:
            reply = f"SEIA couldn't reach the AI server (status {res.status_code}). Try again."
        else:
            reply = res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"Connection error: {str(e)[:120]}"

    # Persist both messages
    db.session.add(Message(user_id=user.id, role="user",
                           content=user_input, mode=user.current_mode))
    db.session.add(Message(user_id=user.id, role="assistant",
                           content=reply, mode=user.current_mode))
    db.session.commit()

    # n8n for agent mode
    n8n_result = None
    if user.current_mode == "agent":
        n8n_result = trigger_n8n(user_input, reply)

    mode_data = MODES[user.current_mode]
    return jsonify({
        "response": reply,
        "mode": user.current_mode,
        "mode_label": mode_data["label"],
        "mode_color": mode_data["color"],
        "mode_switched": mode_switched,
        "auto_mood": score,
        "n8n": n8n_result,
    })

@chat_bp.route("/api/history")
@login_required
def history():
    msgs = (Message.query
            .filter_by(user_id=current_user.id)
            .order_by(Message.timestamp)
            .all())
    return jsonify([{
        "role":    m.role,
        "content": m.content,
        "mode":    m.mode,
        "color":   MODES.get(m.mode, MODES["friend"])["color"],
        "time":    m.timestamp.strftime("%H:%M"),
    } for m in msgs])

@chat_bp.route("/api/reset", methods=["POST"])
@login_required
def reset():
    Message.query.filter_by(user_id=current_user.id).delete()
    current_user.current_mode = "friend"
    db.session.commit()
    return jsonify({"success": True})
