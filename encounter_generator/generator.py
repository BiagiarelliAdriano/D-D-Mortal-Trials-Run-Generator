import random
from encounter_generator.data.blessings import DIVINE_BLESSINGS
from encounter_generator.data.constants import possible_rarities, enspell_levels_by_rarity
from encounter_generator.data.items import MAGIC_ITEMS, WONDROUS_ITEMS
from encounter_generator.data.spells import SPELLS

def generate_divine_blessing():
    return random.choice(DIVINE_BLESSINGS)

def get_rations():
    roll = random.randint(1, 10)
    if roll <= 6:
        return 0
    elif roll <= 9:
        return 1
    else:
        return 2

def get_random_magic_item(rarity):
    category = random.choice(list(MAGIC_ITEMS[rarity].keys()))
    item_list = MAGIC_ITEMS[rarity][category]
    selected = random.choice(item_list)

    if category == "Scroll" and selected == "generate":
        return generate_scroll_for_rarity(rarity)
    elif category == "Armor" and selected == "enspelled":
        return generate_enspell_armor(rarity)
    elif category == "Staff" and selected == "enspelled":
        return generate_enspell_staff(rarity)
    elif category == "Weapon" and selected == "enspelled":
        return generate_enspell_weapon(rarity)
    else:
        return selected

def get_random_wondrous_item(rarity):
    categories = ["Arcana", "Armaments", "Implements", "Relics"]
    chosen_category = random.choice(categories)
    items = WONDROUS_ITEMS.get(rarity, {}).get(chosen_category, [])
    if not items:
        return f"{rarity.capitalize()} Wondrous Item ({chosen_category})"
    
    return random.choice(items)

def generate_scroll_for_rarity(rarity):
    levels = possible_rarities[rarity]
    level = random.choice(levels)
    spell = random.choice(SPELLS[level])["name"]
    level_label = "Cantrip" if level == 0 else f"Level {level}"
    return f"Spell Scroll {level_label} {spell}"

def generate_enspell_armor(rarity):
    levels = enspell_levels_by_rarity.get(rarity, [0])
    level = random.choice(levels)
    spell = random.choice(SPELLS[level])["name"]
    
    level_label = "Cantrip" if level == 0 else f"Level {level}"
    
    valid_armors = [armor for armor in MAGIC_ITEMS["common"]["Armor"] if armor != "Shield"]
    base_armor = random.choice(valid_armors)
    
    return f"Enspelled {base_armor} {level_label} {spell}"

def generate_enspell_staff(rarity):
    levels = enspell_levels_by_rarity.get(rarity, [0])
    level = random.choice(levels)
    spell = random.choice(SPELLS[level])["name"]
    
    level_label = "Cantrip" if level == 0 else f"Level {level}"
    
    return f"Enspelled Staff {level_label} {spell}"

def generate_enspell_weapon(rarity):
    levels = enspell_levels_by_rarity.get(rarity, [0])
    level = random.choice(levels)
    spell = random.choice(SPELLS[level])["name"]
    
    level_label = "Cantrip" if level == 0 else f"Level {level}"
    
    valid_weapons = [weapon for weapon in MAGIC_ITEMS["common"]["Weapon"]]
    base_weapon = random.choice(valid_weapons)
    
    return f"Enspelled {base_weapon} {level_label} {spell}"