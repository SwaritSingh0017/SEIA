# app.py — SEIA Main Flask Application
from flask import Flask, render_template, redirect
from flask_login import LoginManager, current_user
from models import db, User
from database import init_db
from config import SECRET_KEY, DATABASE_URL
import os
 
def create_app():
    app = Flask(__name__)
 
    # Configuration
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
 
    # Initialize extensions
    db.init_app(app)
 
    # Login manager setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access SEIA."
 
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
 
    # Register all route blueprints
    from routes.auth     import auth_bp
    from routes.chat     import chat_bp
    from routes.mood     import mood_bp
    from routes.tasks    import tasks_bp
    from routes.journal  import journal_bp
    from routes.reviews  import reviews_bp
 
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(mood_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(reviews_bp)
 
    # Root routes
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect("/dashboard")
        return render_template("landing.html")
 
    @app.route("/dashboard")
    def dashboard():
        from flask_login import login_required
        if not current_user.is_authenticated:
            return redirect("/login")
        return render_template("dashboard.html", user=current_user)
 
    # Initialize database
    init_db(app)
 
    return app
 
 
app = create_app()
 
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
