# routes/mood.py — Mental Health Mood Tracking
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from models import db, Mood
from datetime import datetime, timedelta
 
mood_bp = Blueprint("mood", __name__)
 
@mood_bp.route("/api/mood/log", methods=["POST"])
@login_required
def log_mood():
    data  = request.json
    score = int(data.get("score", 5))
    note  = data.get("note", "")
    score = max(1, min(10, score))  # Clamp between 1-10
    mood = Mood(user_id=current_user.id, score=score,
               note=note, auto_detected=False)
    db.session.add(mood)
    db.session.commit()
    return jsonify({"success": True, "score": score})
 
@mood_bp.route("/api/mood/history")
@login_required
def mood_history():
    days  = int(request.args.get("days", 30))
    since = datetime.utcnow() - timedelta(days=days)
    moods = Mood.query.filter(
        Mood.user_id == current_user.id,
        Mood.timestamp >= since
    ).order_by(Mood.timestamp).all()
    return jsonify([{
        "date":  m.timestamp.strftime("%Y-%m-%d"),
        "time":  m.timestamp.strftime("%H:%M"),
        "score": m.score,
        "note":  m.note,
        "auto":  m.auto_detected
    } for m in moods])
 
@mood_bp.route("/api/mood/streak")
@login_required
def streak():
    moods  = Mood.query.filter_by(user_id=current_user.id).order_by(Mood.timestamp.desc()).all()
    dates  = set(m.timestamp.date() for m in moods)
    streak = 0
    day    = datetime.utcnow().date()
    while day in dates:
        streak += 1
        day -= timedelta(days=1)
    return jsonify({"streak": streak})
 
@mood_bp.route("/api/mood/average")
@login_required
def average():
    moods = Mood.query.filter_by(user_id=current_user.id).all()
    if not moods: return jsonify({"average": 0})
    avg = sum(m.score for m in moods) / len(moods)
    return jsonify({"average": round(avg, 1)})
