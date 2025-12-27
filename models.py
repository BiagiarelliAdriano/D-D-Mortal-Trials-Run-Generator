from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from sqlalchemy.sql import func

db = SQLAlchemy()

class Run(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_run = db.Column(db.String(100), unique=True, nullable=False)  # Name should be more descriptive
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)  # Use func.now() for timestamp
    data = db.Column(db.Text, nullable=False)  # Stores the run as JSON
    
    def set_data(self, encounters):
        self.data = json.dumps(encounters)
    
    def get_data(self):
        return json.loads(self.data)

DEFAULT_CHARACTER_DATA = {
    "class_name": "",
    "subclass": "",
    "level": 1,
    
    "abilities": {
        "strength": 10,
        "dexterity": 10,
        "constitution": 10,
        "intelligence": 10,
        "wisdom": 10,
        "charisma": 10
    }
}

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)

    def set_data(self, char_data):
        """Merge provided data with defaults and store as JSON."""
        merged = DEFAULT_CHARACTER_DATA.copy()
        merged.update(char_data)
        
        # Deep-merge abilities if provided
        if "abilities" in char_data:
            merged["abilities"] = DEFAULT_CHARACTER_DATA["abilities"].copy()
            merged["abilities"].update(char_data["abilities"])
        
        self.data = json.dumps(merged)

    def get_data(self):
        """Return character data as a Python dict."""
        return json.loads(self.data)