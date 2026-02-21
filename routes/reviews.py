# routes/reviews.py — Review System
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from models import db, Review, User
 
reviews_bp = Blueprint("reviews", __name__)
 
@reviews_bp.route("/reviews")
def reviews_page():
    reviews = Review.query.order_by(Review.created_at.desc()).limit(50).all()
    data = []
    for r in reviews:
        user = User.query.get(r.user_id)
        data.append({
            "name": user.name if user else "Anonymous",
            "rating": r.rating, "text": r.text,
            "mode": r.mode_used,
            "date": r.created_at.strftime("%b %d, %Y")
        })
    return render_template("reviews.html", reviews=data)
 
@reviews_bp.route("/api/reviews", methods=["POST"])
@login_required
def submit_review():
    data   = request.json
    rating = int(data.get("rating", 5))
    text   = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Review text required"}), 400
    review = Review(
        user_id=current_user.id,
        rating=max(1, min(5, rating)),
        text=text,
        mode_used=current_user.current_mode
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"success": True})
