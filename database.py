# database.py — Database initialization
from models import db
 
def init_db(app):
    """Initialize the database with the Flask app."""
    with app.app_context():
        db.create_all()  # Creates all tables if they don't exist
        print("Database initialized successfully!")
