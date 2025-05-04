from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Run(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    data = db.Column(db.Text, nullable=False) # Stores the run as JSON
    
    def set_data(self, encounters):
        self.data = json.dumps(encounters)
    
    def get_data(self):
        return json.loads(self.data)