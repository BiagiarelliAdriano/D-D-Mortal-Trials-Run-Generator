import random
from fractions import Fraction
from encounter_generator.data.items import MAGIC_ITEMS
from encounter_generator.data.monsters import MONSTERS, MONSTERS_BY_TYPE, filtered_monsters
from encounter_generator.data.wildsurges import WILD_SURGES
from encounter_generator.generator import (
    generate_enspell_armor,
    generate_enspell_staff,
    generate_enspell_weapon,
    generate_scroll_for_rarity,
    get_random_magic_item,
    get_random_wondrous_item,
    get_rations,
)

ENCOUNTER_DEFINITIONS = {
    1: {
        "allowed_rarities": ["common", "uncommon"],
        "xp": 600,
        "total_xp": 900,
        "is_levelup": True,
        "gold": 100,
        "monsters": [("1/2", 2), ("1/4", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
    },
    2: {
        "allowed_rarities": ["common", "uncommon"],
        "xp": 900,
        "total_xp": 1800,
        "is_levelup": False,
        "gold": 100,
        "monsters": [("1", 2), ("1/2", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
    },
    3: {
        "allowed_rarities": ["common", "uncommon"],
        "xp": 1050,
        "total_xp": 2850,
        "is_levelup": True,
        "gold": 200,
        "monsters": [("1", 2), ("1/2", 3)],
        "magic_loot_count": 4,
        "is_combat": True,
    },
    4: {
        "allowed_rarities": ["common", "uncommon"],
        "xp": 1425,
        "total_xp": 4275,
        "is_levelup": False,
        "gold": 200,
        "monsters": [("2", 1), ("1", 2), ("1/2", 1)],
        "magic_loot_count": 4,
        "is_combat": True,
    },
    5: {
        "shop": ("uncommon", "rare"),
        "total_gold": 600,
        "is_shop": True
    },
    6: {
        "allowed_rarities": ["uncommon"],
        "xp": 1575,
        "total_xp": 5850,
        "is_levelup": False,
        "gold": 300,
        "monsters": [("2", 1), ("1", 2), ("1/2", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
    },
    7: {
        "allowed_rarities": ["uncommon"],
        "xp": 1725,
        "total_xp": 7575,
        "is_levelup": True,
        "gold": 300,
        "monsters": [("2", 1), ("1", 2), ("1/2", 3)],
        "magic_loot_count": 4,
        "is_combat": True,
    },
    8: {
        "allowed_rarities": ["uncommon"],
        "xp": 3000,
        "total_xp": 10575,
        "is_levelup": False,
        "gold": 400,
        "monsters": [("3", 1), ("2", 2), ("1", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
    },
    9: {
        "allowed_rarities": ["uncommon"],
        "xp": 3300,
        "total_xp": 13875,
        "is_levelup": True,
        "gold": 400,
        "monsters": [("3", 1), ("2", 2), ("1/2", 3)],
        "magic_loot_count": 4,
        "is_combat": True,
    },
    10: {
        "total_gold": 1400,
        "note": "Revisit to previous shop.",
        "is_shop": True,
    },
    11: {
        "allowed_rarities": ["very rare"],
        "xp": 4350,
        "total_xp": 18225,
        "is_levelup": False,
        "gold": 4000,
        "monsters": [("5", 1), ("3", 1), ("1", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    12: {
        "allowed_rarities": ["uncommon", "rare"],
        "xp": 4575,
        "total_xp": 22800,
        "is_levelup": True,
        "gold": 500,
        "monsters": [("4", 2), ("2", 1), ("1", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    13: {
        "allowed_rarities": ["uncommon", "rare"],
        "xp": 5700,
        "total_xp": 28500,
        "is_levelup": False,
        "gold": 500,
        "monsters": [("5", 1), ("4", 1), ("2", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    14: {
        "allowed_rarities": ["uncommon", "rare"],
        "xp": 6075,
        "total_xp": 34575,
        "is_levelup": True,
        "gold": 600,
        "monsters": [("5", 1), ("4", 1), ("3", 1), ("2", 1)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    15: {
        "allowed_rarities": ["uncommon", "rare"],
        "xp": 6825,
        "total_xp": 41400,
        "is_levelup": False,
        "gold": 600,
        "monsters": [("6", 1), ("4", 1), ("3", 1), ("2", 1)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    16: {
        "shop": ("rare", "very rare"),
        "total_gold": 6200,
        "is_shop": True
    },
    17: {
        "allowed_rarities": ["rare"],
        "xp": 7200,
        "total_xp": 48600,
        "is_levelup": True,
        "gold": 700,
        "monsters": [("6", 1), ("4", 1), ("3", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    18: {
        "allowed_rarities": ["rare"],
        "xp": 8700,
        "total_xp": 57300,
        "is_levelup": False,
        "gold": 700,
        "monsters": [("7", 1), ("5", 1), ("3", 1), ("1", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    19: {
        "allowed_rarities": ["rare"],
        "xp": 9450,
        "total_xp": 66750,
        "is_levelup": True,
        "gold": 800,
        "monsters": [("7", 1), ("5", 1), ("3", 1), ("2", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    20: {
        "allowed_rarities": ["rare"],
        "xp": 10500,
        "total_xp": 77250,
        "is_levelup": False,
        "gold": 800,
        "monsters": [("8", 1), ("4", 2), ("2", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    21: {
        "total_gold": 3000,
        "note": "Revisit to previous shop.",
        "is_shop": True,
    },
    22: {
        "allowed_rarities": ["very rare"],
        "xp": 12000,
        "total_xp": 89250,
        "is_levelup": True,
        "gold": 40000,
        "monsters": [("10", 1), ("3", 3)],
        "magic_loot_count": 8,
        "is_combat": True,
        "has_wild_surge": True,
    },
    23: {
        "allowed_rarities": ["rare", "very rare"],
        "xp": 10425,
        "total_xp": 99765,
        "is_levelup": False,
        "gold": 4000,
        "monsters": [("9", 1), ("4", 1), ("2", 1), ("1", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    24: {
        "allowed_rarities": ["rare", "very rare"],
        "xp": 11475,
        "total_xp": 111150,
        "is_levelup": True,
        "gold": 4000,
        "monsters": [("9", 1), ("5", 1), ("2", 1), ("1", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    25: {
        "allowed_rarities": ["rare", "very rare"],
        "xp": 15000,
        "total_xp": 126150,
        "is_levelup": True,
        "gold": 5000,
        "monsters": [("10", 1), ("6", 1), ("4", 1), ("3", 1)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    26: {
        "allowed_rarities": ["rare", "very rare"],
        "xp": 17250,
        "total_xp": 143400,
        "is_levelup": True,
        "gold": 5000,
        "monsters": [("11", 1), ("7", 1), ("3", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    27: {
        "shop": ("very rare", "legendary"),
        "total_gold": 58000,
        "is_shop": True
    },
    28: {
        "allowed_rarities": ["very rare"],
        "xp": 20100,
        "total_xp": 163500,
        "is_levelup": False,
        "gold": 6000,
        "monsters": [("12", 1), ("8", 1), ("4", 1)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    29: {
        "allowed_rarities": ["very rare"],
        "xp": 20550,
        "total_xp": 184050,
        "is_levelup": True,
        "gold": 6000,
        "monsters": [("12", 1), ("8", 1), ("3", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    30: {
        "allowed_rarities": ["very rare"],
        "xp": 23850,
        "total_xp": 207900,
        "is_levelup": True,
        "gold": 7000,
        "monsters": [("13", 1), ("9", 1), ("2", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    31: {
        "allowed_rarities": ["very rare"],
        "xp": 25200,
        "total_xp": 233100,
        "is_levelup": True,
        "gold": 7000,
        "monsters": [("14", 1), ("6", 2), ("4", 1)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    32: {
        "total_gold": 26000,
        "note": "Revisit to previous shop.",
        "is_shop": True,
    },
    33: {
        "allowed_rarities": ["legendary"],
        "xp": 29700,
        "total_xp": 262800,
        "is_levelup": True,
        "gold": 200000,
        "monsters": [("16", 1), ("6", 1), ("4", 1), ("3", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    34: {
        "allowed_rarities": ["very rare", "legendary"],
        "xp": 34500,
        "total_xp": 297300,
        "is_levelup": False,
        "gold": 50000,
        "monsters": [("15", 1), ("14", 1), ("9", 2)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    35: {
        "allowed_rarities": ["very rare", "legendary"],
        "xp": 34800,
        "total_xp": 332100,
        "is_levelup": True,
        "gold": 50000,
        "monsters": [("16", 1), ("13", 1), ("10", 1), ("8", 1)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    36: {
        "allowed_rarities": ["legendary"],
        "xp": 42600,
        "total_xp": 374700,
        "is_levelup": True,
        "gold": 100000,
        "monsters": [("17", 1), ("14", 1), ("11", 1), ("10", 1)],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    37: {
        "allowed_rarities": ["legendary"],
        "gold": 100000,
        "monsters": [("17", 1), ("14", 2), ("11", 1), ("8", 1)],
        "random_cr_choices": ["17", "18", "19"],
        "magic_loot_count": 4,
        "is_combat": True,
        "has_wild_surge": True,
    },
    38: {
        "shop": ("legendary", "legendary"),
        "total_gold": 500000,
        "is_shop": True
    },
    39: {
        "monsters": [("20", 1), ("15", 1), ("10", 2)],
        "random_cr_choices": ["20", "21", "22", "23", "24"],
        "has_wild_surge": True,
    }
}

def initialize_run_state():
    return {
        "remaining_wild_surges": list(WILD_SURGES.keys())
    }

def generate_shop_encounter(rarity1, rarity2):
    shop_inventory = {}

    # Special case: if both are "legendary", generate exactly 3 legendary items per category
    if rarity1 == "legendary" and rarity2 == "legendary":
        for category in MAGIC_ITEMS["legendary"].keys():
            items = []
            for _ in range(3):
                item_list = MAGIC_ITEMS["legendary"][category]
                selected = random.choice(item_list)

                if category == "Scroll" and selected == "generate":
                    items.append(generate_scroll_for_rarity("legendary"))
                elif category == "Armor" and selected == "enspelled":
                    items.append(generate_enspell_armor("legendary"))
                elif category == "Staff" and selected == "enspelled":
                    items.append(generate_enspell_staff("legendary"))
                elif category == "Weapon" and selected == "enspelled":
                    items.append(generate_enspell_weapon("legendary"))
                else:
                    items.append(selected)

            shop_inventory[category] = items

    # Default case: normal 2:1 mix
    for category in MAGIC_ITEMS[rarity1].keys():
        # Decide the 2:1 rarity distribution
        if random.choice([True, False]):
            primary, secondary = rarity1, rarity2
        else:
            primary, secondary = rarity2, rarity1

        items = []

        # Generate 2 items from primary rarity
        for _ in range(2):
            item_list = MAGIC_ITEMS[primary][category]
            selected = random.choice(item_list)

            if category == "Scroll" and selected == "generate":
                items.append(generate_scroll_for_rarity(primary))
            elif category == "Armor" and selected == "enspelled":
                items.append(generate_enspell_armor(primary))
            elif category == "Staff" and selected == "enspelled":
                items.append(generate_enspell_staff(primary))
            elif category == "Weapon" and selected == "enspelled":
                items.append(generate_enspell_weapon(primary))
            else:
                items.append(selected)

        # Generate 1 item from secondary rarity
        item_list = MAGIC_ITEMS[secondary][category]
        selected = random.choice(item_list)

        if category == "Scroll" and selected == "generate":
            items.append(generate_scroll_for_rarity(secondary))
        elif category == "Armor" and selected == "enspelled":
            items.append(generate_enspell_armor(secondary))
        elif category == "Staff" and selected == "enspelled":
            items.append(generate_enspell_staff(secondary))
        elif category == "Weapon" and selected == "enspelled":
            items.append(generate_enspell_weapon(secondary))
        else:
            items.append(selected)

        shop_inventory[category] = items

    # 35% chance to add a Wondrous category
    if random.random() < 0.35:
        wondrous_items = []
        allowed_rarities = [rarity1, rarity2]
        for _ in range(3):
            chosen_rarity = random.choice(allowed_rarities)
            wondrous_items.append(get_random_wondrous_item(chosen_rarity))
        shop_inventory["Wondrous"] = wondrous_items

    return {
        "type": "Shop Encounter",
        "rarity_mix": {primary: 2, secondary: 1},
        "items_by_category": shop_inventory
    }

def generate_encounter(encounter_number, run_state):
    data = ENCOUNTER_DEFINITIONS.get(encounter_number)
    if not data:
        return {"error": "Encounter not found."}

    # Handle shop encounters
    if data.get("is_shop"):
        if "shop" in data:
            shop_data = generate_shop_encounter(*data["shop"])
            shop_data["total_gold"] = data.get("total_gold", 0)
            return shop_data
        return {"note": data.get("note", "Revisit to previous shop.")}

    # Handle combat encounters
    monsters = []

    if "monsters" in data:
        for cr, amount in data["monsters"]:
            if float(Fraction(str(cr))) < 20:
                monsters += random.sample(MONSTERS[cr], amount)

    # Add exactly one high CR monster from random choices
    if "random_cr_choices" in data:
        chosen_cr = random.choice(data["random_cr_choices"])
        monsters += random.sample(MONSTERS[chosen_cr], 1)

    # Prepare base encounter data
    encounter = {
        "monsters": monsters,
    }

    # Include optional fields if present
    optional_fields = ["gold", "xp", "total_xp", "is_levelup", "note", "magic_loot_count", "allowed_rarities"]
    for field in optional_fields:
        if field in data:
            encounter[field] = data[field]

    # Generate magic items with exactly one wondrous item max
    magic_items = []
    loot_count = data.get("magic_loot_count", 0)
    rarities = data.get("allowed_rarities", [])

    # Generate all normal magic items first
    for _ in range(loot_count):
        if rarities:
            magic_items.append(get_random_magic_item(random.choice(rarities)))

    # Then do a single 30% roll to upgrade one to a wondrous item
    if rarities and loot_count > 0 and random.random() < 0.3:
        wondrous_index = random.randrange(loot_count)
        chosen_rarity = random.choice(rarities)
        magic_items[wondrous_index] = get_random_wondrous_item(chosen_rarity)

    if magic_items:
        encounter["magic_items"] = magic_items

    # Only include rations if this is NOT the final encounter
    if encounter_number != 39:
        encounter["rations"] = data.get("rations", get_rations())
    
    if data.get("has_wild_surge"):
        if "remaining_wild_surges" not in run_state:
            run_state["remaining_wild_surges"] = list(WILD_SURGES.keys())

        remaining = run_state["remaining_wild_surges"]

        if not remaining:
            raise RuntimeError("No Wild Surges left to assign in this run")

        chosen_id = random.choice(remaining)
        remaining.remove(chosen_id)

        encounter["wild_surge"] = {
            "id": chosen_id,
            **WILD_SURGES[chosen_id]
    }

    return encounter

def generate_filtered_encounter(encounter_number):
    data = ENCOUNTER_DEFINITIONS.get(encounter_number)
    if not data:
        return {"error": "Encounter not found."}

    # Handle shop encounters
    if data.get("is_shop"):
        if "shop" in data:
            shop_data = generate_shop_encounter(*data["shop"])
            shop_data["total_gold"] = data.get("total_gold", 0)
            return shop_data
        return {"note": data.get("note", "Revisit to previous shop.")}

    # Handle combat encounters
    monsters = []
    if "random_cr_choices" in data:
        valid_crs = [cr for cr in data["random_cr_choices"] if cr in filtered_monsters and filtered_monsters[cr]]
        if valid_crs:
            chosen_cr = random.choice(valid_crs)
            monsters = random.sample(filtered_monsters[chosen_cr], 1)
        else:
            return {
                "monsters": [],
                "note": f"No valid monsters found for CRs: {data['random_cr_choices']} in Encounter {encounter_number}"
            }

    if "monsters" in data:
        skip_index = 1 if "random_cr_choices" in data else 0
        for i, (cr, amount) in enumerate(data["monsters"]):
            if i < skip_index:
                continue  # skip first monster, handled via random_cr_choices
            if cr in filtered_monsters and len(filtered_monsters[cr]) >= amount:
                monsters += random.sample(filtered_monsters[cr], amount)
            else:
                monsters += [f"[No monster for CR {cr}]"] * amount

    encounter = {
        "monsters": monsters,
    }

    optional_fields = ["gold", "xp", "total_xp", "is_levelup", "note", "magic_loot_count", "allowed_rarities", "rations"]
    for field in optional_fields:
        if field in data:
            encounter[field] = data[field]

    # Generate magic items with exactly one wondrous item max
    magic_items = []
    loot_count = data.get("magic_loot_count", 0)
    rarities = data.get("allowed_rarities", [])

    for _ in range(loot_count):
        if rarities:
            magic_items.append(get_random_magic_item(random.choice(rarities)))

    if rarities and loot_count > 0 and random.random() < 0.3:
        wondrous_index = random.randrange(loot_count)
        chosen_rarity = random.choice(rarities)
        magic_items[wondrous_index] = get_random_wondrous_item(chosen_rarity)

    if magic_items:
        encounter["magic_items"] = magic_items

    encounter["rations"] = data.get("rations", get_rations())

    return encounter

def generate_all_encounters(total_encounters):
    run_state = {}
    all_encounters = []
    for i in range(1, total_encounters + 1):
        encounter = generate_encounter(i, run_state)
        all_encounters.append(encounter)
    return all_encounters

def generate_all_filtered_encounters(total_encounters):
    all_filtered_encounters = []
    for i in range(1, total_encounters + 1):
        encounter = generate_filtered_encounter(i)
        all_filtered_encounters.append(encounter)
    return all_filtered_encounters