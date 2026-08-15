import math
import copy

from flask import Flask, request, render_template, redirect, url_for, jsonify
from datetime import datetime
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, Run, Character, User, HostedRun, SessionParticipant, RecoveryRequest, Report, UserNotification
from encounter_generator.encounter_logic import generate_all_encounters
from encounter_generator.generator import generate_divine_blessing
from encounter_generator.data.rules.classes import BARBARIAN, BARD, CLERIC, DRUID, FIGHTER, MONK, PALADIN, RANGER, ROGUE, SORCERER, WARLOCK, WIZARD
from encounter_generator.data.rules.multiclass_rules import check_multiclass_prerequisites
from encounter_generator.data.rules.backgrounds import BACKGROUNDS
from encounter_generator.data.rules.species import SPECIES
from encounter_generator.data.rules.feats import ORIGIN_FEATS, GENERAL_FEATS, FIGHTING_STYLE_FEATS, EPIC_BOONS
from encounter_generator.data.items import WEAPONS_DATA, ARMOR_DATA
from encounter_generator.data.spells import SPELLS
from encounter_generator.data.rules.spell_tables import FULL_CASTER_SLOTS, HALF_CASTER_SLOTS, THIRD_CASTER_SLOTS, PACT_MAGIC_SLOTS, MULTICLASS_CASTER_SLOTS
from encounter_generator.data.rules.game_rules import WEAPON_MASTERY_OPTIONS
from encounter_generator.data.rules.feature_tables import SORCERER_METAMAGIC, WARLOCK_ELDRITCH_INVOCATIONS
import json
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import uuid
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from PIL import Image
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from cryptography.fernet import Fernet
import base64
from hashlib import sha256

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

# ------------------------
# Shop Pricing System
# ------------------------

SHOP_CATEGORIES = ["Armor", "Potion", "Ring", "Rod", "Scroll", "Staff", "Wand", "Weapon"]

# Specific item prices (primarily common-tier items with individual costs)
SHOP_ITEM_PRICES = {
    # Common Armor
    "Breastplate": 400,
    "Chain Mail": 75,
    "Chain Shirt": 50,
    "Half Plate Armor": 750,
    "Hide Armor": 10,
    "Leather Armor": 10,
    "Padded Armor": 5,
    "Plate Armor": 1500,
    "Ring Mail": 30,
    "Scale Mail": 50,
    "Shield": 10,
    "Splint Armor": 200,
    "Studded Leather Armor": 45,
    # Common Potion
    "Potion of Climbing": 50,
    "Potion Of Climbing": 50,
    "Potion of Healing": 50,
    "Potion Of Healing": 50,
    # Common Ring
    "Ring Of Momentary Stillness": 50,
    # Common Rod
    "Rod Of Sudden Resistance": 50,
    # Common Staff
    "Staff Of Tactical Balance": 50,
    # Common Wand
    "Wand Of Minor Distortion": 50,
    # Common Weapons
    "Battleaxe": 10,
    "Club": 1,
    "Dagger": 2,
    "Flail": 10,
    "Glaive": 20,
    "Greataxe": 30,
    "Greatclub": 2,
    "Greatsword": 50,
    "Halberd": 20,
    "Hand Crossbow": 75,
    "Handaxe": 5,
    "Heavy Crossbow": 50,
    "Javelin": 5,
    "Lance": 10,
    "Light Crossbow": 25,
    "Light Hammer": 2,
    "Longbow": 50,
    "Longsword": 15,
    "Mace": 5,
    "Maul": 10,
    "Morningstar": 15,
    "Musket": 500,
    "Pike": 5,
    "Pistol": 250,
    "Quarterstaff": 2,
    "Rapier": 25,
    "Scimitar": 25,
    "Shortbow": 25,
    "Shortsword": 10,
    "Sickle": 1,
    "Sling": 1,
    "Spear": 1,
    "Trident": 5,
    "War Pick": 5,
    "Warhammer": 15,
    "Whip": 2,
}

# Rarity + Category default prices (non-common items without specific prices)
RARITY_CATEGORY_PRICES = {
    "common": {
        "Armor": 50, "Potion": 50, "Ring": 50, "Rod": 50,
        "Scroll": 40, "Staff": 50, "Wand": 50, "Weapon": 10,
        "Wondrous": 100,
    },
    "uncommon": {
        "Armor": 400, "Potion": 200, "Ring": 400, "Rod": 400,
        "Scroll": 200, "Staff": 400, "Wand": 400, "Weapon": 400,
        "Wondrous": 800,
    },
    "rare": {
        "Armor": 4000, "Potion": 2000, "Ring": 4000, "Rod": 4000,
        "Scroll": 2000, "Staff": 4000, "Wand": 4000, "Weapon": 4000,
        "Wondrous": 8000,
    },
    "very rare": {
        "Armor": 40000, "Potion": 20000, "Ring": 40000, "Rod": 40000,
        "Scroll": 20000, "Staff": 40000, "Wand": 40000, "Weapon": 40000,
        "Wondrous": 80000,
    },
    "legendary": {
        "Armor": 400000, "Potion": 200000, "Ring": 400000, "Rod": 400000,
        "Scroll": 200000, "Staff": 400000, "Wand": 400000, "Weapon": 400000,
        "Wondrous": 800000,
    },
}

def get_item_price(item_name, rarity, category):
    """Return the gold cost for a shop item."""
    # Check specific item price first
    if item_name in SHOP_ITEM_PRICES:
        return SHOP_ITEM_PRICES[item_name]
    # Pattern-match scrolls (format: "Spell Scroll Cantrip <spell>" or "Spell Scroll Level N <spell>")
    if category == "Scroll" or (item_name.startswith("Spell Scroll")):
        name_lower = item_name.lower()
        if "cantrip" in name_lower:
            return 30
        if "level 1 " in name_lower or "1st" in name_lower:
            return 50
        # Higher spell-level scrolls → use rarity default
    # Fall back to rarity + category default
    return RARITY_CATEGORY_PRICES.get(rarity, {}).get(category, 10)

def get_item_sell_price(item_name, rarity, category):
    """
    Determines the amount of gold a player receives when selling an item.
    Common items sell for full price.
    All other rarities sell for half price.
    """
    buy_price = get_item_price(item_name, rarity, category)
    if (rarity or "common").lower() == "common":
        return buy_price

    return max(1, buy_price // 2)

def determine_item_rarity(item_name, category, possible_rarities):
    """Detect which rarity pool an item belongs to by lookup."""
    from encounter_generator.data.items import MAGIC_ITEMS as _MI, WONDROUS_ITEMS as _WI
    for r in possible_rarities:
        # Check standard categories
        cat_items = _MI.get(r, {}).get(category, [])
        if item_name in cat_items:
            return r
        # Check Wondrous categories (Arcana, Armaments, Implements, Relics)
        if category == "Wondrous":
            for w_cat in ["Arcana", "Armaments", "Implements", "Relics"]:
                if item_name in _WI.get(r, {}).get(w_cat, []):
                    return r
    return possible_rarities[0]  # fallback to first rarity

def generate_common_shop_items():
    """Build the always-available common items list with prices."""
    from encounter_generator.data.items import MAGIC_ITEMS as _MI
    from encounter_generator.generator import generate_scroll_for_rarity
    common = _MI.get("common", {})
    result = {}
    for category in SHOP_CATEGORIES:
        raw_list = common.get(category, [])
        priced = []
        for item_name in raw_list:
            if item_name == "generate":
                # For scrolls, generate 3 representative options
                generated = set()
                attempts = 0
                while len(generated) < 3 and attempts < 20:
                    generated.add(generate_scroll_for_rarity("common"))
                    attempts += 1
                for scroll_name in sorted(generated):
                    priced.append({"name": scroll_name, "cost": get_item_price(scroll_name, "common", "Scroll")})
            elif item_name == "enspelled":
                continue  # skip enspelled in common (safety)
            else:
                priced.append({"name": item_name, "cost": get_item_price(item_name, "common", category)})
        if priced:
            result[category] = priced
    return result

def get_spellcasting_progression(class_data):
    """
    Returns the spellcasting progression for a class or None if it has no spellcasting.
    """
    if not class_data:
        return None

    spellcasting = class_data.get("spellcasting")
    if spellcasting:
        return spellcasting.get("progression")

    return None

def get_spellcasting_classes(character_data):
    """
    Returns all classes that contribute spellcasting.
    """
    
    spellcasting_classes = []
    for class_entry in character_data.get("class_levels", []):
        class_name = class_entry.get("class_name", "").lower()
        class_data = CLASSES.get(class_name)
        if not class_data:
            continue
        progression = None
        
        # Normal spellcasting
        if class_data.get("spellcasting"):
            progression = class_data["spellcasting"].get("progression")
        
        # Subclass spellcasting
        if not progression:
            subclass_name = class_entry.get("subclass", "").lower()
            subclass_data = (
                class_data
                .get("subclasses", {})
                .get(subclass_name)
            )
            if subclass_data:
                for feature_levels in subclass_data.get("features", {}).values():
                    for feature in feature_levels:
                        feature_id = feature.get("id", "")
                        if (
                            feature_id.startswith("eldritch_knight_spellcasting")
                            or feature_id.startswith("arcane_trickster_spellcasting")
                        ):
                            progression = (
                                feature
                                .get("details", {})
                                .get("progression")
                            )
        if progression:
            spellcasting_classes.append({
                "class_entry": class_entry,
                "progression": progression
            })
    return spellcasting_classes

def calculate_multiclass_caster_level(character_data):
    """
    Calculates effective caster level for multiclass spell slots.

    Uses:
    - Full casters: full levels
    - Half casters: half levels (rounded down)
    - Third casters: one third levels (rounded down)

    Includes subclass spellcasting such as:
    - Eldritch Knight
    - Arcane Trickster
    """

    class_levels = character_data.get("class_levels", [])

    caster_level = 0
    has_pact_magic = False

    for class_entry in class_levels:

        class_name = class_entry.get("class_name", "").lower()
        class_level = class_entry.get("level", 0)

        class_data = CLASSES.get(class_name)

        if not class_data:
            continue


        progression = None


        # Check normal class spellcasting
        if class_data.get("spellcasting"):
            progression = class_data["spellcasting"].get("progression")


        # Check subclass spellcasting
        subclass_name = class_entry.get("subclass", "").lower()

        if subclass_name and not progression:

            subclass_data = (
                class_data
                .get("subclasses", {})
                .get(subclass_name)
            )

            if subclass_data:

                for feature_levels in subclass_data.get("features", {}).values():

                    for feature in feature_levels:

                        if (
                            feature.get("id", "").startswith("eldritch_knight_spellcasting")
                            or feature.get("id", "").startswith("arcane_trickster_spellcasting")
                        ):
                            progression = feature.get("details", {}).get("progression")


        if progression == "full":
            caster_level += class_level

        elif progression == "half":
            caster_level += math.ceil(class_level / 2)

        elif progression == "third":
            caster_level += math.ceil(class_level / 3)

        elif progression in ["pact", "pact_magic"]:
            has_pact_magic = True


    return {
        "caster_level": caster_level,
        "has_pact_magic": has_pact_magic
    }

def calculate_spell_slots(character_data):
    """
    Determines spell slots.
    Returns:
    {
        "spellcasting": {},
        "pact_magic": {}
    }
    """
    spellcasting_classes = get_spellcasting_classes(character_data)
    if not spellcasting_classes:
        return {}
    spellcasting_slots = {}
    pact_slots = {}
    normal_caster_level = 0
    pact_classes = []
    for caster in spellcasting_classes:
        class_entry = caster["class_entry"]
        progression = caster["progression"]
        class_level = class_entry.get("level", 0)
        if progression == "pact":
            pact_classes.append(
                {
                    "level": class_level
                }
            )
        elif progression == "full":
            normal_caster_level += class_level
        elif progression == "half":
            normal_caster_level += math.ceil(class_level / 2)
        elif progression == "third":
            normal_caster_level += math.ceil(class_level / 3)

    # Normal multiclass spellcasting
    if normal_caster_level > 0:
        spellcasting_slots = MULTICLASS_CASTER_SLOTS.get(
            normal_caster_level,
            {}
        )

    # Warlock Pact Magic
    # There can only be one Warlock class
    if pact_classes:
        pact_level = pact_classes[0]["level"]
        pact_slots = PACT_MAGIC_SLOTS.get(
            pact_level,
            {}
        )
    result = {}
    if spellcasting_slots:
        result["spellcasting"] = spellcasting_slots
    if pact_slots:
        result["pact_magic"] = pact_slots
    return result

load_dotenv()
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)
app = Flask(__name__)
CORS(app)

# Database config
uri = os.getenv("DATABASE_URL", "sqlite:///runs.db")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 604800 # 7 days in seconds

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# ------------------------
# Encryption Setup for Recovery
# ------------------------
RECOVERY_KEY_SALT = os.getenv("RECOVERY_KEY_SALT")

def get_fernet(master_key):
    """Derive a Fernet key from the master key string."""
    key = sha256((master_key + RECOVERY_KEY_SALT).encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

# Fallback master key for initial encryption (stored in ENV)
# In a real production app, this should be very secure.
SYSTEM_RECOVERY_MASTER = os.getenv("SYSTEM_RECOVERY_MASTER")

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
        avatar=data.get("avatar", ""),
        discord_id=data.get("discord_id", "").strip() or None,
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
            "discord_id": user.discord_id,
            "is_admin": user.is_admin,
            "patreon_connected": user.patreon_connected,
            "patreon_tier": user.patreon_tier,
            "has_unlimited_access": user.has_unlimited_access()
        }
    }), 201


@app.route("/api/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_profile(user_id):
    user = db.get_or_404(User, user_id)
    
    current_user_id = get_jwt_identity()
    if str(current_user_id) == str(user_id):
        sync_patreon_status(user)
        
    return jsonify({
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "is_admin": user.is_admin,
        "created_at": user.created_at.isoformat(),
        "patreon_connected": user.patreon_connected,
        "patreon_tier": user.patreon_tier,
        "has_unlimited_access": user.has_unlimited_access(),
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
    admin_user = db.session.get(User, current_user_id)
    
    # Check authorization: owner or admin
    if str(current_user_id) != str(user_id) and not admin_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    user = db.get_or_404(User, user_id)
    
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
            try:
                upload_result = cloudinary.uploader.upload(
                    file,
                    folder="mortal_trials/avatars",
                    transformation=[
                        {
                            "width": 600,
                            "height": 600,
                            "crop": "limit",
                            "quality": "auto"
                        }
                    ]
                )
                user.avatar = upload_result["secure_url"]
            except Exception as e:
                return jsonify({"error": f"Image processing failed: {str(e)}"}), 500

    db.session.commit()
    
    return jsonify({
        "success": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "avatar": user.avatar,
            "is_admin": user.is_admin,
            "patreon_connected": user.patreon_connected,
            "patreon_tier": user.patreon_tier,
            "has_unlimited_access": user.has_unlimited_access()
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
    
    # If the frontend sends a security answer (new device / expired session), validate it
    security_answer = data.get("security_answer")
    if security_answer is not None:
        if not user.check_security_answer(security_answer):
            return jsonify({"error": "Incorrect security answer. Access denied."}), 401
        
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "success": True,
        "token": access_token, 
        "user": {
            "id": user.id, 
            "username": user.username, 
            "avatar": user.avatar,
            "is_admin": user.is_admin,
            "patreon_connected": user.patreon_connected,
            "patreon_tier": user.patreon_tier,
            "has_unlimited_access": user.has_unlimited_access()
        }
    }), 200

def sync_patreon_status(user, force=False):
    import requests
    from datetime import datetime, timedelta
    
    if not user.patreon_connected or not user.patreon_access_token:
        return
        
    now = datetime.utcnow()
    # Check if checked in the last 24 hours, unless force=True
    if not force and user.patreon_last_checked:
        if (now - user.patreon_last_checked) < timedelta(hours=24):
            return
            
    campaign_id = os.getenv("PATREON_CAMPAIGN_ID")
    if not campaign_id:
        return
        
    def fetch_data(token):
        url = "https://www.patreon.com/api/oauth2/v2/identity"
        params = {
            "include": "memberships,memberships.currently_entitled_tiers,memberships.campaign",
            "fields[member]": "patron_status",
            "fields[tier]": "title"
        }
        headers = {
            "Authorization": f"Bearer {token}"
        }
        return requests.get(url, params=params, headers=headers)
        
    try:
        resp = fetch_data(user.patreon_access_token)
        
        # If expired (401), try refresh
        if resp.status_code == 401 and user.patreon_refresh_token:
            refresh_data = {
                "grant_type": "refresh_token",
                "refresh_token": user.patreon_refresh_token,
                "client_id": os.getenv("PATREON_CLIENT_ID"),
                "client_secret": os.getenv("PATREON_CLIENT_SECRET")
            }
            refresh_headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            refresh_resp = requests.post("https://www.patreon.com/api/oauth2/token", data=refresh_data, headers=refresh_headers)
            if refresh_resp.status_code == 200:
                tokens = refresh_resp.json()
                user.patreon_access_token = tokens.get("access_token")
                user.patreon_refresh_token = tokens.get("refresh_token")
                db.session.add(user)
                db.session.commit()
                # Retry call with new access token
                resp = fetch_data(user.patreon_access_token)
            else:
                user.patreon_connected = False
                user.patreon_tier = None
                user.patreon_access_token = None
                user.patreon_refresh_token = None
                user.patreon_last_checked = now
                db.session.add(user)
                db.session.commit()
                return
                
        if resp.status_code == 200:
            json_data = resp.json()
            included = json_data.get("included", [])
            active_member_obj = None
            
            for item in included:
                if item.get("type") == "member":
                    campaign_rel = item.get("relationships", {}).get("campaign", {}).get("data", {})
                    if campaign_rel and campaign_rel.get("id") == campaign_id:
                        if item.get("attributes", {}).get("patron_status") == "active_patron":
                            active_member_obj = item
                            break
                            
            if active_member_obj:
                tier_ids = []
                tiers_data = active_member_obj.get("relationships", {}).get("currently_entitled_tiers", {}).get("data", [])
                for t in tiers_data:
                    if t.get("type") == "tier":
                        tier_ids.append(t.get("id"))
                        
                tier_title = None
                if tier_ids:
                    for item in included:
                        if item.get("type") == "tier" and item.get("id") in tier_ids:
                            title = item.get("attributes", {}).get("title")
                            if title:
                                tier_title = title
                                break
                if not tier_title:
                    tier_title = "Patreon Supporter"
                user.patreon_tier = tier_title
            else:
                user.patreon_tier = None
                
            user.patreon_last_checked = now
            db.session.add(user)
            db.session.commit()
        elif resp.status_code in (403, 401):
            user.patreon_connected = False
            user.patreon_tier = None
            user.patreon_access_token = None
            user.patreon_refresh_token = None
            user.patreon_last_checked = now
            db.session.add(user)
            db.session.commit()
    except Exception as e:
        print(f"Error syncing Patreon status for user {user.id}: {e}")

@app.route("/api/auth/access-status", methods=["GET"])
@jwt_required()
def access_status():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    sync_patreon_status(user)
    
    return jsonify({
        "has_unlimited_access": user.has_unlimited_access(),
        "patreon_connected": user.patreon_connected,
        "patreon_tier": user.patreon_tier
    }), 200

@app.route("/auth/patreon")
def patreon_auth():
    token = request.args.get("token")
    if not token:
        return "Missing token", 400
        
    try:
        from flask_jwt_extended import decode_token
        decoded = decode_token(token)
        user_id = decoded["sub"]
    except Exception as e:
        return "Invalid or expired token", 401
        
    user = db.session.get(User, user_id)
    if not user:
        return "User not found", 404
        
    from itsdangerous import URLSafeTimedSerializer
    serializer = URLSafeTimedSerializer(app.config["JWT_SECRET_KEY"])
    state = serializer.dumps({"user_id": user.id})
    
    client_id = os.getenv("PATREON_CLIENT_ID")
    scheme = request.headers.get("X-Forwarded-Proto", request.scheme)
    redirect_uri = f"{scheme}://{request.host}/auth/patreon/callback"
    
    patreon_auth_url = (
        f"https://www.patreon.com/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope=identity identity.memberships"
        f"&state={state}"
    )
    return redirect(patreon_auth_url)

@app.route("/auth/patreon/callback")
def patreon_callback():
    code = request.args.get("code")
    state = request.args.get("state")
    
    if not code or not state:
        return "Authorization code or state missing from request.", 400
        
    from itsdangerous import URLSafeTimedSerializer
    serializer = URLSafeTimedSerializer(app.config["JWT_SECRET_KEY"])
    try:
        data = serializer.loads(state, max_age=600)
        user_id = data["user_id"]
    except Exception as e:
        return "Invalid or expired authorization state.", 400
        
    user = db.session.get(User, user_id)
    if not user:
        return "User not found.", 404
        
    client_id = os.getenv("PATREON_CLIENT_ID")
    client_secret = os.getenv("PATREON_CLIENT_SECRET")
    scheme = request.headers.get("X-Forwarded-Proto", request.scheme)
    redirect_uri = f"{scheme}://{request.host}/auth/patreon/callback"
    
    token_url = "https://www.patreon.com/api/oauth2/token"
    payload = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        import requests
        resp = requests.post(token_url, data=payload, headers=headers)
        if resp.status_code != 200:
            return f"Error exchanging code with Patreon: {resp.text}", 400
            
        token_data = resp.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        
        user.patreon_connected = True
        user.patreon_access_token = access_token
        user.patreon_refresh_token = refresh_token
        
        sync_patreon_status(user, force=True)
        
        db.session.commit()
        
        html_success = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Patreon Connected Successfully</title>
            <script>
                if (window.opener) {{
                    window.opener.postMessage({{
                        success: true,
                        patreon_connected: true,
                        patreon_tier: {json.dumps(user.patreon_tier)}
                    }}, "*");
                }}
                window.close();
            </script>
        </head>
        <body>
            <p>Patreon connected successfully! You may close this window.</p>
        </body>
        </html>
        """
        return html_success
    except Exception as e:
        return f"Error completing Patreon authorization: {str(e)}", 500

@app.route("/api/auth/patreon/disconnect", methods=["POST"])
@jwt_required()
def patreon_disconnect():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    user.patreon_id = None
    user.patreon_connected = False
    user.patreon_tier = None
    user.patreon_access_token = None
    user.patreon_refresh_token = None
    user.patreon_last_checked = None
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "user": {
            "patreon_connected": False,
            "patreon_tier": None,
            "has_unlimited_access": user.has_unlimited_access()
        }
    }), 200

@app.route("/api/auth/patreon/refresh-status", methods=["POST"])
@jwt_required()
def patreon_refresh_status():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    if not user.patreon_connected or not user.patreon_access_token:
        return jsonify({"error": "Patreon not connected"}), 400
        
    sync_patreon_status(user, force=True)
    
    return jsonify({
        "success": True,
        "patreon_connected": user.patreon_connected,
        "patreon_tier": user.patreon_tier,
        "has_unlimited_access": user.has_unlimited_access()
    }), 200

@app.route("/api/auth/verify", methods=["GET"])
@jwt_required()
def verify_token():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    sync_patreon_status(user)
        
    return jsonify({
        "success": True,
        "user": {
            "id": user.id, 
            "username": user.username, 
            "avatar": user.avatar,
            "is_admin": user.is_admin,
            "patreon_connected": user.patreon_connected,
            "patreon_tier": user.patreon_tier,
            "has_unlimited_access": user.has_unlimited_access()
        }
    }), 200

@app.route("/api/admin/reset-my-security-answer", methods=["POST"])
def reset_my_security_answer():
    data = request.get_json()

    if not data or not data.get("username"):
        return jsonify({"error": "Username is required"}), 400

    username = data["username"].strip()
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Only allow administrators to use this temporary endpoint.
    if not user.is_admin:
        return jsonify({"error": "Administrator access required"}), 403

    data = request.get_json()

    if not data or not data.get("security_answer"):
        return jsonify({"error": "A new security answer is required"}), 400

    new_security_answer = data["security_answer"].strip()

    if not new_security_answer:
        return jsonify({"error": "Security answer cannot be empty"}), 400

    # Hash the new security answer using the same method
    # used when security answers are normally created.
    user.security_answer_hash = generate_password_hash(new_security_answer)

    db.session.commit()

    return jsonify({
        "message": "Security answer successfully reset."
    }), 200

@app.route("/api/auth/security-question", methods=["GET"])
def get_security_question():
    """Public endpoint: returns a user's security question text by username.
    Never reveals the answer or any sensitive data."""
    username = request.args.get("username", "").strip()
    if not username:
        return jsonify({"error": "Username required"}), 400
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"security_question": user.security_question}), 200

# ------------------------
# Admin API
# ------------------------

@app.route("/api/admin/system", methods=["GET"])
@jwt_required()
def admin_system():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    
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
# Recovery API
# ------------------------

@app.route("/api/auth/recovery-request", methods=["POST"])
def create_recovery_request():
    data = request.json
    if not data or not data.get("username") or not data.get("request_type"):
        return jsonify({"error": "Missing username or request type"}), 400
        
    username = data["username"].strip()
    request_type = data["request_type"] # 'username', 'password', 'security_answer'
    
    if request_type not in ['username', 'password', 'security_answer']:
        return jsonify({"error": "Invalid request type"}), 400
        
    user = User.query.filter_by(username=username).first()
    
    # We create the request even if the user isn't found (to prevent enumeration via timing/response)
    # But we link it if found.
    new_request = RecoveryRequest(
        username=username,
        user_id=user.id if user else None,
        request_type=request_type
    )
    
    db.session.add(new_request)
    
    # Notify all admins about the new recovery request
    admins = User.query.filter_by(is_admin=True).all()
    for admin in admins:
        notif = UserNotification(
            user_id=admin.id,
            message=f"New Account Recovery Request ({request_type}) submitted for username: {username}."
        )
        db.session.add(notif)
        
    db.session.commit()
    
    return jsonify({"success": True, "message": "Request submitted. Contact the Admin for further steps."}), 201

@app.route("/api/admin/recovery-requests", methods=["POST"])
@jwt_required()
def get_recovery_requests():
    current_user_id = get_jwt_identity()
    admin = db.session.get(User, current_user_id)
    if not admin or not admin.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    data = request.json
    master_key = data.get("master_key")
    if not master_key or master_key != SYSTEM_RECOVERY_MASTER:
        return jsonify({"error": "Invalid Master Key"}), 401
        
    requests = RecoveryRequest.query.filter_by(status='pending').all()
    
    result = []
    for r in requests:
        user_info = None
        if r.user:
            user_info = {
                "id": r.user.id,
                "username": r.user.username,
                "discord_id": r.user.discord_id,
                "security_question": r.user.security_question
            }
            
        result.append({
            "id": r.id,
            "provided_username": r.username,
            "request_type": r.request_type,
            "created_at": r.created_at.isoformat(),
            "user_info": user_info
        })
        
    return jsonify(result), 200

@app.route("/api/admin/recovery-resolve", methods=["POST"])
@jwt_required()
def resolve_recovery_request():
    current_user_id = get_jwt_identity()
    admin = db.session.get(User, current_user_id)
    if not admin or not admin.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    data = request.json
    request_id = data.get("request_id")
    action = data.get("action") # 'approve', 'deny'
    master_key = data.get("master_key")
    
    if master_key != SYSTEM_RECOVERY_MASTER:
         return jsonify({"error": "Invalid Master Key"}), 401
         
    recovery_req = db.session.get(RecoveryRequest, request_id)
    if not recovery_req:
        return jsonify({"error": "Request not found"}), 404
        
    response_data = {"success": True}
    
    if action == 'approve':
        import secrets
        from datetime import datetime, timedelta
        code = secrets.token_hex(4).upper()
        recovery_req.recovery_code = code
        recovery_req.code_expires_at = datetime.utcnow() + timedelta(hours=24)
        recovery_req.status = 'approved'
        response_data["recovery_code"] = code
    elif action == 'deny':
        recovery_req.status = 'denied'
    else:
        return jsonify({"error": "Invalid action"}), 400
        
    recovery_req.resolved_at = func.now()
    db.session.commit()
    
    return jsonify(response_data), 200

@app.route("/api/auth/verify-security-answer", methods=["POST"])
def verify_security_answer():
    data = request.json
    if not data or not data.get("username") or not data.get("security_answer"):
        return jsonify({"error": "Username and security answer required"}), 400
        
    user = User.query.filter_by(username=data["username"].strip()).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    if not user.security_question:
        return jsonify({"error": "This account does not have a security question configured"}), 400
        
    if not user.check_security_answer(data["security_answer"]):
        return jsonify({"error": "Incorrect security answer"}), 401
        
    from datetime import timedelta
    reset_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(minutes=5),
        additional_claims={"is_recovery": True}
    )
    return jsonify({"success": True, "reset_token": reset_token}), 200

@app.route("/api/auth/redeem-recovery", methods=["POST"])
def redeem_recovery():
    data = request.json
    if not data or not data.get("username") or not data.get("recovery_code"):
        return jsonify({"error": "Username and recovery code required"}), 400
        
    user = User.query.filter_by(username=data["username"].strip()).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    from datetime import datetime
    req = RecoveryRequest.query.filter_by(
        user_id=user.id,
        recovery_code=data["recovery_code"].strip().upper(),
        status='approved'
    ).first()
    
    if not req:
        return jsonify({"error": "Invalid or inactive recovery code"}), 400
        
    if req.code_expires_at and req.code_expires_at < datetime.utcnow():
        return jsonify({"error": "Recovery code has expired"}), 400
        
    from datetime import timedelta
    reset_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(minutes=5),
        additional_claims={"is_recovery": True}
    )
    
    req.status = 'resolved'
    req.resolved_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({"success": True, "reset_token": reset_token}), 200

@app.route("/api/auth/reset-credentials", methods=["POST"])
@jwt_required()
def reset_credentials():
    from flask_jwt_extended import get_jwt
    claims = get_jwt()
    if not claims.get("is_recovery"):
        return jsonify({"error": "Unauthorized credential reset attempt"}), 403
        
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    data = request.json
    new_password = data.get("new_password")
    new_security_question = data.get("new_security_question")
    new_security_answer = data.get("new_security_answer")
    
    if not new_password and not new_security_answer:
        return jsonify({"error": "Nothing to reset"}), 400
        
    if new_password:
        if len(new_password) < 12:
            return jsonify({"error": "Password must be at least 12 characters long"}), 400
        user.set_password(new_password)
        
    if new_security_question and new_security_answer:
        user.security_question = new_security_question.strip()
        user.set_security_answer(new_security_answer.strip())
        
    db.session.commit()
    return jsonify({"success": True, "message": "Credentials updated successfully"}), 200


# ------------------------
# Reports & Notifications API
# ------------------------

@app.route("/api/reports", methods=["POST"])
@jwt_required()
def api_create_report():
    current_user_id = get_jwt_identity()
    data = request.json
    
    report_type = data.get("report_type")
    description = data.get("description")
    
    if not report_type or not description:
        return jsonify({"error": "Missing required fields"}), 400
        
    report = Report(
        user_id=current_user_id,
        report_type=report_type,
        feature=data.get("feature"),
        description=description,
        reproduction_steps=data.get("reproduction_steps")
    )
    db.session.add(report)
    
    # Notify all admins about the new report
    admins = User.query.filter_by(is_admin=True).all()
    user_who_reported = db.session.get(User, current_user_id)
    username = user_who_reported.username if user_who_reported else "A user"
    for admin in admins:
        notif = UserNotification(
            user_id=admin.id,
            message=f"New {report_type} submitted by {username}."
        )
        db.session.add(notif)
        
    db.session.commit()
    return jsonify({"success": True, "message": "Report submitted successfully."}), 201

@app.route("/api/admin/reports", methods=["GET"])
@jwt_required()
def api_admin_get_reports():
    current_user_id = get_jwt_identity()
    admin = db.session.get(User, current_user_id)
    if not admin or not admin.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    reports = Report.query.order_by(Report.created_at.desc()).all()
    result = []
    for r in reports:
        result.append({
            "id": r.id,
            "username": r.user.username,
            "report_type": r.report_type,
            "feature": r.feature,
            "description": r.description,
            "reproduction_steps": r.reproduction_steps,
            "status": r.status,
            "created_at": r.created_at.isoformat(),
            "resolved_at": r.resolved_at.isoformat() if r.resolved_at else None
        })
    return jsonify(result), 200

@app.route("/api/admin/reports/<int:report_id>/resolve", methods=["POST"])
@jwt_required()
def api_admin_resolve_report(report_id):
    current_user_id = get_jwt_identity()
    admin = db.session.get(User, current_user_id)
    if not admin or not admin.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    report = db.get_or_404(Report, report_id)
    data = request.json
    reply_message = data.get("message")
    
    if not reply_message:
        return jsonify({"error": "Missing reply message"}), 400
        
    report.status = "resolved"
    report.resolved_at = func.now()
    
    notification = UserNotification(
        user_id=report.user_id,
        message=f"Admin reply regarding your {report.report_type} report: {reply_message}"
    )
    db.session.add(notification)
    db.session.commit()
    return jsonify({"success": True, "message": "Report resolved and notification sent."}), 200

@app.route("/api/users/notifications", methods=["GET"])
@jwt_required()
def api_get_notifications():
    current_user_id = get_jwt_identity()
    notifications = UserNotification.query.filter_by(user_id=current_user_id, is_read=False).all()
    result = []
    for n in notifications:
        result.append({
            "id": n.id,
            "message": n.message,
            "created_at": n.created_at.isoformat()
        })
    return jsonify(result), 200

@app.route("/api/users/notifications/<int:notification_id>/read", methods=["POST"])
@jwt_required()
def api_mark_notification_read(notification_id):
    current_user_id = get_jwt_identity()
    notification = db.get_or_404(UserNotification, notification_id)
    if str(notification.user_id) != str(current_user_id):
        return jsonify({"error": "Unauthorized"}), 403
        
    notification.is_read = True
    db.session.commit()
    return jsonify({"success": True}), 200

# ------------------------
# Character API (REST)
# ------------------------

@app.route("/api/characters", methods=["GET", "POST"])
@jwt_required()
def api_characters():
    current_user_id = get_jwt_identity()
    if request.method == "POST":
        data = request.form
        user = db.session.get(User, current_user_id)
        
        if not user.has_unlimited_access():
            character_count = Character.query.filter_by(
                user_id=current_user_id
            ).count()
            
            if character_count >= 10:
                return jsonify({
                    "error": "Free accounts are limited to 10 characters. Support the project on Patreon for unlimited access."
                }), 403

        character_data = {
            "class_name": data.get("class_name"),
            "subclass": data.get("subclass"),
            "level": int(data.get("level", 1)),
            "class_levels": [
                {
                    "class_name": data.get("class_name"),
                    "level": int(data.get("level", 1)),
                    "subclass": data.get("subclass")
                }
            ],
            "abilities": json.loads(data.get("abilities", "{}")),
            "base_abilities": json.loads(data.get("abilities", "{}")),
            "species": data.get("species"),
            "species_variant": data.get("species_variant"),
            "size": data.get("size"),
            "background": data.get("background"),
            "proficiencies": {
                "armor": [],
                "weapons": [],
                "tools": []
            },
            "choices": json.loads(data.get("choices", "{}")),
            "xp": XP_THRESHOLDS.get(int(data.get("level", 1)), 0),
            "level_up_pending": False,
            "level_one_pending": True,
            "hit_dice_remaining": int(data.get("level", 1))
        }

        # Add Skill Proficiencies (Class + Background)
        prof_list = json.loads(data.get("proficiencies", "[]"))
        if prof_list:
            character_data["skillProficiencies"] = {s.lower().replace(" ", "_"): True for s in prof_list}
        # Add Class Proficiencies
        class_name = character_data["class_name"]
        cls = CLASSES.get(class_name.lower())
        
        if cls:
            class_profs = cls.get("proficiencies", {})
            character_data["proficiencies"]["armor"] = class_profs.get("armor", [])
            character_data["proficiencies"]["weapons"] = class_profs.get("weapons", [])
            tools = class_profs.get("tools", {})
            character_data["proficiencies"]["tools"] = tools.get("granted", [])

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

            return {"name": name, "quantity": qty, "category": category, "rarity": "common"}

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
        character.update_hp(character_data, character_data["level"], con_mod)

        try:
            db.session.add(character)
            db.session.commit()
            return jsonify({"id": character.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    # GET all characters
    # Admins see everything. 
    # Regular users see their own (public/private) + others' public characters.
    user = db.session.get(User, current_user_id)
    if user.is_admin:
        characters = Character.query.all()
    else:
        characters = Character.query.filter(
            (Character.user_id == current_user_id) | (Character.is_private == False)
        ).all()
    
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
            "active_run_title": active_run_title,
            "owner_username": c.owner.username,
            "user_id": c.user_id,
            "is_private": c.is_private
        })
        
    return jsonify(result)

@app.route("/api/characters/<int:char_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def api_character_detail(char_id):
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    character = db.get_or_404(Character, char_id)
    
    # Ownership/Privacy Check
    is_owner = str(character.user_id) == str(current_user_id)
    if not is_owner and not user.is_admin:
        if character.is_private:
            return jsonify({"error": "This character is private"}), 403
        
        # If public but not owner/admin, only GET is allowed
        if request.method in ["PUT", "DELETE"]:
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

        # Enforce subclass locking per class
        new_subclass = new_data.get("subclass")
        subclass_class = new_data.get("subclass_class")
        if new_subclass and subclass_class:
            for class_entry in updated_data.get("class_levels", []):
                if class_entry["class_name"].lower() == subclass_class.lower():
                    existing_subclass = class_entry.get("subclass")
                    
                    # Prevent changing an already chosen subclass for THIS class only
                    if existing_subclass and existing_subclass != new_subclass:
                        new_data.pop("subclass", None)
                        break

        updated_data.update(new_data)
        
        # Keep multiclass class_levels subclasses synchronized
        if "subclass" in new_data:
            selected_subclass = new_data["subclass"]
            subclass_class = new_data.get("subclass_class")
            class_levels = updated_data.get("class_levels", [])
            if class_levels and subclass_class:
                for class_entry in class_levels:
                    if class_entry["class_name"].lower() == subclass_class.lower():
                        class_entry["subclass"] = selected_subclass
                        break
                
                updated_data["class_levels"] = class_levels
        
        updated_data.pop("subclass_class", None)
        
        character.set_data(updated_data)
        
        if new_level != old_level:
            abilities = updated_data.get("abilities", {})
            con_score = abilities.get("constitution", 10)
            con_mod = (con_score - 10) // 2
            character.update_hp(updated_data, new_level, con_mod)
            # Note: update_hp saves internally, so we don't need to call set_data again ideally, 
            # but update_hp calls set_data, so it's fine.
        db.session.commit()
        return jsonify({
            "success": True,
            "saved_slots": updated_data.get("spell_slots_current")
        })

    # Check for pending rest
    pending_rest = None
    participant = SessionParticipant.query.filter(
        SessionParticipant.character_id == character.id,
        SessionParticipant.pending_rest != None
    ).first()
    if participant:
        pending_rest = participant.pending_rest

    # GET single character
    data = character.get_data()

    # Recalculate multiclass spell slots when loading character
    data["spell_slots_max"] = calculate_spell_slots(data)

    return jsonify({
        "id": character.id,
        "name": character.name,
        "user_id": character.user_id,
        "is_private": character.is_private,
        "level": data.get("level", 1),
        "class": {
            "name": data.get("class_name"),
            "subclass": next(
                (
                    cls.get("subclass")
                    for cls in data.get("class_levels", [])
                    if cls.get("class_name") == data.get("class_name")
                ),
                data.get("subclass")
            )
        },
        "data": data,
        "pending_rest": pending_rest
    })

@app.route("/api/classes/multiclass-data", methods=["GET"])
@jwt_required()
def get_multiclass_data():

    result = {}

    for class_id, class_rules in CLASSES.items():
        result[class_id] = {
            "name": class_rules.get("name"),
            "primary_ability": class_rules.get("primary_ability")
        }

    return jsonify(result)

@app.route("/api/characters/<int:char_id>/toggle-privacy", methods=["POST"])
@jwt_required()
def api_toggle_character_privacy(char_id):
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    character = db.get_or_404(Character, char_id)
    
    if str(character.user_id) != str(current_user_id) and not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    character.is_private = not character.is_private
    db.session.commit()
    
    return jsonify({
        "success": True, 
        "is_private": character.is_private,
        "message": f"Character is now {'private' if character.is_private else 'public'}"
    })

@app.route("/api/characters/<int:char_id>/levelup", methods=["POST"])
@jwt_required()
def api_character_levelup(char_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    character = db.get_or_404(Character, char_id)
    if str(character.user_id) != str(current_user_id) and not user.is_admin:
        return jsonify({"error": "Unauthorized to level up this character"}), 403
    data = character.get_data()
    previous_state = copy.deepcopy(data)
    levelup_class = request.json.get("class_name") if request.json else None
    if not levelup_class:
        levelup_class = data.get("class_name")
    current_level = data.get("level", 1)
    if current_level >= 20:
        return jsonify({"error": "Character is already at max level"}), 400
    next_level = current_level + 1
    
    # Optional: You could check XP here if you want to enforce threshold
    # But usually this endpoint is for manual overriding or confirmation.
    # To be safe, we'll just allow it if called.

    data["level"] = next_level

    # Update multiclass progression
    class_levels = data.get("class_levels", [])
    
    # Safety fallback for older characters created before multiclass support
    if not class_levels:
        class_levels = [
            {
                "class_name": data.get("class_name"),
                "level": current_level,
                "subclass": data.get("subclass", "")
            }
        ]
    existing_class = next(
        (cls for cls in class_levels if cls["class_name"].lower() == levelup_class.lower()),
        None
    )
    if not existing_class:
        prerequisite = check_multiclass_prerequisites(
            data,
            levelup_class,
            CLASSES
        )
        if not prerequisite["allowed"]:
            return jsonify({
                "error": "Cannot multiclass",
                "reason": prerequisite["reason"]
            }), 400
    if existing_class:
        # Taking another level in an existing class
        existing_class["level"] += 1
    else:
        # Starting a new multiclass
        class_levels.append({
            "class_name": levelup_class,
            "level": 1,
            "subclass": ""
        })
        multiclass_prof = CLASSES[levelup_class.lower()].get("multiclass_proficiencies", {})
        
        # Armor
        for armor in multiclass_prof.get("armor", []):
            if armor not in data["proficiencies"]["armor"]:
                data["proficiencies"]["armor"].append(armor)
        
        # Weapons
        for weapon in multiclass_prof.get("weapons", []):
            if weapon not in data["proficiencies"]["weapons"]:
                data["proficiencies"]["weapons"].append(weapon)
        
        # Tools that are automatically granted
        for tool in multiclass_prof.get("tools", {}).get("granted", []):
            if tool not in data["proficiencies"]["tools"]:
                data["proficiencies"]["tools"].append(tool)
        
        # Skills that are automatically granted
        for skill in multiclass_prof.get("skills", {}).get("granted", []):
            skill_key = skill.lower().replace(".", "_")
            data["skillProficiencies"][skill_key] = True
    data["class_levels"] = class_levels
    
    # Update Spell Slots upon level up (multiclass spellcasting)
    new_max_slots = calculate_spell_slots(data)
    if new_max_slots:
        current_slots = data.get(
            "spell_slots_current",
            {}
        ).copy()
        old_max_slots = data.get(
            "spell_slots_max",
            {}
        )
        updated_slots = {}
        for pool_name, slots in new_max_slots.items():
            if pool_name not in old_max_slots:
                old_max_slots[pool_name] = {}
            if pool_name not in current_slots:
                current_slots[pool_name] = {}
            updated_slots[pool_name] = {}
            for spell_level, maximum in slots.items():
                old_maximum = old_max_slots[pool_name].get(
                    spell_level,
                    0
                )
                current_amount = current_slots[pool_name].get(
                    spell_level,
                    old_maximum
                )
                gained_slots = maximum - old_maximum
                updated_slots[pool_name][spell_level] = min(
                    current_amount + gained_slots,
                    maximum
                )
    if new_max_slots:
        data["spell_slots_current"] = updated_slots
        data["spell_slots_max"] = new_max_slots
    
    # Store complete snapshot before level up
    level_history = data.get("level_history", [])

    # Prevent recursive history growth
    snapshot = copy.deepcopy(previous_state)
    snapshot.pop("level_history", None)
    level_history.append(snapshot)
    data["level_history"] = level_history
    data["level_up_pending"] = False
    character.set_data(data)

    # Recalculate HP
    abilities = data.get("abilities", {})
    con_score = abilities.get("constitution", 10)
    con_mod = (con_score - 10) // 2
    character.update_hp(data, next_level, con_mod)
    
    db.session.commit()
    return jsonify({"success": True, "new_level": next_level, "data": character.get_data()})

@app.route("/api/characters/<int:char_id>/acknowledge-gold-gift", methods=["POST"])
@jwt_required()
def api_acknowledge_gold_gift(char_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    character = db.get_or_404(Character, char_id)
    
    if str(character.user_id) != str(current_user_id) and not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    char_data = character.get_data()
    char_data["gold_gifts"] = []
    
    character.set_data(char_data)
    db.session.commit()
    
    return jsonify({"success": True})

@app.route("/api/characters/<int:char_id>/rest/short", methods=["POST"])
@jwt_required()
def api_character_short_rest(char_id):
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    character = db.get_or_404(Character, char_id)
    
    if str(character.user_id) != str(current_user_id) and not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    data = character.get_data()
    req_data = request.json or {}
    
    # Update HP
    hp_regained = int(req_data.get("hp_regained", req_data.get("hpRegained", 0)))
    dice_spent = int(req_data.get("dice_spent", req_data.get("diceSpent", 0)))
    
    max_hp = data.get("hp_max_base", 0) + data.get("hp_modifier", 0)
    data["hp_current"] = min(max_hp, data.get("hp_current", 0) + hp_regained)
    
    # Update Hit Dice
    hit_dice_remaining = data.get("hit_dice_remaining", {})

    if isinstance(hit_dice_remaining, dict):
        remaining_to_spend = dice_spent
        for class_name in hit_dice_remaining:
            if remaining_to_spend <= 0:
                break
            available = hit_dice_remaining[class_name]
            spent = min(
                available,
                remaining_to_spend
            )
            hit_dice_remaining[class_name] -= spent
            remaining_to_spend -= spent
        data["hit_dice_remaining"] = hit_dice_remaining
    else:
        # Backwards compatibility for old characters
        data["hit_dice_remaining"] = max(
            0,
            hit_dice_remaining - dice_spent
        )
    
    recharged_features = req_data.get("recharged_features", req_data.get("rechargedFeatures", []))
    if recharged_features:
        feature_uses = data.get("featureUses", {})
        for feat_info in recharged_features:
            # Support both legacy string IDs and new structured objects
            if isinstance(feat_info, str):
                feature_uses.pop(feat_info, None)
            elif isinstance(feat_info, dict):
                feat_id = feat_info.get("id")
                if not feat_id:
                    continue
                restore = feat_info.get("restore", "full")
                max_uses = feat_info.get("maxUses")
                if restore == "partial" and max_uses:
                    amount = int(feat_info.get("amount", 1))
                    current = feature_uses.get(feat_id, max_uses)
                    feature_uses[feat_id] = min(max_uses, current + amount)
                else:
                    # Full restore: remove the key so the UI shows max by default
                    feature_uses.pop(feat_id, None)
        data["featureUses"] = feature_uses

    character.set_data(data)
    
    # Clear pending rest
    participations = SessionParticipant.query.filter_by(character_id=character.id).all()
    for p in participations:
        p.pending_rest = None
        
    db.session.commit()
    return jsonify({"success": True, "data": data})

@app.route("/api/characters/<int:char_id>/rest/long", methods=["POST"])
@jwt_required()
def api_character_long_rest(char_id):
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    character = db.get_or_404(Character, char_id)
    
    if str(character.user_id) != str(current_user_id) and not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    data = character.get_data()
    
    # 1. Full HP restoration (Reset current HP to max base + modifier)
    max_hp = data.get("hp_max_base", 0) + data.get("hp_modifier", 0)
    data["hp_current"] = max_hp
    
    # 2. Full Hit Dice replenishment
    hp_rolls = data.get("hp_rolls", {})

    if isinstance(hp_rolls, dict):
        data["hit_dice_remaining"] = {
            class_name: len(rolls)
            for class_name, rolls in hp_rolls.items()
        }
    else:
        # Backwards compatibility for old characters
        data["hit_dice_remaining"] = data.get("level", 1)
    
    # 3. Reset modified Ability Scores to Base
    if "base_abilities" in data:
        data["abilities"] = json.loads(json.dumps(data["base_abilities"]))
    
    # 4. Reduce Exhaustion by 1
    conditions = data.get("conditions", {})
    exhaustion = conditions.get("exhaustion", 0)
    if exhaustion > 0:
        conditions["exhaustion"] = exhaustion - 1
    data["conditions"] = conditions
    
    # 5. Restore Spell Slots on Long Rest
    if "spell_slots_current" in data:
        data["spell_slots_current"] = data.get("spell_slots_max", data["spell_slots_current"])

    req_data = request.json or {}
    recharged_features = req_data.get("recharged_features", req_data.get("rechargedFeatures", []))
    if recharged_features:
        feature_uses = data.get("featureUses", {})
        for feat_info in recharged_features:
            if isinstance(feat_info, str):
                feature_uses.pop(feat_info, None)
            elif isinstance(feat_info, dict):
                feat_id = feat_info.get("id")
                if feat_id:
                    # Long rest always fully restores
                    feature_uses.pop(feat_id, None)
        data["featureUses"] = feature_uses

    character.set_data(data)
    
    # Clear pending rest
    participations = SessionParticipant.query.filter_by(character_id=character.id).all()
    for p in participations:
        p.pending_rest = None
        
    db.session.commit()
    return jsonify({"success": True, "data": data})

@app.route("/api/characters/<int:char_id>/mod-stats", methods=["POST"])
@jwt_required()
def api_character_mod_stats(char_id):
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    character = db.get_or_404(Character, char_id)
    
    if str(character.user_id) != str(current_user_id) and not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    data = character.get_data()
    req_data = request.json or {}
    
    # Expected payload: {"type": "ability", "stat": "strength", "value": 18} 
    # or {"type": "hp_max", "value": 10}
    
    update_type = req_data.get("type")
    if update_type == "ability":
        stat = req_data.get("stat")
        value = int(req_data.get("value", 10))
        if stat in data.get("abilities", {}):
            data["abilities"][stat] = value
    elif update_type == "hp_max":
        value = int(req_data.get("value", 0))
        data["hp_modifier"] = value
        # Update current HP if it's now over max? 
        max_hp = data.get("hp_max_base", 0) + value
        if data.get("hp_current", 0) > max_hp:
            data["hp_current"] = max_hp
    elif update_type == "ac":
        value = int(req_data.get("value", 0))
        data["ac_modifier"] = value

    character.set_data(data)
    db.session.commit()
    return jsonify({"success": True, "data": data})

@app.route("/api/characters/<int:char_id>/leveldown", methods=["POST"])
@jwt_required()
def api_character_leveldown(char_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    character = db.get_or_404(Character, char_id)
    if str(character.user_id) != str(current_user_id) and not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
    data = character.get_data()
    history = data.get("level_history", [])
    if not history:
        return jsonify({
            "error": "No previous level available"
        }), 400
    
    # Get previous character state
    previous_state = history.pop()
    previous_state["level_history"] = history
    
    # Preserve spell choices
    previous_state["spell_slots_current"] = data.get(
        "spell_slots_current",
        {}
    )
    
    # Recalculate spell slots based on new level
    new_slots = calculate_spell_slots(previous_state)
    previous_state["spell_slots_max"] = new_slots
    
    # Clamp current slots
    current_slots = previous_state.get(
        "spell_slots_current",
        {}
    )
    for pool, levels in current_slots.items():
        for spell_level in list(levels.keys()):
            if pool not in new_slots:
                levels[spell_level] = 0
            elif spell_level not in new_slots[pool]:
                levels[spell_level] = 0
            else:
                levels[spell_level] = min(
                    levels[spell_level],
                    new_slots[pool][spell_level]
                )
    character.set_data(previous_state)
    
    # Recalculate HP
    con_score = previous_state["abilities"].get(
        "constitution",
        10
    )
    con_mod = (con_score - 10) // 2
    character.update_hp(
        previous_state,
        previous_state["level"],
        con_mod
    )
    db.session.commit()
    return jsonify({
        "success": True,
        "data": character.get_data()
    })

@app.route("/api/characters/<int:char_id>/acknowledge-item", methods=["POST"])
@jwt_required()
def api_acknowledge_item(char_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    character = db.get_or_404(Character, char_id)
    
    if str(character.user_id) != str(current_user_id) and not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    data = request.json
    if not data or "item_index" not in data:
        return jsonify({"error": "Missing item index"}), 400
        
    idx = data["item_index"]
    char_data = character.get_data()
    inventory = char_data.get("inventory", [])
    
    if idx < 0 or idx >= len(inventory):
        return jsonify({"error": "Item not found"}), 404
        
    # Clear gift flags
    if isinstance(inventory[idx], dict):
        inventory[idx]["is_new_gift"] = False
        
    character.set_data(char_data)
    db.session.commit()
    
    return jsonify({"success": True})

@app.route("/api/characters/<int:char_id>/inventory/remove", methods=["POST"])
@jwt_required()
def api_remove_item(char_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    character = db.get_or_404(Character, char_id)
    
    if str(character.user_id) != str(current_user_id) and not user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    data = request.json
    if not data or "index" not in data:
        return jsonify({"error": "Missing item index"}), 400
        
    idx = data["index"]
    remove_all = data.get("remove_all", False)
    
    char_data = character.get_data()
    inventory = char_data.get("inventory", [])
    
    if idx < 0 or idx >= len(inventory):
        return jsonify({"error": "Item not found"}), 404
        
    item = inventory[idx]
    if isinstance(item, dict) and item.get("quantity", 1) > 1 and not remove_all:
        item["quantity"] -= 1
    else:
        inventory.pop(idx)
        
    character.set_data(char_data)
    db.session.commit()
    
    return jsonify({"success": True, "inventory": inventory})

# ------------------------
# Legacy HTML Routes (safe to remove later)
# ------------------------

@app.route("/characters-hub")
def characters_hub():
    characters = Character.query.all()
    return render_template("characters.html", characters=characters)

@app.route("/characters/<int:char_id>")
def view_character(char_id):
    character = db.get_or_404(Character, char_id)
    return render_template(
        "character_sheet.html",
        character=character,
        character_data=character.get_data(),
        editable=False
    )

@app.route("/characters/<int:char_id>/edit", methods=["GET", "POST"])
def edit_character(char_id):
    character = db.get_or_404(Character, char_id)

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
@jwt_required()
def api_generate_run():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Admins and active Patreon supporters have unlimited Run generation.
    has_unlimited_access = user.has_unlimited_access()

    # Free-user daily limit
    DAILY_RUN_LIMIT = 3

    if not has_unlimited_access:
        today = datetime.utcnow().date()

        # Reset the counter if this is a new calendar day.
        if user.run_generation_date != today:
            user.run_generation_date = today
            user.run_generations_today = 0

        # Stop generation if the user has reached the daily limit.
        if user.run_generations_today >= DAILY_RUN_LIMIT:
            return jsonify({
                "error": "Daily Run generation limit reached. Subscribe to the Patreon for more immediately!",
                "generations_remaining": 0,
                "daily_limit": DAILY_RUN_LIMIT,
                "reset_date": str(today)
            }), 429

    try:
        # Generate the Run.
        encounters = generate_all_encounters(39)
        blessing = generate_divine_blessing()

        # Format encounters for JSON.
        formatted_encounters = []
        for i, enc in enumerate(encounters, 1):
            formatted_encounters.append([i, enc])

        # Only count a generation if generation itself succeeded.
        if not has_unlimited_access:
            user.run_generations_today += 1

        db.session.commit()

        if has_unlimited_access:
            generations_remaining = None
        else:
            generations_remaining = (
                DAILY_RUN_LIMIT - user.run_generations_today
            )

        return jsonify({
            "encounters": formatted_encounters,
            "divine_blessing": blessing,
            "generations_remaining": generations_remaining,
            "daily_limit": DAILY_RUN_LIMIT,
            "unlimited_access": has_unlimited_access,
            "reset_date": (
                str(user.run_generation_date)
                if not has_unlimited_access
                else None
            )
        }), 200

    except Exception as e:
        db.session.rollback()
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
    run = db.get_or_404(Run, run_id)
    parsed = json.loads(run.data)
    return render_template(
        "run_generator.html",
        divine_blessing=parsed["blessing"],
        encounters=parsed["encounters"]
    )

@app.route("/runs/<int:run_id>/delete", methods=["POST"])
def delete_run(run_id):
    run = db.get_or_404(Run, run_id)
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
    try:
        db.session.add(run)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "A trial with this name already exists. Please choose a unique title."}), 400
        
    return jsonify({
        "message": "Run saved successfully",
        "id": run.id
    }), 201

@app.route("/api/runs/<int:run_id>", methods=["DELETE"])
@jwt_required()
def api_delete_run_json(run_id):
    current_user_id = get_jwt_identity()
    run = db.get_or_404(Run, run_id)
    
    # Only the owner or an admin can delete
    is_admin = False
    admin_user = User.query.get(current_user_id)
    if admin_user:
        is_admin = admin_user.is_admin

    if str(run.user_id) != str(current_user_id) and not is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    try:
        db.session.delete(run)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "This Run is connected to a hosted game. To delete this Run, you must first delete the hosted game."}), 400

    return jsonify({"message": "Run deleted successfully"}), 200

@app.route("/api/rules/armor")
def api_rules_armor():
    return jsonify(ARMOR_DATA)

@app.route("/api/rules/weapons")
def api_rules_weapons():
    return jsonify(WEAPONS_DATA)

@app.route("/api/rules/options")
def api_rules_options():
    return jsonify({
        "weapon_mastery": WEAPON_MASTERY_OPTIONS,
        "weapons": WEAPONS_DATA,
        "metamagic": SORCERER_METAMAGIC,
        "invocations": WARLOCK_ELDRITCH_INVOCATIONS
    })

@app.route("/api/feats")
def api_feats():
    return jsonify({
        "origin": ORIGIN_FEATS,
        "general": GENERAL_FEATS,
        "fighting_style": FIGHTING_STYLE_FEATS,
        "epic_boon": EPIC_BOONS
    })

@app.route("/api/rules/spell_slots")
def api_rules_spell_slots():
    return jsonify({
        "full": FULL_CASTER_SLOTS,
        "half": HALF_CASTER_SLOTS,
        "third": THIRD_CASTER_SLOTS,
        "pact_magic": PACT_MAGIC_SLOTS,
        "multiclass_slots": MULTICLASS_CASTER_SLOTS
    })

@app.route("/api/spells/<classname>")
def get_spells(classname):
    class_spells = {}

    classname = classname.lower()

    for level, spells_list in SPELLS.items():
        filtered_spells = []

        for spell in spells_list:

            available = False

            # Normal class spell list
            for cls in spell.get("classes", []):
                if cls.lower() == classname:
                    available = True
                    break

            # Subclass spell access
            if not available:
                for subclass in spell.get("subclasses", []):
                    subclass_name = subclass.lower()

                    if classname in subclass_name:
                        available = True
                        break

            if available:
                filtered_spells.append({
                    **spell,
                    "level": level
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
    user = db.session.get(User, current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    run = db.session.get(Run, data["run_id"])
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
    user = db.session.get(User, current_user_id)
    
    # Get all active sessions
    all_active_sessions = HostedRun.query.filter_by(is_active=True).all()
    
    # Get all participations for the current user to check roles
    user_participations = SessionParticipant.query.filter_by(user_id=current_user_id).all()
    user_session_ids = {p.hosted_run_id: p.role for p in user_participations}
    
    result = []
    for s in all_active_sessions:
        is_participant = s.id in user_session_ids
        is_admin = user.is_admin
        role = user_session_ids.get(s.id, 'Visitor')
        can_enter = is_participant or is_admin
        
        result.append({
            "id": s.id,
            "invite_code": s.invite_code if can_enter else None,
            "dm_name": s.dm.username,
            "run_title": s.run.title_run,
            "role": role,
            "can_enter": can_enter,
            "created_at": s.created_at.isoformat(),
            "participant_count": len(s.participants)
        })
    
    # Sort: Own DM games first, then by DM name
    result.sort(key=lambda x: (x['role'] != 'DM', x['dm_name']))
    
    return jsonify(result), 200

@app.route("/api/host/details/<int:session_id>", methods=["GET"])
@jwt_required()
def api_get_hosted_run_details(session_id):
    current_user_id = get_jwt_identity()
    session = db.get_or_404(HostedRun, session_id)
    
    # Verify participant or Admin
    participant = SessionParticipant.query.filter_by(
        user_id=current_user_id, 
        hosted_run_id=session.id
    ).first()
    
    user = db.session.get(User, current_user_id)
    if not participant and not (user and user.is_admin):
        return jsonify({"error": "Access denied. You are not a participant in this session."}), 403
    
    participants_info = []
    for p in session.participants:
        participants_info.append({
            "user_id": p.user.id,
            "username": p.user.username,
            "role": p.role,
            "pending_rest": p.pending_rest,
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
        "party_inventory": [
            (item if isinstance(item, dict) else {"name": item, "rarity": "common"})
            for item in json.loads(session.party_inventory)
        ],
        "vault_gold": json.loads(session.vault_gold or "[]"),
        "claimed_items": json.loads(session.claimed_items) if session.claimed_items else [],
        "completed_encounters": json.loads(session.completed_encounters),
        "shop_state": json.loads(session.shop_state) if session.shop_state else None,
        "rations": session.rations,
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
    
    character = db.session.get(Character, data["character_id"])
    if not character or str(character.user_id) != str(current_user_id):
        return jsonify({"error": "Character not found or not yours"}), 404
    
    participant.character_id = character.id
    db.session.commit()
    
    return jsonify({"message": "Character linked successfully"}), 200

@app.route("/api/host/<int:session_id>/rename", methods=["POST"])
@jwt_required()
def api_rename_hosted_run(session_id):
    current_user_id = get_jwt_identity()
    session = db.get_or_404(HostedRun, session_id)
    
    if str(session.dm_id) != str(current_user_id):
        return jsonify({"error": "Only the Dungeon Master can rename the run"}), 403
        
    data = request.json
    new_title = data.get("title")
    if not new_title:
        return jsonify({"error": "Missing title"}), 400
        
    try:
        session.run.title_run = new_title[:24].strip()
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "A trial with this name already exists. Please choose a unique title."}), 400
        
    return jsonify({"message": "Run renamed successfully", "title": session.run.title_run}), 200

@app.route("/api/host/<int:session_id>/spend-rations", methods=["POST"])
@jwt_required()
def api_spend_rations(session_id):
    current_user_id = get_jwt_identity()
    session = db.get_or_404(HostedRun, session_id)
    
    user = db.session.get(User, current_user_id)
    is_admin = user.is_admin if user else False
    
    if str(session.dm_id) != str(current_user_id) and not is_admin:
        return jsonify({"error": "Only the Dungeon Master or an Admin can spend rations"}), 403
        
    data = request.json
    rest_type = data.get("rest_type") # 'short' or 'long'
    
    if rest_type not in ['short', 'long']:
        return jsonify({"error": "Invalid rest type"}), 400
        
    cost = 0.5 if rest_type == 'short' else 1.0
    
    if session.rations < cost:
        return jsonify({"error": "Not enough rations"}), 400
        
    session.rations -= cost
    
    # Notify participants and set pending rest
    for participant in session.participants:
        if participant.role != 'DM' and participant.character_id:
            participant.pending_rest = rest_type
            
            # Create global notification
            db.session.add(UserNotification(
                user_id=participant.user_id,
                message=f"A {rest_type.capitalize()} Rest has been initiated by the Dungeon Master! Open your Character Sheet."
            ))
            
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": f"{rest_type.capitalize()} Rest initiated.",
        "rations": session.rations
    })

@app.route("/api/host/<int:session_id>/complete-encounter", methods=["POST"])
@jwt_required()
def api_complete_encounter(session_id):
    current_user_id = get_jwt_identity()
    session = db.get_or_404(HostedRun, session_id)
    
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

    # ── Interactive Shop Encounter ──────────────────────────────────────────────
    if target_enc.get("type") == "Shop Encounter" and target_enc.get("items_by_category"):
        # Mark as completed first
        completed = json.loads(session.completed_encounters)
        if enc_num not in completed:
            completed.append(enc_num)
            session.completed_encounters = json.dumps(completed)

        # Initialise shop_state for the category-selection phase
        shop_state = {
            "encounter_num": int(enc_num),
            "phase": "selection",
            "categories_available": list(SHOP_CATEGORIES),
            "rarity_mix": target_enc.get("rarity_mix", {}),
            "encounter_items": target_enc.get("items_by_category", {}),
            "selections": {},   # char_id (str) -> chosen category
            "items": {},        # populated when phase transitions to shopping
            "common_items": {} # populated when phase transitions to shopping
        }
        session.shop_state = json.dumps(shop_state)
        db.session.commit()

        return jsonify({
            "message": f"Shop Encounter {enc_num} opened — awaiting category selections",
            "shop_started": True
        }), 200
    # ────────────────────────────────────────────────────────────────────────────
    
    # Logic to update party inventory if items/gold were found
    current_inv = json.loads(session.party_inventory)
    vault_gold = json.loads(session.vault_gold or "[]")
    
    if "gold" in target_enc:
        gold_total = target_enc['gold']
        # The user requested that EVERY character receives the FULL amount noted in the encounter, 
        # not a shared portion.
        gold_per_share = gold_total 
        
        # Count connected characters
        connected_participants = [p for p in session.participants if p.role == 'Ascendant' and p.character_id]
        
        # Distribute to connected
        for p in connected_participants:
            character = db.session.get(Character, p.character_id)
            if character:
                char_data = character.get_data()
                char_data["gold"] = char_data.get("gold", 0) + gold_per_share
                character.set_data(char_data)
        
        # Surplus to vault (for empty slots based on party size)
        party_size = run_data.get("settings", {}).get("party_size", 4)
        surplus_shares = party_size - len(connected_participants)
        if surplus_shares > 0:
            vault_gold.append({
                "amount": gold_per_share,
                "count": surplus_shares,
                "source": f"Encounter {enc_num}"
            })
            
    if "magic_items" in target_enc:
        for item in target_enc["magic_items"]:
            current_inv.append(item)
            
    # XP Distribution
    level_up_ready_chars = []
    if "xp" in target_enc or "total_xp" in target_enc:
        xp_gain = target_enc.get("xp") or target_enc.get("total_xp", 0)
        connected_participants = [p for p in session.participants if p.role == 'Ascendant' and p.character_id]
        
        for p in connected_participants:
            character = db.session.get(Character, p.character_id)
            if character:
                char_data = character.get_data()
                current_xp = char_data.get("xp", 0)
                new_xp = current_xp + xp_gain
                char_data["xp"] = new_xp
                
                # Level up check - mark as pending, do not increase level yet
                current_level = char_data.get("level", 1)
                next_threshold = XP_THRESHOLDS.get(current_level + 1, 999999)

                if new_xp >= next_threshold:
                    char_data["level_up_pending"] = True
                    level_up_ready_chars.append(character.name)

                character.set_data(char_data)

    session.party_inventory = json.dumps(current_inv)
    session.vault_gold = json.dumps(vault_gold)
    
    # Handle Rations from encounter
    rations_found = 0
    if "rations" in target_enc:
        rations_found = float(target_enc["rations"])
        session.rations = round(session.rations + rations_found, 1)

    # Update completed encounters
    completed = json.loads(session.completed_encounters)
    if enc_num not in completed:
        completed.append(enc_num)
        session.completed_encounters = json.dumps(completed)
            
    db.session.commit()
    
    res_data = {
        "message": f"Encounter {enc_num} completed",
        "party_inventory": current_inv,
        "rations_found": rations_found,
        "rations": session.rations
    }
    if level_up_ready_chars:
        res_data["leveled_up"] = level_up_ready_chars
        res_data["message"] += f". {', '.join(level_up_ready_chars)} can now Level Up!"
        
    return jsonify(res_data), 200


# ------------------------
# Shop Interaction API
# ------------------------

@app.route("/api/host/<int:session_id>/shop/select-category", methods=["POST"])
@jwt_required()
def api_shop_select_category(session_id):
    """Player selects a category to add to the shop during the selection phase."""
    current_user_id = get_jwt_identity()
    data = request.json
    category = data.get("category") if data else None

    if not category or category not in SHOP_CATEGORIES:
        return jsonify({"error": "Invalid or missing category"}), 400

    session = db.get_or_404(HostedRun, session_id)
    participant = SessionParticipant.query.filter_by(
        user_id=current_user_id,
        hosted_run_id=session_id
    ).first()

    if not participant:
        return jsonify({"error": "Access denied"}), 403
    if participant.role == 'DM':
        return jsonify({"error": "Dungeon Masters cannot select shop categories"}), 403
    if not participant.character_id:
        return jsonify({"error": "You must link a character before selecting a category"}), 400

    if not session.shop_state:
        return jsonify({"error": "No active shop phase"}), 400

    shop_state = json.loads(session.shop_state)

    if shop_state.get("locked"):
        return jsonify({"error": "The shop is currently locked by the Dungeon Master"}), 403

    if shop_state.get("phase") != "selection":
        return jsonify({"error": "Category selection phase is over"}), 400

    char_id = str(participant.character_id)

    if char_id in shop_state["selections"]:
        return jsonify({"error": "You have already made your selection"}), 400

    if category in shop_state["selections"].values():
        return jsonify({"error": "Another party member already chose this category"}), 400

    # Record the selection
    shop_state["selections"][char_id] = category

    # Count eligible ascendants (those with a linked character)
    ascendant_count = sum(
        1 for p in session.participants
        if p.role == 'Ascendant' and p.character_id is not None
    )
    needed = min(4, ascendant_count)
    selections_made = len(shop_state["selections"])

    # Transition to shopping phase when all needed selections are in
    if selections_made >= needed:
        encounter_items = shop_state.get("encounter_items", {})
        rarity_mix = shop_state.get("rarity_mix", {})
        possible_rarities = list(rarity_mix.keys())

        # Build priced item list for each chosen category
        items = {}
        seen_categories = set()
        for _char_id, chosen_cat in shop_state["selections"].items():
            if chosen_cat in seen_categories:
                continue
            seen_categories.add(chosen_cat)
            raw_items = encounter_items.get(chosen_cat, [])
            priced = []
            for item_raw in raw_items:
                # Handle both legacy string items and new object items
                if isinstance(item_raw, dict):
                    item_name = item_raw.get("name")
                    rarity = item_raw.get("rarity")
                    item_cat = item_raw.get("category", chosen_cat)
                else:
                    item_name = item_raw
                    rarity = determine_item_rarity(item_name, chosen_cat, possible_rarities) if possible_rarities else "common"
                    item_cat = chosen_cat
                    
                cost = get_item_price(item_name, rarity, item_cat)
                priced.append({
                    "name": item_name, 
                    "rarity": rarity, 
                    "cost": cost, 
                    "sold_to": None,
                    "category": item_cat
                })
            items[chosen_cat] = priced

        # Check for additional Wondrous category in encounter data
        if "Wondrous" in encounter_items:
            wondrous_raw = encounter_items["Wondrous"]
            priced_wondrous = []
            for item_raw in wondrous_raw:
                if isinstance(item_raw, dict):
                    item_name = item_raw.get("name")
                    rarity = item_raw.get("rarity")
                    item_cat = "Wondrous"
                else:
                    item_name = item_raw
                    rarity = determine_item_rarity(item_name, "Wondrous", possible_rarities) if possible_rarities else "common"
                    item_cat = "Wondrous"
                    
                cost = get_item_price(item_name, rarity, item_cat)
                priced_wondrous.append({
                    "name": item_name, 
                    "rarity": rarity, 
                    "cost": cost, 
                    "sold_to": None,
                    "category": item_cat
                })
            items["Wondrous"] = priced_wondrous

        shop_state["items"] = items
        shop_state["common_items"] = generate_common_shop_items()
        shop_state["phase"] = "shopping"

    session.shop_state = json.dumps(shop_state)
    db.session.commit()

    return jsonify({"shop_state": shop_state}), 200


@app.route("/api/host/<int:session_id>/shop/buy-item", methods=["POST"])
@jwt_required()
def api_shop_buy_item(session_id):
    """Player purchases an item from the active shop."""
    current_user_id = get_jwt_identity()
    data = request.json

    if not data or "category" not in data or "item_index" not in data:
        return jsonify({"error": "Missing category or item_index"}), 400

    category = data["category"]
    item_index = data["item_index"]
    is_common = data.get("is_common", False)  # True = buying from the always-available common section

    session = db.get_or_404(HostedRun, session_id)
    participant = SessionParticipant.query.filter_by(
        user_id=current_user_id,
        hosted_run_id=session_id
    ).first()

    if not participant:
        return jsonify({"error": "Access denied"}), 403
    if participant.role == 'DM':
        return jsonify({"error": "Dungeon Masters cannot buy from the shop"}), 403
    if not participant.character_id:
        return jsonify({"error": "You must link a character before shopping"}), 400

    if not session.shop_state:
        return jsonify({"error": "No active shop"}), 400

    shop_state = json.loads(session.shop_state)

    if shop_state.get("locked"):
        return jsonify({"error": "The shop is currently locked by the Dungeon Master"}), 403

    if shop_state.get("phase") != "shopping":
        return jsonify({"error": "The shop is not open yet"}), 400
    if is_common:
        item_list = shop_state.get("common_items", {}).get(category, [])
    else:
        item_list = shop_state.get("items", {}).get(category, [])

    if item_index < 0 or item_index >= len(item_list):
        return jsonify({"error": "Item not found"}), 404

    item = item_list[item_index]

    # Regular items can only be bought once
    if not is_common and item.get("sold_to") is not None:
        return jsonify({"error": "This item has already been purchased"}), 400

    cost = item.get("cost", 0)

    # Check buyer's gold
    character = db.session.get(Character, participant.character_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    char_data = character.get_data()
    current_gold = int(char_data.get("gold", 0))

    # Calculate trade-in discount
    trade_in_indices = data.get("trade_in_indices", [])
    total_discount = 0
    if trade_in_indices and category == "Wondrous":
        inventory = char_data.get("inventory", [])
        # We process indices in reverse order to ensure removing items doesn't invalidate subsequent indices
        # But wait, indices might be out of sync if we just pop. 
        # Better: identify items first, then filter them out.
        
        valid_indices = []
        for idx in trade_in_indices:
            if idx < 0 or idx >= len(inventory):
                continue
            item_raw = inventory[idx]
            # Normalize to dict
            traded_item = item_raw if isinstance(item_raw, dict) else {"name": item_raw, "rarity": "common", "category": "Other"}
            
            # Verify rarity matches (case-insensitive)
            tr = (traded_item.get("rarity") or "common").lower()
            ir = (item.get("rarity") or "common").lower()
            
            if tr == ir:
                item_val = get_item_price(traded_item.get("name"), traded_item.get("rarity"), traded_item.get("category", "Other"))
                total_discount += item_val
                valid_indices.append(idx)
        
        # Remove traded items from inventory
        new_inventory = [item for i, item in enumerate(inventory) if i not in valid_indices]
        char_data["inventory"] = new_inventory

    final_cost = max(0, cost - total_discount)

    if current_gold < final_cost:
        return jsonify({"error": f"Insufficient gold. Final cost after trade-ins: {final_cost} gp"}), 400

    # Deduct gold
    char_data["gold"] = current_gold - final_cost

    # Add item to character inventory (top)
    inv_item = {
        "name": item["name"],
        "quantity": 1,
        "category": category,
        "rarity": item.get("rarity", "common"),
        "shop_purchase": True
    }
    if "inventory" not in char_data:
        char_data["inventory"] = []
    char_data["inventory"].insert(0, inv_item)
    character.set_data(char_data)

    # Mark item as sold in shop_state (regular items only)
    if not is_common:
        shop_state["items"][category][item_index]["sold_to"] = {
            "char_id": participant.character_id,
            "char_name": character.name
        }
        session.shop_state = json.dumps(shop_state)

    db.session.commit()

    return jsonify({
        "message": f"{character.name} purchased {item['name']} for {cost} gp",
        "new_gold": char_data["gold"],
        "shop_state": shop_state
    }), 200

@app.route("/api/host/<int:session_id>/shop/sell-items", methods=["POST"])
@jwt_required()
def api_shop_sell_items(session_id):
    current_user_id = get_jwt_identity()
    data = request.json
    if not data or "items" not in data:
        return jsonify({"error": "Missing items"}), 400
    session = db.get_or_404(HostedRun, session_id)
    participant = SessionParticipant.query.filter_by(
        user_id=current_user_id,
        hosted_run_id=session_id
    ).first()
    if not participant:
        return jsonify({"error": "Access denied"}), 403
    if participant.role == "DM":
        return jsonify({"error": "Dungeon Masters cannot sell items"}), 403
    if not participant.character_id:
        return jsonify({"error": "You must link a character before selling"}), 400
    if not session.shop_state:
        return jsonify({"error": "No active shop"}), 400
    shop_state = json.loads(session.shop_state)
    if shop_state.get("locked"):
        return jsonify({"error": "The shop is currently locked"}), 403
    if shop_state.get("phase") != "shopping":
        return jsonify({"error": "Shop is not open"}), 400
    character = db.session.get(Character, participant.character_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    char_data = character.get_data()
    inventory = char_data.get("inventory", [])
    selected_items = data["items"]
    
    total_gold = 0

    for sale in selected_items:
        idx = sale["index"]
        quantity_to_sell = sale["quantity"]
        if idx < 0 or idx >= len(inventory):
            return jsonify({"error": "Invalid inventory index"}), 400
        raw_item = inventory[idx]
        if isinstance(raw_item, str):
            item = {
                "name": raw_item,
                "rarity": "common",
                "category": "Other",
                "quantity": 1
            }

            inventory[idx] = item
        else:
            item = raw_item
        current_quantity = item.get("quantity", 1)
        if quantity_to_sell <= 0 or quantity_to_sell > current_quantity:
            return jsonify({"error": "Selling too many items"}), 400
        unit_price = get_item_sell_price(
            item.get("name"),
            item.get("rarity", "common"),
            item.get("category", "Other")
        )
        total_gold += unit_price * quantity_to_sell
        item["quantity"] = current_quantity - quantity_to_sell
    # Remove empty stacks
    inventory = [
        item for item in inventory
        if not isinstance(item, dict)
        or item.get("quantity", 1) > 0
    ]
    char_data["inventory"] = inventory
    current_gold = int(char_data.get("gold",0))
    char_data["gold"] = current_gold + total_gold
    character.set_data(char_data)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "gold_gained": total_gold,
        "new_gold": char_data["gold"],
        "inventory": inventory
    }), 200

@app.route("/api/host/<int:session_id>/shop/sell-price", methods=["POST"])
@jwt_required()
def api_shop_sell_price(session_id):
    current_user_id = get_jwt_identity()
    session = db.get_or_404(HostedRun, session_id)
    participant = SessionParticipant.query.filter_by(
        user_id=current_user_id,
        hosted_run_id=session_id
    ).first()
    if not participant:
        return jsonify({"error": "Access denied"}), 403
    data = request.json
    if not data or "items" not in data:
        return jsonify({"error": "Missing items"}), 400
    prices = {}
    for index, raw_item in enumerate(data["items"]):
        if isinstance(raw_item, str):
            item = {
                "name": raw_item,
                "rarity": "common",
                "category": "Other",
                "quantity": 1
            }
        else:
            item = raw_item
        sell_price = get_item_sell_price(
            item.get("name"),
            item.get("rarity", "common"),
            item.get("category", "Other")
        )
        quantity = item.get("quantity", 1)
        prices[index] = sell_price * quantity
    return jsonify({
        "prices": prices
    }), 200

@app.route("/api/host/<int:session_id>/shop/toggle-lock", methods=["POST"])
@jwt_required()
def api_shop_toggle_lock(session_id):
    """DM or Admin toggles the locked state of the shop."""
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    session = db.get_or_404(HostedRun, session_id)

    # Authorization Check: DM of session or Admin
    if str(session.dm_id) != str(current_user_id) and not user.is_admin:
        return jsonify({"error": "Unauthorized: Only the Dungeon Master or an Admin can lock/unlock the shop"}), 403

    if not session.shop_state:
        return jsonify({"error": "No active shop to lock"}), 400

    shop_state = json.loads(session.shop_state)
    is_locked = shop_state.get("locked", False)
    shop_state["locked"] = not is_locked

    session.shop_state = json.dumps(shop_state)
    db.session.commit()

    return jsonify({
        "success": True,
        "locked": shop_state["locked"],
        "message": f"Shop {'locked' if shop_state['locked'] else 'unlocked'} successfully"
    }), 200

@app.route("/api/host/<int:session_id>/claim-item", methods=["POST"])
@jwt_required()
def api_claim_item(session_id):
    current_user_id = get_jwt_identity()
    data = request.json
    if not data or "item_index" not in data:
        return jsonify({"error": "Missing item index"}), 400
    
    session = db.get_or_404(HostedRun, session_id)
    participant = SessionParticipant.query.filter_by(
        user_id=current_user_id, 
        hosted_run_id=session.id
    ).first()
    
    if not participant:
        return jsonify({"error": "Access denied"}), 403
        
    if participant.role == 'DM':
        return jsonify({"error": "Dungeon Masters cannot claim items from the Vault"}), 403
    
    if not participant.character_id:
        return jsonify({"error": "You must select an Ascendant character before claiming items from the Vault"}), 400
        
    character = db.session.get(Character, participant.character_id)
    if not character:
        return jsonify({"error": "Associated character not found"}), 404
    
    inventory = json.loads(session.party_inventory)
    claimed = json.loads(session.claimed_items or "[]")
    idx = data["item_index"]
    
    if idx < 0 or idx >= len(inventory):
        return jsonify({"error": "Item not found in vault"}), 404
    
    item = inventory.pop(idx)
    # Ensure item is a dict for character inventory
    normalized_item = item if isinstance(item, dict) else {"name": item, "rarity": "common", "quantity": 1, "category": "Other"}
    
    # Update Character Inventory
    char_data = character.get_data()
    if "inventory" not in char_data:
        char_data["inventory"] = []
    # Prepend the item (user requested items at the top)
    char_data["inventory"].insert(0, normalized_item)
    character.set_data(char_data)
    
    # Update Session Claimed Items
    claimed.append({
        "item": normalized_item["name"],
        "character_name": character.name,
        "character_id": character.id
    })
    
    session.party_inventory = json.dumps(inventory)
    session.claimed_items = json.dumps(claimed)
    db.session.commit()
    
    return jsonify({
        "message": f"Claimed {item}",
        "party_inventory": inventory,
        "claimed_items": claimed
    }), 200

@app.route("/api/host/<int:session_id>/claim-gold", methods=["POST"])
@jwt_required()
def api_claim_gold(session_id):
    current_user_id = get_jwt_identity()
    session = db.get_or_404(HostedRun, session_id)
    participant = SessionParticipant.query.filter_by(user_id=current_user_id, hosted_run_id=session_id).first()
    
    if not participant or participant.role == 'DM':
        return jsonify({"error": "Dungeon Masters cannot claim gold from the Vault"}), 403
    
    if not participant.character_id:
        return jsonify({"error": "You must select an Ascendant character before claiming gold"}), 400

    data = request.json
    share_index = data.get("share_index")
    if share_index is None:
        return jsonify({"error": "Missing share_index"}), 400

    vault_gold = json.loads(session.vault_gold or "[]")
    if share_index < 0 or share_index >= len(vault_gold):
        return jsonify({"error": "Gold share not found"}), 404

    character = db.session.get(Character, participant.character_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    # Claim one share
    share = vault_gold[share_index]
    amount = share["amount"]
    
    char_data = character.get_data()
    char_data["gold"] = char_data.get("gold", 0) + amount
    character.set_data(char_data)

    share["count"] -= 1
    if share["count"] <= 0:
        vault_gold.pop(share_index)
    
    session.vault_gold = json.dumps(vault_gold)
    
    # Also log in claimed_items for history if we want (optional but good)
    claimed = json.loads(session.claimed_items or "[]")
    claimed.append({
        "item": f"{amount} Gold (1x Share)",
        "character_name": character.name,
        "character_id": character.id
    })
    session.claimed_items = json.dumps(claimed)
    
    db.session.commit()
    
    return jsonify({
        "message": f"Claimed {amount} gold",
        "vault_gold": vault_gold,
        "claimed_items": claimed
    }), 200

@app.route("/api/host/<int:session_id>", methods=["DELETE"])
@jwt_required()
def api_delete_hosted_run(session_id):
    current_user_id = get_jwt_identity()
    session = db.get_or_404(HostedRun, session_id)
    
    if str(session.dm_id) != str(current_user_id):
        return jsonify({"error": "Only the Dungeon Master can delete this session"}), 403
    
    # Participants will be deleted by cascade delete-orphan in HostedRun model
    db.session.delete(session)
    db.session.commit()
    
    return jsonify({"message": "Session deleted successfully"}), 200

@app.route("/api/host/<int:session_id>/transfer-item", methods=["POST"])
@jwt_required()
def api_transfer_item(session_id):
    current_user_id = get_jwt_identity()
    data = request.json
    
    if not data or not data.get("sender_char_id") or not data.get("receiver_char_id") or "item_index" not in data:
        return jsonify({"error": "Missing required transfer data"}), 400
        
    session = db.get_or_404(HostedRun, session_id)
    if not session.is_active:
        return jsonify({"error": "This session is no longer active"}), 400
        
    sender_id = data["sender_char_id"]
    receiver_id = data["receiver_char_id"]
    item_idx = data["item_index"]
    
    # 1. Validate Participants
    sender_participant = SessionParticipant.query.filter_by(hosted_run_id=session.id, character_id=sender_id).first()
    receiver_participant = SessionParticipant.query.filter_by(hosted_run_id=session.id, character_id=receiver_id).first()
    
    if not sender_participant or not receiver_participant:
        return jsonify({"error": "One or both characters are not in this session"}), 400
        
    # 2. Authorization Check: Owner of sender, DM of session, or Admin
    requesting_user = db.session.get(User, current_user_id)
    sender_char = db.session.get(Character, sender_id)
    
    is_owner = str(sender_char.user_id) == str(current_user_id)
    is_dm = str(session.dm_id) == str(current_user_id)
    is_admin = requesting_user.is_admin if requesting_user else False
    
    if not (is_owner or is_dm or is_admin):
        return jsonify({"error": "Unauthorized to transfer items from this character"}), 403
        
    # 3. Perform Transfer
    receiver_char = db.session.get(Character, receiver_id)
    
    sender_data = sender_char.get_data()
    receiver_data = receiver_char.get_data()
    
    sender_inv = sender_data.get("inventory", [])
    if item_idx < 0 or item_idx >= len(sender_inv):
        return jsonify({"error": "Item not found in sender's inventory"}), 404
        
    # Extract item
    item = sender_inv.pop(item_idx)
    
    # Add to receiver (at the top)
    if "inventory" not in receiver_data:
        receiver_data["inventory"] = []
    
    # Add Gift Metadata
    if isinstance(item, str):
        item = {"name": item, "quantity": 1, "category": "Other"}
    
    item["is_new_gift"] = True
    item["from_character_name"] = sender_char.name
    item["from_user_name"] = requesting_user.username
    
    receiver_data["inventory"].insert(0, item)
    
    # Save both
    sender_char.set_data(sender_data)
    receiver_char.set_data(receiver_data)
    
    db.session.commit()
    
    return jsonify({
        "success": True, 
        "message": f"Transferred {item.get('name', 'item')} to {receiver_char.name}",
        "sender_inventory": sender_inv
    }), 200

@app.route("/api/admin/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def api_admin_delete_user(user_id):
    admin_id = get_jwt_identity()
    admin_user = db.session.get(User, admin_id)
    
    if not admin_user or not admin_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    user_to_delete = db.get_or_404(User, user_id)
    
    if str(user_to_delete.id) == str(admin_id):
        return jsonify({"error": "You cannot delete your own account"}), 400
        
    # Manual cleanup for sessions where this user is DM
    hosted_runs = HostedRun.query.filter_by(dm_id=user_to_delete.id).all()
    for hr in hosted_runs:
        db.session.delete(hr)

    # Manual cleanup for participations in other sessions
    SessionParticipant.query.filter_by(user_id=user_to_delete.id).delete(
        synchronize_session=False
    )

    # Delete all Runs owned by this user.
    # HostedRun records referencing these runs have already been removed above.
    Run.query.filter_by(user_id=user_to_delete.id).delete(
        synchronize_session=False
    )

    # Character deletion, reports, and notifications are handled
    # by the User relationships' cascade settings.
    db.session.delete(user_to_delete)
    db.session.commit()
    
    return jsonify({"message": f"User {user_to_delete.username} and all associated data deleted successfully"}), 200

@app.route("/api/host/<int:session_id>/transfer-gold", methods=["POST"])
@jwt_required()
def api_transfer_gold(session_id):
    current_user_id = get_jwt_identity()
    data = request.json
    
    if not data or not data.get("sender_char_id") or not data.get("receiver_char_id") or "amount" not in data:
        return jsonify({"error": "Missing required transfer data"}), 400
        
    session = db.get_or_404(HostedRun, session_id)
    if not session.is_active:
        return jsonify({"error": "This session is no longer active"}), 400
        
    sender_id = data["sender_char_id"]
    receiver_id = data["receiver_char_id"]
    try:
        amount = int(data["amount"])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount"}), 400
        
    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400
        
    # 1. Validate Participants
    sender_participant = SessionParticipant.query.filter_by(hosted_run_id=session.id, character_id=sender_id).first()
    receiver_participant = SessionParticipant.query.filter_by(hosted_run_id=session.id, character_id=receiver_id).first()
    
    if not sender_participant or not receiver_participant:
        return jsonify({"error": "One or both characters are not in this session"}), 400
        
    # 2. Authorization Check: Owner of sender, DM of session, or Admin
    requesting_user = db.session.get(User, current_user_id)
    sender_char = db.session.get(Character, sender_id)
    
    is_owner = str(sender_char.user_id) == str(current_user_id)
    is_dm = str(session.dm_id) == str(current_user_id)
    is_admin = requesting_user.is_admin if requesting_user else False
    
    if not (is_owner or is_dm or is_admin):
        return jsonify({"error": "Unauthorized to transfer gold from this character"}), 403
        
    # 3. Perform Transfer
    receiver_char = db.session.get(Character, receiver_id)
    
    sender_data = sender_char.get_data()
    receiver_data = receiver_char.get_data()
    
    sender_gold = int(sender_data.get("gold", 0))
    if sender_gold < amount:
        return jsonify({"error": "Insufficient gold"}), 400
        
    # Deduct sender, Add receiver
    sender_data["gold"] = sender_gold - amount
    receiver_data["gold"] = int(receiver_data.get("gold", 0)) + amount
    
    # Add gold gift notification to receiver
    if "gold_gifts" not in receiver_data:
        receiver_data["gold_gifts"] = []
    
    # Limit number of pending notifications to avoid data bloat
    receiver_data["gold_gifts"] = receiver_data["gold_gifts"][-9:] 
    receiver_data["gold_gifts"].append({
        "amount": amount,
        "from_character_name": sender_char.name,
        "timestamp": datetime.now().isoformat()
    })
    
    sender_char.set_data(sender_data)
    receiver_char.set_data(receiver_data)
    
    db.session.commit()
    
    return jsonify({
        "success": True, 
        "message": f"Transferred {amount} GP to {receiver_char.name}",
        "new_gold": sender_data["gold"]
    }), 200

# ------------------------
# Entry Point
# ------------------------

if __name__ == "__main__":
    app.run(debug=True)
