# routes/tasks.py — Task Manager
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Task
 
tasks_bp = Blueprint("tasks", __name__)
 
@tasks_bp.route("/api/tasks", methods=["GET"])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return jsonify([{
        "id": t.id, "title": t.title,
        "done": t.done, "priority": t.priority
    } for t in tasks])
 
@tasks_bp.route("/api/tasks", methods=["POST"])
@login_required
def add_task():
    data = request.json
    task = Task(
        user_id=current_user.id,
        title=data.get("title", "").strip(),
        priority=data.get("priority", "normal")
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"success": True, "id": task.id})
 
@tasks_bp.route("/api/tasks/<int:task_id>/done", methods=["POST"])
@login_required
def mark_done(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.done = not task.done
    db.session.commit()
    return jsonify({"success": True, "done": task.done})
 
@tasks_bp.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({"success": True})
