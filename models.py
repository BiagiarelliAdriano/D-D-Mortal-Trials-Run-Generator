from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import random
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from encounter_generator.data.rules.game_rules import CLASS_HIT_DICE

db = SQLAlchemy()

class Run(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_run = db.Column(db.String(100), nullable=False) 
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    data = db.Column(db.Text, nullable=False)  # Stores the run as JSON
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    def set_data(self, encounters):
        self.data = json.dumps(encounters)
    
    def get_data(self):
        return json.loads(self.data)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=False, default="") # D&D class inspired avatar names or file path
    discord_id = db.Column(db.String(255), nullable=True)
    security_question = db.Column(db.String(255), nullable=True)
    security_answer_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # Patreon integration
    patreon_id = db.Column(db.String(100), nullable=True)
    patreon_connected = db.Column(db.Boolean, default=False)
    patreon_tier = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    
    # Relationship: A user can have many characters
    characters = db.relationship('Character', backref='owner', lazy=True, cascade="all, delete-orphan")
    reports = db.relationship('Report', backref='user', lazy=True, cascade="all, delete-orphan")
    notifications = db.relationship('UserNotification', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def set_security_answer(self, answer):
        # Lowercase and strip to make it slightly more forgiving
        clean_answer = answer.strip().lower()
        self.security_answer_hash = generate_password_hash(clean_answer)
        
    def check_security_answer(self, answer):
        clean_answer = answer.strip().lower()
        return check_password_hash(self.security_answer_hash, clean_answer)
    
    def has_unlimited_access(self):
        return self.is_admin or (
            self.patreon_connected and
            self.patreon_tier == "website"
        )

DEFAULT_CHARACTER_DATA = {
    "class_name": "",
    "subclass": "",
    "level": 1,
    "class_levels": [
        {
            "class_name": "",
            "level": 1,
            "subclass": ""
        }
    ],
    "xp": 0,
    "level_up_pending": False,
    "level_one_pending": True,
    "background": "",
    
    "hp_current": 0,
    "hp_max_base": 0,
    "hp_max_original": 0,
    "hp_modifier": 0,
    "hp_rolls": {},
    "hit_dice_remaining": 0,

    "heroicInspiration": False,
    
    "abilities": {
        "strength": 16,
        "dexterity": 14,
        "constitution": 12,
        "intelligence": 18,
        "wisdom": 20,
        "charisma": 8
    },
    "base_abilities": {
        "strength": 16,
        "dexterity": 14,
        "constitution": 12,
        "intelligence": 18,
        "wisdom": 20,
        "charisma": 8
    },
    "conditions": {
        "exhaustion": 0
    },
    "proficiencies": {
        "armor": [],
        "weapons": [],
        "tools": []
    },
    "skillProficiencies": {
        "acrobatics": False,
        "animal_handling": False,
        "arcana": False,
        "athletics": False,
        "deception": False,
        "history": False,
        "insight": False,
        "intimidation": False,
        "investigation": False,
        "medicine": False,
        "nature": False,
        "perception": False,
        "performance": False,
        "persuasion": False,
        "religion": False,
        "sleight_of_hand": False,
        "stealth": False,
        "survival": False,
    },
    "inventory": [],
    "gold": 0,
    "spell_slots_current": {},
}

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_private = db.Column(db.Boolean, default=False)

    def set_data(self, char_data):
        """
        Merge provided data with defaults and store as JSON.
        Supports deep merging for nested objects.
        """
        merged = json.loads(json.dumps(DEFAULT_CHARACTER_DATA)) # deep copy
        
        for key, value in char_data.items():
            if (
                isinstance(value, dict)
                and key in merged
                and isinstance(merged[key], dict)
            ):
                merged[key].update(value)
            else:
                merged[key] = value
        
        self.data = json.dumps(merged)

    def update_hp(self, new_level, con_mod):
        """
        Calculates HP using multiclass rules.
        Each class contributes its own Hit Dice pool.
        """
        data = self.get_data()
        class_levels = data.get("class_levels", [])
        hp_rolls = data.get("hp_rolls", {})
        
        # Convert old characters using the previous system
        if isinstance(hp_rolls, list):
            hp_rolls = {
                data.get("class_name", "Barbarian"): hp_rolls
            }
        
        total_character_levels = sum(
            cls.get("level", 0)
            for cls in class_levels
        )
        for cls in class_levels:
            class_name = cls.get("class_name")
            if not class_name:
                continue
            class_level = cls.get("level", 0)
            hit_die = CLASS_HIT_DICE.get(class_name, 8)
            if class_name not in hp_rolls:
                hp_rolls[class_name] = []
            current_rolls = hp_rolls[class_name]
            
            # Add missing levels
            while len(current_rolls) < class_level:
                # First level of entire character gets max HP
                if total_character_levels == class_level and len(current_rolls) == 0:
                    roll = hit_die
                else:
                    roll = random.randint(1, hit_die)
                
                current_rolls.append(roll)
            
            # Remove extra rolls if needed
            while len(current_rolls) > class_level:
                current_rolls.pop()
        
        # Calculate HP
        base_hp = 0
        
        for rolls in hp_rolls.values():
            base_hp += sum(rolls)
        con_bonus = new_level * con_mod
        hp_max_base = base_hp + con_bonus
        data["hp_rolls"] = hp_rolls
        data["hp_max_base"] = hp_max_base
        
        # Hit dice remaining equals total character level
        data["hit_dice_remaining"] = {
            class_name: len(rolls)
            for class_name, rolls in hp_rolls.items()
        }
        
        if data.get("hp_current", 0) == 0:
            data["hp_current"] = hp_max_base + data.get("hp_modifier", 0)
        
        self.set_data(data)

    def get_data(self):
        """Return character data as a Python dict."""
        data = json.loads(self.data)
        
        # Backfill missing keys (safe upgrade path)
        for key, value in DEFAULT_CHARACTER_DATA.items():
            if key not in data:
                data[key] = value
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    data[key].setdefault(subkey, subvalue)
        return data

class HostedRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invite_code = db.Column(db.String(6), unique=True, nullable=False)
    dm_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    run_id = db.Column(db.Integer, db.ForeignKey('run.id'), nullable=False)
    party_inventory = db.Column(db.Text, default='[]')
    claimed_items = db.Column(db.Text, default='[]')
    completed_encounters = db.Column(db.Text, default='[]')
    vault_gold = db.Column(db.Text, default='[]')
    shop_state = db.Column(db.Text, nullable=True)
    rations = db.Column(db.Float, default=3.0, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)

    # Relationships
    dm = db.relationship('User', foreign_keys=[dm_id], backref='hosted_runs_as_dm')
    run = db.relationship('Run', backref='hosted_session', uselist=False)
    # Changed backref to avoid collision if necessary, but participants seems unique
    participants = db.relationship('SessionParticipant', backref='hosted_run', cascade="all, delete-orphan")

class SessionParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hosted_run_id = db.Column(db.Integer, db.ForeignKey('hosted_run.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    role = db.Column(db.String(20), default='Ascendant') # 'DM' or 'Ascendant'
    joined_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    pending_rest = db.Column(db.String(20), nullable=True) # 'short' or 'long'

    # Relationships
    user = db.relationship('User', backref='session_participations')
    character = db.relationship('Character', backref='session_links')

class RecoveryRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Linked if username matches
    request_type = db.Column(db.String(20), nullable=False) # 'username', 'password', 'security_answer'
    status = db.Column(db.String(20), default='pending') # 'pending', 'resolved', 'denied'
    recovery_code = db.Column(db.String(8), nullable=True)
    code_expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    resolved_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    user = db.relationship('User', backref='recovery_requests')

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    report_type = db.Column(db.String(20), nullable=False) # 'Feedback' or 'Bug'
    feature = db.Column(db.String(100), nullable=True) # Used for bugs
    description = db.Column(db.Text, nullable=False)
    reproduction_steps = db.Column(db.Text, nullable=True) # Used for bugs
    status = db.Column(db.String(20), default='pending') # 'pending' or 'resolved'
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    resolved_at = db.Column(db.DateTime, nullable=True)

class UserNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
