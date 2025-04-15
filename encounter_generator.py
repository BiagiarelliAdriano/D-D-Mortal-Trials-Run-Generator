import random

monsters = {
    "1/4": ["Aarakocra Skirmisher", "Animated Broom", "Animated Flying Sword", "Axe Beak", "Blink Dog",
            "Boar", "Bullywug Warrior", "Constrictor Snake", "Draft Horse", "Dretch", "Elk",
            "Giant Badger", "Giant Bat", "Giant Centipede", "Giant Frog", "Giant Lizard", "Giant Owl",
            "Giant Venomous Snake", "Giant Wolf Spider", "Goblin Warrior", "Grimlock", "Kenku",
            "Kuo-toa", "Modron Duodrone", "Mud Mephit", "Needle Blight", "Panther", "Pixie",
            "Priest Acolyte", "Pseudodragon", "Pteranodon", "Riding Horse", "Skeleton", "Smoke Mephit",
            "Sprite", "Steam Mephit", "Swarm Of Bats", "Swarm Of Rats", "Swarm Of Ravens",
            "Troglodyte", "Violet Fungus", "Winged Kobold", "Wolf", "Zombie"],
    "1/2": ["Ape", "Black Bear", "Cockatrice", "Crocodile", "Darkmantle", "Dust Mephit",
            "Gas Spore Fungus", "Giant Goat", "Giant Wasp", "Gnoll Warrior", "Gray Ooze",
            "Hobgoblin Warrior", "Ice Mephit", "Jackalwere", "Magma Mephit", "Magmin", "Modron Tridrone",
            "Myconid Adult", "Perfomer", "Piercer", "Rust Monster", "Sahuagin Warrior", "Satyr",
            "Scout", "Shadow", "Swarm Of Insects", "Tough", "Troll Limb", "Vine Blight", "Warhorse",
            "Warhorse Skeleton", "Worg"],
    "1": ["Animated Armor", "Brass Dragon Wyrmling", "Brown Bear", "Bugbear Warrior", "Copper Dragon Wyrmling",
          "Death Dog", "Dire Wolf", "Dryad", "Empyrean Iota", "Faerie Dragon Youth", "Ghoul", "Giant Eagle",
          "Giant Hyena", "Giant Spider", "Giant Toad", "Giant Vulture", "Goblin Boss", "Harpy",
          "Hippogriff", "Imp", "Kuo-toa Whip", "Lacedon Ghoul", "Lion", "Manes Vaporspawn",
          "Modron Quadrone", "Myconid Spore Servant", "Ogrillon Ogre", "Pirate", "Psychic Gray Ooze",
          "Quasit", "Salamander Fire Snake", "Scarecrow", "Specter", "Sphinx Of Wonder", "Spy",
          "Swarm Of Larvae", "Thri-kreen Marauder", "Tiger", "Yuan-ti Infiltrator"],
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