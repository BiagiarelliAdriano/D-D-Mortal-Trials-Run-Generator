from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, Run, Character, User, HostedRun, SessionParticipant
from encounter_generator.encounter_logic import generate_all_encounters
from encounter_generator.generator import generate_divine_blessing
from encounter_generator.data.rules.classes import BARBARIAN, BARD, CLERIC, DRUID, FIGHTER, MONK, PALADIN, RANGER, ROGUE, SORCERER, WARLOCK, WIZARD
from encounter_generator.data.rules.backgrounds import BACKGROUNDS
from encounter_generator.data.rules.species import SPECIES
from encounter_generator.data.rules.feats import ORIGIN_FEATS, GENERAL_FEATS, FIGHTING_STYLE_FEATS, EPIC_BOONS
from encounter_generator.data.items import WEAPONS_DATA, ARMOR_DATA
from encounter_generator.data.spells import SPELLS
from encounter_generator.data.rules.spell_tables import FULL_CASTER_SLOTS, HALF_CASTER_SLOTS, THIRD_CASTER_SLOTS, PACT_MAGIC_SLOTS
from encounter_generator.data.rules.game_rules import WEAPON_MASTERY_OPTIONS
from encounter_generator.data.rules.feature_tables import SORCERER_METAMAGIC, WARLOCK_ELDRITCH_INVOCATIONS
import json
import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

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
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback-secret-dragon-horde-key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 604800 # 7 days in seconds

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

if os.environ.get("FLASK_ENV") != "production":
    with app.app_context():
        db.create_all()

# Configuration for uploads
UPLOAD_FOLDER = 'static/uploads/avatars'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
# Auth API
# ------------------------

@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.json
    if not data or not data.get("username") or not data.get("password") or not data.get("security_answer"):
        return jsonify({"error": "Missing required fields"}), 400
        
    username = data["username"].strip()
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken."}), 409
        
    user = User(
        username=username,
        avatar=data.get("avatar", "fighter"),
        security_question=data.get("security_question", "What is the name of your very first Dungeons & Dragons character?").strip()
    )
    user.set_password(data["password"])
    user.set_security_answer(data["security_answer"])
    
    # First user becomes admin automatically for testing/setup
    if User.query.count() == 0:
        user.is_admin = True
        
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "success": True,
        "token": access_token, 
        "user": {
            "id": user.id, 
            "username": user.username, 
            "avatar": user.avatar,
            "is_admin": user.is_admin
        }
    }), 201

@app.route("/api/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    
    # Return basic profile info + characters
    return jsonify({
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "is_admin": user.is_admin,
        "created_at": user.created_at.isoformat(),
        "characters": [{
            "id": c.id,
            "name": c.name,
            "level": c.get_data().get("level", 1),
            "class_name": c.get_data().get("class_name", "")
        } for c in user.characters]
    }), 200

@app.route("/api/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user_profile(user_id):
    current_user_id = get_jwt_identity()
    admin_user = User.query.get(current_user_id)
    
    # Check authorization: owner or admin
    if str(current_user_id) != str(user_id) and not admin_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    user = User.query.get_or_404(user_id)
    
    # Check if admin is trying to edit password/security answer of another user
    is_admin_editing_other = admin_user.is_admin and str(current_user_id) != str(user_id)
    
    # Handle Text Data (Multipart or JSON)
    username = request.form.get("username")
    password = request.form.get("password")
    security_question = request.form.get("security_question")
    security_answer = request.form.get("security_answer")
    
    if username:
        username = username.strip()
        existing = User.query.filter_by(username=username).first()
        if existing and existing.id != user.id:
            return jsonify({"error": "Username already taken"}), 409
        user.username = username
        
    if password:
        if is_admin_editing_other:
            return jsonify({"error": "Admins cannot change other users' passwords"}), 403
        if len(password) < 12:
            return jsonify({"error": "Password must be at least 12 characters long"}), 400
        user.set_password(password)

    if security_question:
        user.security_question = security_question.strip()
    
    if security_answer:
        if is_admin_editing_other:
            return jsonify({"error": "Admins cannot change other users' security answers"}), 403
        user.set_security_answer(security_answer.strip())
        
    # Handle Avatar Upload
    if 'avatar_file' in request.files:
        file = request.files['avatar_file']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{uuid.uuid4().hex}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Optimization: Resize and compress
            try:
                img = Image.open(file)
                # Convert to RGB if necessary (for RGBA/P to JPEG/WEBP compatibility)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                # Resize to max 600x600 while maintaining aspect ratio
                img.thumbnail((600, 600))
                img.save(filepath, optimize=True, quality=85)
                
                # Delete old custom avatar if it exists (Optional improvement)
                # if user.avatar.startswith('static/uploads/'): ...
                
                user.avatar = f"/{filepath}" # Store with leading slash for web access
            except Exception as e:
                return jsonify({"error": f"Image processing failed: {str(e)}"}), 500

    db.session.commit()
    
    return jsonify({
        "success": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "avatar": user.avatar,
            "is_admin": user.is_admin
        }
    }), 200

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing username or password"}), 400
        
    user = User.query.filter_by(username=data["username"].strip()).first()
    
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401
        
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "success": True,
        "token": access_token, 
        "user": {
            "id": user.id, 
            "username": user.username, 
            "avatar": user.avatar,
            "is_admin": user.is_admin
        }
    }), 200

@app.route("/api/auth/verify", methods=["GET"])
@jwt_required()
def verify_token():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    return jsonify({
        "success": True,
        "user": {
            "id": user.id, 
            "username": user.username, 
            "avatar": user.avatar,
            "is_admin": user.is_admin
        }
    }), 200

# ------------------------
# Admin API
# ------------------------

@app.route("/api/admin/system", methods=["GET"])
@jwt_required()
def admin_system():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    users = User.query.all()
    user_data = []
    for u in users:
        u_chars = [{
            "id": c.id,
            "name": c.name,
            "level": c.get_data().get("level", 1),
            "class_name": c.get_data().get("class_name", "")
        } for c in u.characters]
        
        user_data.append({
            "id": u.id,
            "username": u.username,
            "avatar": u.avatar,
            "is_admin": u.is_admin,
            "security_question": u.security_question,
            "character_count": len(u.characters),
            "characters": u_chars,
            "created_at": str(u.created_at)
        })
    
    total_characters = Character.query.count()
    
    return jsonify({
        "total_users": len(users),
        "total_characters": total_characters,
        "users": user_data
    }), 200

# ------------------------
# Character API (REST)
# ------------------------

@app.route("/api/characters", methods=["GET", "POST"])
@jwt_required()
def api_characters():
    current_user_id = get_jwt_identity()
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
            "xp": XP_THRESHOLDS.get(int(data.get("level", 1)), 0),
            "level_up_pending": True  # Show level up UI on fresh character
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

        character = Character(name=data.get("name"), user_id=current_user_id)
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
    characters = Character.query.filter_by(user_id=current_user_id).all()
    
    result = []
    for c in characters:
        active_run_title = None
        for link in c.session_links:
            if link.hosted_run and link.hosted_run.is_active:
                active_run_title = link.hosted_run.run.title_run
                break
                
        result.append({
            "id": c.id,
            "name": c.name,
            "level": c.get_data().get("level", 1),
            "class_name": c.get_data().get("class_name", ""),
            "subclass": c.get_data().get("subclass", ""),
            "species": c.get_data().get("species", ""),
            "species_variant": c.get_data().get("species_variant", ""),
            "active_run_title": active_run_title
        })
        
    return jsonify(result)

@app.route("/api/characters/<int:char_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def api_character_detail(char_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    character = Character.query.get_or_404(char_id)
    
    # Ownership Check (Bypass for Admin)
    if str(character.user_id) != str(current_user_id) and not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

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
@jwt_required()
def api_character_levelup(char_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    character = Character.query.get_or_404(char_id)
    
    if str(character.user_id) != str(current_user_id) and not user.is_admin:
        return jsonify({"error": "Unauthorized to level up this character"}), 403
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
    data["level_up_pending"] = True  # Trigger level up UI on frontend
    character.set_data(data)
    
    # Recalculate HP
    con_score = data.get("abilities", {}).get("constitution", 10)
    con_mod = (con_score - 10) // 2
    character.update_hp(next_level, con_mod, data.get("class_name", "Barbarian"))
    
    db.session.commit()
    return jsonify({"success": True, "new_level": next_level})

@app.route("/api/characters/<int:char_id>/leveldown", methods=["POST"])
@jwt_required()
def api_character_leveldown(char_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    character = Character.query.get_or_404(char_id)
    
    if str(character.user_id) != str(current_user_id) and not user.is_admin:
        return jsonify({"error": "Unauthorized to level down this character"}), 403
        
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

@app.route("/api/run/generate", methods=["GET"])
def api_generate_run():
    # Use 39 as the standard number of encounters from legacy code
    try:
        encounters = generate_all_encounters(39)
        blessing = generate_divine_blessing()
        
        # Format encounters for JSON (matching the legacy tuple-style indexing)
        formatted_encounters = []
        for i, enc in enumerate(encounters, 1):
            formatted_encounters.append([i, enc])
            
        return jsonify({
            "encounters": formatted_encounters,
            "divine_blessing": blessing
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

# ------------------------
# NEW JSON API for Runs
# ------------------------

@app.route("/api/runs", methods=["GET"])
@jwt_required(optional=True)
def api_list_runs():
    current_user_id = get_jwt_identity()
    if current_user_id:
        runs = Run.query.filter_by(user_id=current_user_id).all()
    else:
        # If not logged in, show runs with no user_id (public/anonymous)
        runs = Run.query.filter_by(user_id=None).all()
        
    return jsonify([{
        "id": r.id,
        "title": r.title_run,
        "created_at": r.created_at.isoformat(),
        "data": json.loads(r.data)
    } for r in runs]), 200

@app.route("/api/runs", methods=["POST"])
@jwt_required(optional=True)
def api_save_run():
    data = request.json
    if not data or not data.get("title") or not data.get("data"):
        return jsonify({"error": "Missing title or run data"}), 400
        
    current_user_id = get_jwt_identity()
    
    run = Run(
        title_run=data["title"],
        data=json.dumps(data["data"]),
        user_id=current_user_id
    )
    db.session.add(run)
    db.session.commit()
    
    return jsonify({
        "message": "Run saved successfully",
        "id": run.id
    }), 201

@app.route("/api/runs/<int:run_id>", methods=["DELETE"])
@jwt_required()
def api_delete_run_json(run_id):
    current_user_id = get_jwt_identity()
    run = Run.query.get_or_404(run_id)
    
    # Only the owner or an admin can delete
    is_admin = False
    admin_user = User.query.get(current_user_id)
    if admin_user:
        is_admin = admin_user.is_admin

    if str(run.user_id) != str(current_user_id) and not is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    db.session.delete(run)
    db.session.commit()
    return jsonify({"message": "Run deleted successfully"}), 200

@app.route("/api/rules/armor")
def api_rules_armor():
    return jsonify(ARMOR_DATA)

@app.route("/api/rules/options")
def api_rules_options():
    return jsonify({
        "weapon_mastery": WEAPON_MASTERY_OPTIONS,
        "metamagic": SORCERER_METAMAGIC,
        "invocations": WARLOCK_ELDRITCH_INVOCATIONS
    })

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
# RUN HOSTING API
# ------------------------

import random
import string

def generate_invite_code():
    """Generate a unique 6-digit alphanumeric code."""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        # Check if code already exists in an active session
        if not HostedRun.query.filter_by(invite_code=code, is_active=True).first():
            return code

@app.route("/api/host/create", methods=["POST"])
@jwt_required()
def api_create_hosted_run():
    data = request.json
    if not data or not data.get("run_id"):
        return jsonify({"error": "Missing run_id"}), 400
    
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    run = Run.query.get(data["run_id"])
    if not run:
        return jsonify({"error": "Run not found"}), 404

    invite_code = generate_invite_code()
    
    hosted_run = HostedRun(
        invite_code=invite_code,
        dm_id=current_user_id,
        run_id=run.id,
        party_inventory='[]'
    )
    db.session.add(hosted_run)
    db.session.flush() # Get ID before commit

    # Add DM as a participant
    dm_participant = SessionParticipant(
        user_id=current_user_id,
        hosted_run_id=hosted_run.id,
        role='DM'
    )
    db.session.add(dm_participant)
    db.session.commit()

    return jsonify({
        "message": "Session created successfully",
        "invite_code": invite_code,
        "session_id": hosted_run.id
    }), 201

@app.route("/api/host/join", methods=["POST"])
@jwt_required()
def api_join_hosted_run():
    data = request.json
    if not data or not data.get("invite_code"):
        return jsonify({"error": "Missing invite code"}), 400
    
    code = data["invite_code"].upper().strip()
    hosted_run = HostedRun.query.filter_by(invite_code=code, is_active=True).first()
    
    if not hosted_run:
        return jsonify({"error": "Session not found or inactive"}), 404
    
    current_user_id = get_jwt_identity()
    
    # Check if user is already a participant
    existing = SessionParticipant.query.filter_by(
        user_id=current_user_id, 
        hosted_run_id=hosted_run.id
    ).first()
    
    if existing:
        return jsonify({
            "message": "Already joined this session",
            "session_id": hosted_run.id
        }), 200

    # Max 5 players (DM counts as one? Or DM + 5? I'll assume 5 total for now)
    participant_count = SessionParticipant.query.filter_by(hosted_run_id=hosted_run.id).count()
    if participant_count >= 5:
        return jsonify({"error": "Session is full (Max 5 participants)"}), 400

    new_participant = SessionParticipant(
        user_id=current_user_id,
        hosted_run_id=hosted_run.id,
        role='Ascendant'
    )
    db.session.add(new_participant)
    db.session.commit()

    return jsonify({
        "message": "Joined session successfully",
        "session_id": hosted_run.id
    }), 201

@app.route("/api/host/active", methods=["GET"])
@jwt_required()
def api_list_active_hosted_runs():
    current_user_id = get_jwt_identity()
    
    # Get all active sessions where the user is a participant
    participations = SessionParticipant.query.filter_by(user_id=current_user_id).all()
    session_ids = [p.hosted_run_id for p in participations]
    
    sessions = HostedRun.query.filter(HostedRun.id.in_(session_ids), HostedRun.is_active == True).all()
    
    result = []
    for s in sessions:
        # Determine user role in this session
        role = next((p.role for p in participations if p.hosted_run_id == s.id), 'Ascendant')
        
        result.append({
            "id": s.id,
            "invite_code": s.invite_code,
            "dm_name": s.dm.username,
            "run_title": s.run.title_run,
            "role": role,
            "created_at": s.created_at.isoformat(),
            "participant_count": len(s.participants)
        })
    
    # Sort: Own DM games first
    result.sort(key=lambda x: x['role'] != 'DM')
    
    return jsonify(result), 200

@app.route("/api/host/details/<int:session_id>", methods=["GET"])
@jwt_required()
def api_get_hosted_run_details(session_id):
    current_user_id = get_jwt_identity()
    session = HostedRun.query.get_or_404(session_id)
    
    # Verify participant
    participant = SessionParticipant.query.filter_by(
        user_id=current_user_id, 
        hosted_run_id=session.id
    ).first()
    
    if not participant:
        return jsonify({"error": "Access denied. You are not a participant in this session."}), 403
    
    participants_info = []
    for p in session.participants:
        participants_info.append({
            "user_id": p.user.id,
            "username": p.user.username,
            "role": p.role,
            "character": {
                "id": p.character.id,
                "name": p.character.name,
                "data": p.character.get_data()
            } if p.character else None
        })

    return jsonify({
        "id": session.id,
        "invite_code": session.invite_code,
        "dm_id": session.dm_id,
        "run": {
            "id": session.run.id,
            "title": session.run.title_run,
            "data": json.loads(session.run.data)
        },
        "participants": participants_info,
        "party_inventory": json.loads(session.party_inventory),
        "completed_encounters": json.loads(session.completed_encounters),
        "is_active": session.is_active
    }), 200

@app.route("/api/host/<int:session_id>/link-character", methods=["POST"])
@jwt_required()
def api_link_character_to_session(session_id):
    current_user_id = get_jwt_identity()
    data = request.json
    if not data or not data.get("character_id"):
        return jsonify({"error": "Missing character_id"}), 400
    
    participant = SessionParticipant.query.filter_by(
        user_id=current_user_id, 
        hosted_run_id=session_id
    ).first()
    
    if not participant:
        return jsonify({"error": "You are not a participant in this session"}), 403
    
    character = Character.query.get(data["character_id"])
    if not character or str(character.user_id) != str(current_user_id):
        return jsonify({"error": "Character not found or not yours"}), 404
    
    participant.character_id = character.id
    db.session.commit()
    
    return jsonify({"message": "Character linked successfully"}), 200

@app.route("/api/host/<int:session_id>/rename", methods=["POST"])
@jwt_required()
def api_rename_hosted_run(session_id):
    current_user_id = get_jwt_identity()
    session = HostedRun.query.get_or_404(session_id)
    
    if str(session.dm_id) != str(current_user_id):
        return jsonify({"error": "Only the Dungeon Master can rename the run"}), 403
        
    data = request.json
    new_title = data.get("title")
    if not new_title:
        return jsonify({"error": "Missing title"}), 400
        
    session.run.title_run = new_title[:24].strip()
    db.session.commit()
    
    return jsonify({"message": "Run renamed successfully", "title": session.run.title_run}), 200

@app.route("/api/host/<int:session_id>/complete-encounter", methods=["POST"])
@jwt_required()
def api_complete_encounter(session_id):
    current_user_id = get_jwt_identity()
    session = HostedRun.query.get_or_404(session_id)
    
    if str(session.dm_id) != str(current_user_id):
        return jsonify({"error": "Only the Dungeon Master can complete encounters"}), 403
    
    data = request.json
    if not data or not data.get("encounter_num"):
        return jsonify({"error": "Missing encounter number"}), 400
    
    enc_num = str(data["encounter_num"])
    run_data = json.loads(session.run.data)
    
    # Find the encounter in the run data
    target_enc = None
    for num, enc in run_data["encounters"]:
        if str(num) == enc_num:
            target_enc = enc
            break
    
    if not target_enc:
        return jsonify({"error": "Encounter not found"}), 404
    
    # Logic to update party inventory if items/gold were found
    current_inv = json.loads(session.party_inventory)
    
    if "gold" in target_enc:
        current_inv.append(f"{target_enc['gold']} Gold")
    
    if "magic_items" in target_enc:
        for item in target_enc["magic_items"]:
            current_inv.append(item)
            
    session.party_inventory = json.dumps(current_inv)
    
    # Update completed encounters
    completed = json.loads(session.completed_encounters)
    if enc_num not in completed:
        completed.append(enc_num)
        session.completed_encounters = json.dumps(completed)
            
    db.session.commit()
    
    return jsonify({
        "message": f"Encounter {enc_num} completed",
        "party_inventory": current_inv
    }), 200

@app.route("/api/host/<int:session_id>/claim-item", methods=["POST"])
@jwt_required()
def api_claim_item(session_id):
    current_user_id = get_jwt_identity()
    data = request.json
    if not data or "item_index" not in data:
        return jsonify({"error": "Missing item index"}), 400
    
    session = HostedRun.query.get_or_404(session_id)
    participant = SessionParticipant.query.filter_by(
        user_id=current_user_id, 
        hosted_run_id=session.id
    ).first()
    
    if not participant:
        return jsonify({"error": "Access denied"}), 403
    
    inventory = json.loads(session.party_inventory)
    idx = data["item_index"]
    
    if idx < 0 or idx >= len(inventory):
        return jsonify({"error": "Item not found in vault"}), 404
    
    item = inventory.pop(idx)
    session.party_inventory = json.dumps(inventory)
    db.session.commit()
    
    return jsonify({
        "message": f"Claimed {item}",
        "party_inventory": inventory
    }), 200

# ------------------------
# Entry Point
# ------------------------

if __name__ == "__main__":
    app.run(debug=True)
