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

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)

    def set_data(self, char_data):
        """Store character data as JSON string."""
        self.data = json.dumps(char_data)

    def get_data(self):
        """Return character data as a Python dict."""
        return json.loads(self.data)