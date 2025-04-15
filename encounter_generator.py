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
    "2": ["Allosaurus", "Animated Rug Of Smothering", "Ankheg", "Awakened Tree", "Azer Sentinel",
          "Bandit Captain", "Berserker", "Black Dragon Wyrmling", "Bronze Dragon Wyrmling", "Bulette Pup",
          "Carrion Crawler", "Centaur Trooper", "Cultist Fanatic", "Druid", "Ettercap",
          "Faerie Dragon Adult", "Gargoyle", "Gelatinous Cube", "Ghast", "Giant Boar",
          "Giant Constrictor Snake", "Giant Elk", "Gibbering Mouther", "Githzerai Monk", "Gnoll Pack Lord",
          "Green Dragon Wyrmling", "Grick", "Griffon", "Intellect Devourer", "Lizardfolk Geomancer",
          "Mage Apprentice", "Merrow", "Mimic", "Minotaur Skeleton", "Modron Pentadrone", "Myconid Sovereign",
          "Nothic", "Ochre Jelly", "Ogre", "Ogre Zombie", "Pegasus", "Peryton", "Plesiosaurus", "Polar Bear",
          "Poltergeist", "Priest", "Quaggoth", "Rhinoceros", "Saber-Toothed Tiger", "Sahuagin Priest",
          "Sea Hag", "Silver Dragon Wyrmling", "Spined Devil", "Swarm Of Stirgest", "Swarm Of Venomous Snakes",
          "Wererat", "White Dragon Wyrmling", "Will-o'-Wisp"],
    "3": ["Ankylosaurus", "Basilisk", "Bearded Devil", "Blue Dragon Wyrmling", "Bugbear Stalker", "Displacer Beast",
          "Doppelganger", "Flaming Skeleton", "Giant Scorpion", "Githyanki Soldier", "Goblin Hexer",
          "Golden Dragon Wyrmling", "Green Hag", "Grell", "Hell Hound", "Hobgoblin Captain", "Hook Horror",
          "Knight", "Kuo-toa Monitor", "Manticore", "Minotaur Of Baphomet", "Mummy", "Nightmare", "Owlbear",
          "Phase Spider", "Quaggoth Thonot", "Scout Captain", "Spectator", "Swarm Of Crawling Claws",
          "Swarm Of Lemures", "Vampire Familiar", "Warrior Veteran", "Werewolf", "Wight", "Winter Wolf",
          "Yeti", "Yuan-ti Malison"],
    "4": ["Aarakocra Aeromancer", "Archelon", "Banshee", "Black Pudding", "Bone Naga", "Bullywug Bog Sage",
          "Chuul", "Couatl", "Elephant", "Ettin", "Flameskull", "Ghost", "Gnoll Fang Of Yeenoghu",
          "Guard Captain", "Helmed Horror", "Hippopotamus", "Incubus", "Juvenile Shadow Dragon", "Lamia",
          "Lizardfolk Sovereign", "Red Dragon Wyrmling", "Shadow Demon", "Succubus", "Swarm Of Dretches",
          "Tough Boss", "Wereboar", "Weretiger"],
    "5": ["Air Elemental", "Barded Devil", "Barlgura", "Beholder Zombie", "Bulette", "Cambion", "Earth Elemental",
          "Fire Elemental", "Flesh Golem", "Giant Axe Beak", "Giant Crocodile", "Gladiator", "Gorgon",
          "Half-Dragon", "Hill Giant", "Mezzoloth", "Night Hag", "Otyugh", "Pixie Wonderbringer", "Red Slaad",
          "Revenant", "Roper", "Sahuagin Baron", "Salamander", "Shambling Mound", "Triceratops", "Troll",
          "Umber Hulk", "Unicorn", "Vampire Spawn", "Water Elemental", "Werebear", "Wraith", "Xorn",
          "Young Remorhaz"],
    "6": ["Azer Pyromancer", "Chasme", "Chimera", "Cyclops Sentry", "Drider", "Galeb Duhr", "Ghast Gravecaller",
          "Githzerai Zerth", "Hobgoblin Warlord", "Invisible Stalker", "Kuo-toa Archpriest", "Mage", "Mammoth",
          "Medusa", "Merfolk Wavebender", "Performer Maestro", "Pirate Captain", "Satyr Revelmaster", "Vrock",
          "Wyvern", "Young Brass Dragon", "Young White Dragon"],
    "7": ["Bandit Deceiver", "Blue Slaad", "Centaur Warden", "Giant Ape", "Graveyard Revenant", "Grick Ancient",
          "Mind Flayer", "Oni", "Primeval Owlbear", "Shield Guardian", "Stone Giant", "Tree Blight",
          "Violet Fungus Necrohulk", "Young Black Dragon", "Young Copper Dragon", "Yuan-ti Abomination"],
    "8": ["Aberrant Cultist", "Assassin", "Berserker Commander", "Chain Devil", "Cloaker", "Cockatrice Regent",
          "Death Cultist", "Elemental Cultist", "Fiend Cultist", "Fomorian", "Frost Giant", "Githyanki Knight",
          "Gnoll Demoniac", "Green Slaad", "Hezrou", "Hydra", "Sphinx Of Secrets", "Spirit Naga",
          "Thri-kreen Psion", "Tyrannosaurus Rex", "Vampire Nightbringer", "Young Bronze Dragon",
          "Young Green Dragon"],
    "9": ["Abominable Yeti", "Bone Devil", "Brazen Gorgon", "Clay Golem", "Cloud Giant", "Fire Giant",
          "Glabrezu", "Gray Slaad", "Nycaloth", "Treant", "Young Blue Dragon", "Young Silver Dragon"],
    "10": ["Aboleth", "Cultist Hierophant", "Cyclops Oracle", "Death Slaad", "Deva", "Dire Worg",
           "Guardian Naga", "Haunting Revenant", "Noble Prodigy", "Performer Legend", "Spy Master",
           "Stone Golem", "Warrior Commander", "Yochlol", "Young Gold Dragon", "Young Red Dragon"],
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