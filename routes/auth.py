# routes/auth.py — Authentication Routes
from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
 
auth_bp = Blueprint("auth", __name__)
 
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect("/dashboard")
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        name     = request.form.get("name", "").strip()
        if not email or not password or not name:
            flash("All fields are required.", "error")
            return redirect("/signup")
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return redirect("/signup")
        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please log in.", "error")
            return redirect("/login")
        user = User(
            email=email, name=name,
            password=generate_password_hash(password),
            current_mode="friend"
        )
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect("/dashboard")
    return render_template("signup.html")
 
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/dashboard")
    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect("/dashboard")
        flash("Invalid email or password.", "error")
    return render_template("login.html")
 
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
 
@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)
