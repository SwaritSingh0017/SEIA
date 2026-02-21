# models.py — Database Models
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
 
db = SQLAlchemy()
 
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id           = db.Column(db.Integer, primary_key=True)
    email        = db.Column(db.String(120), unique=True, nullable=False)
    name         = db.Column(db.String(80), nullable=False)
    password     = db.Column(db.String(255), nullable=False)
    current_mode = db.Column(db.String(20), default="friend")
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship("Message", backref="user", lazy=True)
    moods    = db.relationship("Mood",    backref="user", lazy=True)
    tasks    = db.relationship("Task",    backref="user", lazy=True)
    journals = db.relationship("Journal", backref="user", lazy=True)
    reviews  = db.relationship("Review",  backref="user", lazy=True)
 
class Message(db.Model):
    __tablename__ = "messages"
    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role      = db.Column(db.String(20), nullable=False)  # user or assistant
    content   = db.Column(db.Text, nullable=False)
    mode      = db.Column(db.String(20), default="friend")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
 
class Mood(db.Model):
    __tablename__ = "moods"
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    score         = db.Column(db.Integer, nullable=False)  # 1 to 10
    note          = db.Column(db.Text, default="")
    auto_detected = db.Column(db.Boolean, default=False)
    timestamp     = db.Column(db.DateTime, default=datetime.utcnow)
 
class Task(db.Model):
    __tablename__ = "tasks"
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title      = db.Column(db.String(255), nullable=False)
    done       = db.Column(db.Boolean, default=False)
    priority   = db.Column(db.String(10), default="normal")  # low/normal/high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
 
class Journal(db.Model):
    __tablename__ = "journals"
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content    = db.Column(db.Text, nullable=False)
    mood_score = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
 
class Review(db.Model):
    __tablename__ = "reviews"
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    rating     = db.Column(db.Integer, nullable=False)  # 1 to 5
    text       = db.Column(db.Text, nullable=False)
    mode_used  = db.Column(db.String(20), default="friend")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
