import random

monsters = {
    "1/4": ["Aarakocra Skirmisher", "Animated Broom", "Kenku", "Winged Kobold"],
    "1/2": ["Orc", "Hobgoblin", "Scout"]
}

magic_items = {
    "common": ["Potion Of Healing", "Scroll Of Light", "Driftglobe"],
    "uncommon": ["Bag Of Holding", "Cloak Of Elvenkind", "Boots Of Striding"]
}

def get_rations():
    roll = random.randint(1, 10)
    if roll <= 5:
        return 0
    elif roll <= 9:
        return 1
    else:
        2

def generate_encounter(encounter_number):
    if encounter_number == 1:
        encounter = {
            "monsters": random.sample(monsters["1/2"], 2) + random.sample(monsters["1/4"], 2),
            "xp": 600,
            "gold": 100,
            "magic_items": random.sample(magic_items["common"] + magic_items["uncommon"], 4),
            "rations": get_rations()
        }
        return encounter

encounter = generate_encounter(1)
for key, value in encounter.items():
    print(f"{key.capitalize()}: {value}")