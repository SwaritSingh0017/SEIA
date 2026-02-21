from flask import Blueprint, render_template, request, jsonify, abort
from models import db, User, Message, Mood, Task, Journal, Review
from datetime import datetime, timedelta
import os
 
admin_bp = Blueprint("admin", __name__)
 
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "")
 
def check_admin():
    token = request.args.get("token", "")
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        abort(403)
 
@admin_bp.route("/admin/stats")
def stats():
    check_admin()
    since_7d = datetime.utcnow() - timedelta(days=7)
    data = {
        "users":          User.query.count(),
        "new_users_7d":   User.query.filter(User.created_at >= since_7d).count(),
        "messages":       Message.query.count(),
        "messages_7d":    Message.query.filter(Message.timestamp >= since_7d).count(),
        "mood_logs":      Mood.query.count(),
        "tasks":          Task.query.count(),
        "journals":       Journal.query.count(),
        "reviews":        Review.query.count(),
        "avg_rating":     round(
            db.session.query(db.func.avg(Review.rating)).scalar() or 0, 1
        ),
        "mode_breakdown": {
            mode: Message.query.filter_by(role="user", mode=mode).count()
            for mode in ["friend", "partner", "coder", "therapist", "agent"]
        },
    }
    return jsonify(data)
 
@admin_bp.route("/admin/users")
def users():
    check_admin()
    users = User.query.order_by(User.created_at.desc()).limit(50).all()
    return jsonify([{
        "id":       u.id,
        "name":     u.name,
        "email":    u.email,
        "mode":     u.current_mode,
        "joined":   u.created_at.isoformat(),
        "messages": Message.query.filter_by(user_id=u.id).count(),
    } for u in users])
