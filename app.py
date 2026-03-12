from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Run, Character
from encounter_generator.encounter_logic import generate_all_encounters
from encounter_generator.generator import generate_divine_blessing
from encounter_generator.data.rules.classes import BARBARIAN, BARD, CLERIC, DRUID, FIGHTER, MONK, PALADIN, RANGER, ROGUE, SORCERER, WARLOCK, WIZARD
from encounter_generator.data.rules.backgrounds import BACKGROUNDS
from encounter_generator.data.rules.species import SPECIES
from encounter_generator.data.rules.feats import ORIGIN_FEATS, GENERAL_FEATS, FIGHTING_STYLE_FEATS, EPIC_BOONS
from encounter_generator.data.items import WEAPONS_DATA, ARMOR_DATA
from encounter_generator.data.spells import SPELLS
from encounter_generator.data.rules.spell_tables import FULL_CASTER_SLOTS, HALF_CASTER_SLOTS, THIRD_CASTER_SLOTS, PACT_MAGIC_SLOTS
import json
import os

XP_THRESHOLDS = {
    1: 0,
    2: 300,
    3: 900,
    4: 2700,
    5: 6500,
    6: 14000,
    7: 23000,
    8: 34000,
    9: 48000,
    10: 64000,
    11: 85000,
    12: 100000,
    13: 120000,
    14: 140000,
    15: 165000,
    16: 195000,
    17: 225000,
    18: 265000,
    19: 305000,
    20: 355000
}

app = Flask(__name__)
CORS(app)

# Database config
uri = os.getenv("DATABASE_URL", "sqlite:///runs.db")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

if os.environ.get("FLASK_ENV") != "production":
    with app.app_context():
        db.create_all()

# ------------------------
# Basic Pages
# ------------------------

@app.route("/")
def home():
    return render_template("index.html")

CLASSES = {
    "barbarian": BARBARIAN,
    "bard": BARD,
    "cleric": CLERIC,
    "druid": DRUID,
    "fighter": FIGHTER,
    "monk": MONK,
    "paladin": PALADIN,
    "ranger": RANGER,
    "rogue": ROGUE,
    "sorcerer": SORCERER,
    "warlock": WARLOCK,
    "wizard": WIZARD
}

# ------------------------
# Class & Background API
# ------------------------

@app.route("/api/classes/<classname>")
def get_class(classname):
    cls = CLASSES.get(classname.lower())
    if cls:
        return jsonify(cls)
    return jsonify({"error": f"Class '{classname}' not found"}), 404

@app.route("/api/backgrounds")
def get_backgrounds():
    return jsonify(BACKGROUNDS)

@app.route("/api/species")
def get_species():
    return jsonify(SPECIES)

@app.route("/api/feats")
def get_feats():
    return jsonify({
        "origin": ORIGIN_FEATS,
        "general": GENERAL_FEATS,
        "fighting_style": FIGHTING_STYLE_FEATS,
        "epic_boon": EPIC_BOONS
    })

@app.route("/api/rules/weapons")
def get_weapons():
    return jsonify(WEAPONS_DATA)

# ------------------------
# Character API (REST)
# ------------------------

@app.route("/api/characters", methods=["GET", "POST"])
def api_characters():
    if request.method == "POST":
        data = request.form

        character_data = {
            "class_name": data.get("class_name"),
            "subclass": data.get("subclass"),
            "level": int(data.get("level", 1)),
            "abilities": json.loads(data.get("abilities", "{}")),
            "species": data.get("species"),
            "species_variant": data.get("species_variant"),
            "size": data.get("size"),
            "background": data.get("background"),
            "choices": json.loads(data.get("choices", "{}")),
            "xp": XP_THRESHOLDS.get(int(data.get("level", 1)), 0)
        }

        # Add Skill Proficiencies (Class + Background)
        prof_list = json.loads(data.get("proficiencies", "[]"))
        if prof_list:
            character_data["skillProficiencies"] = {s.lower().replace(" ", "_"): True for s in prof_list}

        # Initialize Inventory and Gold (Class + Background)
        # 1. Background Equipment
        bg_equip_choice = data.get("starting_equipment_choice", "standard") # Background choice
        bg_name = character_data["background"]
        background = next((bg for bg in BACKGROUNDS if bg["name"] == bg_name), None)
        
        starting_gold = 0
        starting_inventory = []

        def parse_equipment_string(item_input):
            # Handles "4 Handaxes", "Dagger", etc. OR {"name": "Dagger", "quantity": 1, ...}
            import re
            
            if isinstance(item_input, dict):
                qty = item_input.get("quantity", 1)
                name = item_input.get("name", "Unknown Item")
            else:
                match = re.match(r"^(\d+)\s+(.*)$", item_input.strip())
                if match:
                    qty = int(match.group(1))
                    name = match.group(2)
                else:
                    qty = 1
                    name = item_input.strip()
            
            # Simple category detection
            category = "Other"
            
            # Check for exact or singular match in WEAPONS_DATA
            check_name = name.strip()
            if check_name in WEAPONS_DATA:
                category = "Weapon"
            elif check_name.endswith('s') and check_name[:-1] in WEAPONS_DATA:
                category = "Weapon"
                name = check_name[:-1] # Normalize to singular for combat action matching
            elif any(k in name.lower() for k in ["armor", "leather", "mail", "plate"]):
                category = "Armor"
            elif any(k in name.lower() for k in ["pack", "kit", "rations", "torch", "rope"]):
                category = "Gear"

            return {"name": name, "quantity": qty, "category": category}

        if background and "starting_equipment" in background:
            if bg_equip_choice == "gold":
                starting_gold += background["starting_equipment"].get("gold_option", 50)
            else:
                starting_gold += background["starting_equipment"]["standard"].get("gold", 0)
                items = background["starting_equipment"]["standard"].get("items", [])
                starting_inventory.extend([parse_equipment_string(i) for i in items])

        # 2. Class Equipment
        class_name = character_data["class_name"]
        cls = CLASSES.get(class_name.lower())
        class_equip_choice = data.get("class_starting_equipment_choice", "option_a")

        if cls and "starting_equipment" in cls:
            choice = cls["starting_equipment"].get(class_equip_choice)
            if choice:
                starting_gold += choice.get("gold", 0)
                items = choice.get("items", [])
                starting_inventory.extend([parse_equipment_string(i) for i in items])

        character_data["gold"] = starting_gold
        character_data["inventory"] = starting_inventory

        character = Character(name=data.get("name"))
        character.set_data(character_data)

        # Initial HP Calculation
        con_score = character_data["abilities"].get("constitution", 10)
        con_mod = (con_score - 10) // 2
        character.update_hp(character_data["level"], con_mod, character_data["class_name"])

        try:
            db.session.add(character)
            db.session.commit()
            return jsonify({"id": character.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    # GET all characters
    characters = Character.query.all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "level": c.get_data().get("level", 1),
            "class_name": c.get_data().get("class_name", ""),
            "subclass": c.get_data().get("subclass", ""),
            "species": c.get_data().get("species", ""),
            "species_variant": c.get_data().get("species_variant", "")
        }
        for c in characters
    ])

@app.route("/api/characters/<int:char_id>", methods=["GET", "PUT", "DELETE"])
def api_character_detail(char_id):
    character = Character.query.get_or_404(char_id)

    if request.method == "DELETE":
        db.session.delete(character)
        db.session.commit()
        return jsonify({"success": True}), 204

    if request.method == "PUT":
        data = request.json or {}

        character.name = data.get("name", character.name)

        updated_data = character.get_data()
        
        # Check if we need to update HP (Level change)
        old_level = updated_data.get("level", 1)
        new_data = data.get("data", {})
        new_level = int(new_data.get("level", old_level))
        
        updated_data.update(new_data)
        character.set_data(updated_data) # Save basic updates first
        
        if new_level != old_level:
            abilities = updated_data.get("abilities", {})
            con_score = abilities.get("constitution", 10)
            con_mod = (con_score - 10) // 2
            character.update_hp(new_level, con_mod, updated_data.get("class_name", "Barbarian"))
            # Note: update_hp saves internally, so we don't need to call set_data again ideally, 
            # but update_hp calls set_data, so it's fine.

        db.session.commit()
        return jsonify({"success": True})

    # GET single character
    data = character.get_data()
    return jsonify({
        "id": character.id,
        "name": character.name,
        "level": data.get("level", 1),
        "class": {
            "name": data.get("class_name"),
            "subclass": data.get("subclass")
        },
        "data": data
    })

@app.route("/api/characters/<int:char_id>/levelup", methods=["POST"])
def api_character_levelup(char_id):
    character = Character.query.get_or_404(char_id)
    data = character.get_data()
    
    current_level = data.get("level", 1)
    if current_level >= 20:
        return jsonify({"error": "Character is already at max level"}), 400
        
    next_level = current_level + 1
    xp_required = XP_THRESHOLDS.get(next_level, 0)
    current_xp = data.get("xp", 0)
    
    if current_xp < xp_required:
        return jsonify({"error": f"Insufficient XP. Need {xp_required}, have {current_xp}"}), 400
        
    # Level up logic
    data["level"] = next_level
    character.set_data(data)
    
    # Recalculate HP
    con_score = data.get("abilities", {}).get("constitution", 10)
    con_mod = (con_score - 10) // 2
    character.update_hp(next_level, con_mod, data.get("class_name", "Barbarian"))
    
    db.session.commit()
    return jsonify({"success": True, "new_level": next_level})

@app.route("/api/characters/<int:char_id>/leveldown", methods=["POST"])
def api_character_leveldown(char_id):
    character = Character.query.get_or_404(char_id)
    data = character.get_data()
    
    current_level = data.get("level", 1)
    if current_level <= 1:
        return jsonify({"error": "Character is already at level 1"}), 400
        
    next_level = current_level - 1
    # Set XP to the threshold of the NEW level (or keep same, but usually leveling down resets to threshold)
    # The user said "and a user can modify... with an option to level down"
    # I'll set it to the threshold of the new level for a clean reset.
    data["level"] = next_level
    data["xp"] = XP_THRESHOLDS.get(next_level, 0)
    character.set_data(data)
    
    # Recalculate HP (models.py handles the truncation of rolls)
    con_score = data.get("abilities", {}).get("constitution", 10)
    con_mod = (con_score - 10) // 2
    character.update_hp(next_level, con_mod, data.get("class_name", "Barbarian"))
    
    db.session.commit()
    return jsonify({"success": True, "new_level": next_level})

# ------------------------
# Legacy HTML Routes (safe to remove later)
# ------------------------

@app.route("/characters-hub")
def characters_hub():
    characters = Character.query.all()
    return render_template("characters.html", characters=characters)

@app.route("/characters/<int:char_id>")
def view_character(char_id):
    character = Character.query.get_or_404(char_id)
    return render_template(
        "character_sheet.html",
        character=character,
        character_data=character.get_data(),
        editable=False
    )

@app.route("/characters/<int:char_id>/edit", methods=["GET", "POST"])
def edit_character(char_id):
    character = Character.query.get_or_404(char_id)

    if request.method == "POST":
        character.name = request.form.get("name")
        updated_data = {
            "class_name": request.form.get("class_name"),
            "subclass": request.form.get("subclass"),
            "level": int(request.form.get("level", 1))
        }
        character.set_data(updated_data)
        db.session.commit()
        return redirect(url_for("characters_hub"))

    return render_template("character_sheet.html", character=character, editable=True)

# ------------------------
# Run Generator
# ------------------------

@app.route("/run-generator", methods=["GET", "POST"])
def run_generator():
    if request.method == "POST":
        run_output = list(enumerate(generate_all_encounters(39), 1))
        blessing = generate_divine_blessing()
        return render_template(
            "run_generator.html",
            encounters=run_output,
            divine_blessing=blessing
        )

    return render_template("run_generator.html")

@app.route("/save", methods=["POST"])
def save():
    title_run = request.form.get("title")
    blessing = request.form.get("blessing")
    encounters = request.form.get("encounters")

    if title_run and blessing and encounters:
        run = Run(
            title_run=title_run,
            data=json.dumps({
                "blessing": json.loads(blessing),
                "encounters": json.loads(encounters)
            })
        )
        db.session.add(run)
        db.session.commit()

    return redirect(url_for("list_runs"))

@app.route("/runs")
def list_runs():
    runs = Run.query.all()
    return render_template("runs.html", runs=runs)

@app.route("/runs/<int:run_id>")
def view_run(run_id):
    run = Run.query.get_or_404(run_id)
    parsed = json.loads(run.data)
    return render_template(
        "run_generator.html",
        divine_blessing=parsed["blessing"],
        encounters=parsed["encounters"]
    )

@app.route("/runs/<int:run_id>/delete", methods=["POST"])
def delete_run(run_id):
    run = Run.query.get_or_404(run_id)
    db.session.delete(run)
    db.session.commit()
    return redirect(url_for("list_runs"))

@app.route("/api/rules/armor")
def api_rules_armor():
    return jsonify(ARMOR_DATA)

@app.route("/api/rules/spell_slots")
def api_rules_spell_slots():
    return jsonify({
        "full": FULL_CASTER_SLOTS,
        "half": HALF_CASTER_SLOTS,
        "third": THIRD_CASTER_SLOTS,
        "pact_magic": PACT_MAGIC_SLOTS
    })

@app.route("/api/spells/<classname>")
def get_spells(classname):
    class_spells = {}
    for level, spells_list in SPELLS.items():
        filtered_spells = []
        for spell in spells_list:
            if "classes" in spell and classname.capitalize() in spell["classes"]:
                filtered_spells.append({
                    "name": spell.get("name"),
                    "school": spell.get("school")
                })
        if filtered_spells:
            class_spells[level] = filtered_spells
    return jsonify(class_spells)

# ------------------------
# Entry Point
# ------------------------

if __name__ == "__main__":
    app.run(debug=True)
