from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from sqlalchemy.sql import func
from encounter_generator.data.rules.game_rules import CLASS_HIT_DICE

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
    "background": "",
    
    "hp_current": 0,
    "hp_max_base": 0,
    "hp_max_original": 0,
    "hp_modifier": 0,
    "hp_rolls": [],
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
    "gold": 0
}

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)

    def set_data(self, char_data):
        """
        Merge provided data with defaults and store as JSON.
        Supports deep merging for nested objects.
        """
        merged = json.loads(json.dumps(DEFAULT_CHARACTER_DATA)) # deep copy
        
        for key, value in char_data.items():
            if isinstance(value, dict) and key in merged:
                merged[key].update(value)
            else:
                merged[key] = value
        
        self.data = json.dumps(merged)

    def update_hp(self, new_level, con_mod, class_name):
        """
        Calculates and updates HP based on level, class, and constitution.
        Preserves existing rolls if level is unchanged or increased.
        """
        data = self.get_data()
        current_rolls = data.get("hp_rolls", [])
        
        hit_die = CLASS_HIT_DICE.get(class_name, 8) # Default to d8
        
        # If level < len(rolls), we might have down-leveled (truncate)
        # If level > len(rolls), we need to roll new dice
        
        # Level 1 is always max die
        if not current_rolls:
            current_rolls = [hit_die]
        
        # Adjust rolls list size
        if new_level > len(current_rolls):
            import random
            for _ in range(new_level - len(current_rolls)):
                 # Roll hit die (1 to hit_die)
                roll = random.randint(1, hit_die)
                current_rolls.append(roll)
        elif new_level < len(current_rolls):
            current_rolls = current_rolls[:new_level]
            
        # Calculate Max HP Base (without modifier)
        # Formula: Sum(rolls) + (Level * Con Mod)
        base_hp = sum(current_rolls)
        con_bonus = new_level * con_mod
        hp_max_base = base_hp + con_bonus
        
        # Update data
        data["hp_rolls"] = current_rolls
        data["hp_max_base"] = hp_max_base
        
        # Store original HP if not already set (first time calculation)
        if data.get("hp_max_original", 0) == 0:
            data["hp_max_original"] = hp_max_base
        
        # If current HP is 0 (new char), initialize to max
        if data.get("hp_current", 0) == 0:
            modifier = data.get("hp_modifier", 0)
            data["hp_current"] = hp_max_base + modifier
        
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