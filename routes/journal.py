# routes/journal.py — Private Journal
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from models import db, Journal
 
journal_bp = Blueprint("journal", __name__)
 
@journal_bp.route("/journal")
@login_required
def journal_page():
    return render_template("journal.html", user=current_user)
 
@journal_bp.route("/api/journal", methods=["POST"])
@login_required
def write_entry():
    data = request.json
    entry = Journal(
        user_id=current_user.id,
        content=data.get("content", "").strip(),
        mood_score=data.get("mood_score")
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({"success": True})
 
@journal_bp.route("/api/journal")
@login_required
def get_entries():
    entries = Journal.query.filter_by(user_id=current_user.id).order_by(Journal.created_at.desc()).all()
    return jsonify([{
        "id": e.id, "content": e.content,
        "mood": e.mood_score,
        "date": e.created_at.strftime("%Y-%m-%d %H:%M")
    } for e in entries])
