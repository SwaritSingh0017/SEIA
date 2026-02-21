# routes/chat.py — SEIA Chat Engine
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
import requests as http
from models import db, Message, Mood
from config import OPENROUTER_KEY, FREE_MODEL, MODES, CRISIS_PHRASES, CRISIS_RESPONSE
from routes.n8n_handler import trigger_n8n
 
chat_bp = Blueprint("chat", __name__)
 
def detect_mode(text):
    t = text.lower()
    for mode, data in MODES.items():
        if mode == "friend": continue
        for trigger in data["triggers"]:
            if trigger in t:
                return mode
    return None
 
def detect_crisis(text):
    t = text.lower()
    return any(phrase in t for phrase in CRISIS_PHRASES)
 
def auto_mood_score(text):
    neg = ["sad","anxious","depressed","stressed","tired","hopeless",
           "crying","hate","awful","terrible","miserable","lonely"]
    pos = ["happy","great","amazing","excited","wonderful","love",
           "fantastic","good","blessed","grateful","joy","ecstatic"]
    t = text.lower()
    n = sum(1 for w in neg if w in t)
    p = sum(1 for w in pos if w in t)
    if n > p: return max(1, 5 - n)
    if p > n: return min(10, 5 + p)
    return None
 
@chat_bp.route("/chat")
@login_required
def chat_page():
    return render_template("chat.html", user=current_user)
 
@chat_bp.route("/api/chat", methods=["POST"])
@login_required
def chat_api():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"error": "Empty message"}), 400
 
    user = current_user
 
    # Detect & switch mode
    new_mode = detect_mode(user_input)
    if new_mode and new_mode != user.current_mode:
        user.current_mode = new_mode
        db.session.commit()
 
    # Crisis check (safety first)
    if detect_crisis(user_input):
        return jsonify({
            "response": CRISIS_RESPONSE,
            "mode": user.current_mode,
            "crisis": True
        })
 
    # Auto mood detection
    score = auto_mood_score(user_input)
    if score:
        db.session.add(Mood(user_id=user.id, score=score, auto_detected=True))
        db.session.commit()
 
    # Load last 20 messages for context
    history = Message.query.filter_by(user_id=user.id).order_by(Message.id.desc()).limit(20).all()
    history.reverse()
    messages = [{"role": m.role, "content": m.content} for m in history]
    messages.append({"role": "user", "content": user_input})
 
    system = MODES[user.current_mode]["system"]
 
    # Call OpenRouter free model
    try:
        res = http.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://seia.pythonanywhere.com"
            },
            json={
                "model": FREE_MODEL,
                "messages": [{"role": "system", "content": system}] + messages
            },
            timeout=30
        )
        reply = res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"SEIA hit a connection error: {str(e)}"
 
    # Save messages to database
    db.session.add(Message(user_id=user.id, role="user",
                          content=user_input, mode=user.current_mode))
    db.session.add(Message(user_id=user.id, role="assistant",
                          content=reply, mode=user.current_mode))
    db.session.commit()
 
    # Trigger n8n for agent mode
    n8n_result = None
    if user.current_mode == "agent":
        n8n_result = trigger_n8n(user_input, reply)
 
    return jsonify({
        "response": reply,
        "mode": user.current_mode,
        "n8n": n8n_result,
        "auto_mood": score
    })
 
@chat_bp.route("/api/history")
@login_required
def chat_history():
    msgs = Message.query.filter_by(user_id=current_user.id).order_by(Message.timestamp).all()
    return jsonify([{"role": m.role, "content": m.content,
                    "mode": m.mode, "time": m.timestamp.isoformat()}
                   for m in msgs])
 
@chat_bp.route("/api/reset", methods=["POST"])
@login_required
def reset_chat():
    Message.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({"success": True})
