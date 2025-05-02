import random
import time

divine_blessings = [
    {
        "name": "Aquila",
        "title": "Eye Of Twilight",
        "description": """Aquila, the God of the sky, celestial bodies, and the cycle of day and night,
            was also the God that once had the largest realm. They reside above the heavens, encompassing
            and watching over the entire world. In most legends, Aquila's pride does not obscure their kindness.
            They gaze upon humanity, warming the earth and bringing down life-giving rain. However, they can also
            transform into the most fearsome calamity, harshly punishing any who dare to overcome the sky. Legends
            depict Aquila as a colossal sky-bird with a hundred eyes. When their eyes open, light fills the world,
            and when their eyelids fall, darkness envelops the land. Aquila is also the God of creation and invention.""",
        "blessing": """At any given moment, once per run, you immediately know the position of all enemies on the battlefield,
            and until the start of the next round, you gain the benefits of the Haste spell, you have Advantage with all attacks
            and enemies have Disadvantage with any Saving Throw caused by you."""
    },
    {
        "name": "Cerces",
        "title": "Bough Of Rift",
        "description": """Cerces is the master of wisdom, intellect, and vegetation. They wield authority over ecologies, knowledge,
            and rationality, and people refer to them as the hermit in search of wisdom. Nature is Cerces' courtyard and also their
            library. They allow people to study and rest there, and convey their knowledge to the ignorant tirelessly and generously.
            Cerces graces the world in the form of a grand and holy tree. Where they take root, vegetation sprouts to become
            massive forest.""",
        "blessing": """For this run, at the beginning of combat, gain 1d4 Temporary Hit Points. At any given moment, once per run,
            if you would fail a Saving Throw, you can choose to succeed instead. The next time you fall to 0 HP, regain this Blessing."""
    },
    {
        "name": "Georios",
        "title": "Pillar Of Stone",
        "description": """Georios is the God of earth. The skies and the seas were also born of their dormant breath. Mythology
            believes that every mountain range was once a physical manifestation of Georios. They are the largest, gentlest,
            and most benevolent God that protects the mortal world. Georios is also the God of agriculture and history.""",
        "blessing": """At any given moment, once per run, until the start of the next round, you gain +4AC and if you are hit
            by an attack, you reduce incoming damage by 20"""
    },
    {
        "name": "Janus",
        "title": "Gate Of Infinity",
        "description": """Janus is the God of passages and roads. They know the existence and ends of all paths. Janus' power can open
            the doors to all broken mortal worlds, create non-existent paths, and point to unseen directions. Janus is the God most
            revered by humanity. They created roads and connected cities. The passages that Janus rules over are not just doors
            humans traverse through, but also the path that connects destiny. They reveal fate through prophecies and point the way
            forward for humanity. Janus made countless roads, as well as countless choices. They guide humans to the correct path, so
            mankind will avoid the destiny of confusion. Very few are aware that the God of doors is also the God of isolation and
            imprisonment.""",
        "blessing": """At any given moment, once per run, you can change the position of each creature, including characters,
            on the battlefield however you want, inside the battlefield. After the changes, until the end of the current round,
            you have double your speed and enemies cannot move."""
    },
    {
        "name": "Kephale",
        "title": "Throne Of Worlds",
        "description": """Kephale is the omniscient, omnipotent God of original creation that holds up the skies. Kephale was born from
            the combination of lightning bolts from the skies striking the spine of the earth. They were then given the duty of the creation
            of life. The first humans were created in Kephale's own image and given life. Kephale loved these tiny beings so deeply that their
            majestic figure would always remain in the mortal world to accompany them.""",
        "blessing": """At any given moment, you can either make an attack you just missed hit instead or make an attack that would hit you
            miss instead. Once you use this Blessing, you regain it after scoring a Critical Hit. Each time you regain this Blessing,
            the number of Critical Hits required to restore it increases by 1."""
    },
    {
        "name": "Mnestia",
        "title": "Chrysalis Of Gold",
        "description": """Mnestia is the God that symbolizes beauty and love. Their appearance is often illustrated as a beautiful and elusive
            butterfly with golden patterns carved into their wings. They pursue beauty in the world, weave it into the golden thread, spin the
            romances of humankind and grant everyone love and affection.""",
        "blessing": """At any given moment, once per run, gain 30 Temporary Hit Points. If you take any damage while having these Temporary
            Hit Points, the creature that dealt damage is Charmed by you. At the end of the current round after using this Blessing, remove
            all remaining Temporary Hit Points you have and heal Hit Points by the same amount."""
    },
    {
        "name": "Nikador",
        "title": "Lance Of Fury",
        "description": """Nikador is the God of strife and competition. He is portrayed as a noble warrior that wears pure white sacred armor.
            Legend has it that the Lance of Fury that they wield can raze even the most powerful and prosperous city to the ground.
            Their bloodthirsty temperament has also made them a God of blood and sacrifice. Warriors gather under them and yearn to follow
            Nikador into war and achieve an honorable death.""",
        "blessing": """At any given moment, once per combat, you can add 1d4 to any attack roll or damage roll. At any given moment, once per run,
            if you are Bloodied, you gain the following benefits for the rest of the combat or until you are no longer Bloodied:
            'You are resistant to Bludgeoning, Piercing and Slashing damage, you add 1d6 to attack rolls and damage rolls, and after inflicting damage
            to a creature, heal for half of the damage inflicted'."""
    },
    {
        "name": "Oronyx",
        "title": "Veil Of Evernight",
        "description": """Oronyx is the God of time and night. Before the first dawn of the universe, the world was caged in the purest darkness.
            When the borders and day and night were separated, the young Oronyx jolted awake from the newborn concept of time, heading toward
            the outer reaches of the universe alone. There, they materialized as the Evernight Veil and henceforth remained afar from humanity,
            quietly spending their time managing the fabric of time.""",
        "blessing": """For this run, each character starts with the Lucky feat. If they already have the Lucky feat, they gain 1 use more for it."""
    },
    {
        "name": "Phagousa",
        "title": "Chalice Of Plenty",
        "description": """Phagousa is the God that controls oceans and storms, as well as the master of honey brew and banquets. They are capable
            of freely moving bodies of water across any place as they please. According to mythology, they are a capricious and pleasure-obsessed
            God that sees the oceans as their place of alcoholic revelry. Phagousa also bears the duty of washing clean the filth of the world.
            Baths that have received the benediction of the God are able to not only clean the body of impurities, but can also cleanse the wounds
            of the soul. They are an irreplaceable joy in the lives of all people. At the same time, Phagousa is also the God of banquets and
            drunkenness. They passed on the art of brewing to humanity and taught them the first songs and dances with the ocean breeze and waves.""",
        "blessing": """For this run, each Healing Potion recovers the maximum amount of Hit Points they can give. The first time a character drinks
            a Healing Potion, there is a 20 percent chance to gain 1 level of Exhaustion. Each subsequent time a character drinks a Healing Potion
            without gaining the level of Exhaustion or before taking a Long Rest, the chance doubles."""
    },
    {
        "name": "Talanton",
        "title": "Scale Of Justice",
        "description": """Talanton is the God of law and justice. They rarely appear in the mortal world in physical form and there are almost no records
            of them in legend. People often say that they are the rules of destiny, the law of all things, and the divine retribution for violation of such
            rules and laws. Talanton is seen as a manifestation of justice. They uphold the taboos and boundaries of the world and lay down logic and laws
            for all things. They created all currencies to ensure that all transactions are of equivalent exchange. They maintain the balance of the world.
            Any action that would damage these laws will be subject to retribution. Just as a scale that never tilts, all things must be free of excess.
            If one wishes to obtain, they must first lose.""",
        "blessing": """At any given moment, once per run, for the rest of the combat, you can gain 6 points to any three of your statistics, but lose
            6 points from the other three."""
    },
    {
        "name": "Thanatos",
        "title": "Hand Of Shadow",
        "description": """Thanatos is the God of death and annihilation, and no one knows their true form - for the dead cannot relay legends
            to the living. It is said that their touch causes flowers to wither, soil to crack, metal to corrode, and flesh to turn to ashes - everything
            shrouded in thick, dark mist and disintegrating into meaningless fragments.""",
        "blessing": """Once per run, when you would die, return to consciousness standing with half maximum HP. At the end of the current combat,
            if you have not recovered any amount of Hit Points from any source other than this Blessing, you die."""
    },
    {
        "name": "Zagreus",
        "title": "Coin Of Whimsy",
        "description": """Zagreus is the God of lies and fortune. The true Zagreus is often depicted as a two-faced God who is both smiling
            and crying. Its two parts are much like the coexistence of lies and truth in the world. One cannot exist without the other.
            Zagreus has no interest in fulfilling their divine duties. They love to cause divisions in the paths of the Gods and play tricks
            to sow chaos and disorder. They do not have their own altars or temples, either. This is because even Zagreus' disciples would not
            worship such a God. Thus, they become the God of the poor and unremarkable. Legend states that they often appear in barren desert
            areas to provide people with unpredictable opportunities and change. Before setting out on a long journey, people would often curse
            the name of Zagreus to reduce the chances of them encountering thieves or ill fortune. They would also offer up prayers in times of
            suffering, in the hopes of everything suddenly turning around. This is precisely the reason that they are tolerated. Nothing is perfect,
            and no truth remains eternal. Change and carelessness can be fatal, but they can also be a savior in a critical moment.""",
        "blessing": """At any given moment, you can consume one magical item to gain 1d4 x 200 gold pieces. If you consume one legendary magical item,
            also get a random card from the Deck of Wonder that activates immediately."""
    }
]

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
    "11": ["Bandit Crime Lord", "Behir", "Dao", "Death Knight Aspirant", "Djinni", "Efreeti",
           "Horned Devil", "Marid", "Mind Flayer Arcanist", "Remorhaz", "Roc", "Sphinx Of Lore"],
    "12": ["Arcanaloth", "Archmage", "Archpriest", "Erinyes", "Githzerai Psion", "Pirate Admiral",
           "Questing Knight"],
    "13": ["Adult Brass Dragon", "Adult White Dragon", "Beholder", "Nalfeshnee", "Rakshasa",
           "Shadow Dragon", "Storm Giant", "Ultroloth", "Vampire"],
    "14": ["Adult Black Dragon", "Adult Copper Dragon", "Death Tyrant", "Ice Devil"],
    "15": ["Adult Bronze Dragon", "Adult Green Dragon", "Mummy Lord", "Purple Worm",
           "Salamander Inferno Master", "Vampire Umbral Lord"],
    "16": ["Adult Blue Dragon", "Adult Silver Dragon", "Githyanki Dracomancer", "Gulthias Blight",
           "Iron Golem", "Marilith", "Planetar"],
    "17": ["Adult Gold Dragon", "Adult Red Dragon", "Death Knight", "Dracolich", "Dragon Turtle",
           "Goristro", "Sphinx Of Valor"],
    "18": ["Demilich"],
    "19": ["Balor"],
    "20": ["Ancient Brass Dragon", "Ancient White Dragon", "Animal Lord", "Pit Fiend"],
    "21": ["Ancient Black Dragon", "Ancient Copper Dragon", "Arch-hag", "Lich", "Solar"],
    "22": ["Ancient Bronze Dragon", "Ancient Green Dragon", "Elemental Cataclysm"],
    "23": ["Ancient Blue Dragon", "Ancient Silver Dragon", "Blob Of Annihilation", "Empyrean",
           "Kraken"],
    "24": ["Ancient Gold Dragon", "Ancient Red Dragon"],
}

spells = {
    0: [
        {"name": "Acid Splash", "school": "Evocation"},
        {"name": "Blade Ward", "school": "Abjuration"},
        {"name": "Chill Touch", "school": "Necromancy"},
        {"name": "Eldritch Blast", "school": "Evocation"},
        {"name": "Fire Bolt", "school": "Evocation"},
        {"name": "Guidance", "school": "Divination"},
        {"name": "Light", "school": "Evocation"},
        {"name": "Mage Hand", "school": "Conjuration"},
        {"name": "Mending", "school": "Transmutation"},
        {"name": "Mind Sliver", "school": "Enchantment"},
        {"name": "Poison Spray", "school": "Necromancy"},
        {"name": "Produce Flame", "school": "Conjuration"},
        {"name": "Ray Of Frost", "school": "Evocation"},
        {"name": "Resistance", "school": "Abjuration"},
        {"name": "Sacred Flame", "school": "Evocation"},
        {"name": "Shillelagh", "school": "Transmutation"},
        {"name": "Shocking Grasp", "school": "Evocation"},
        {"name": "Sorcerous Burst", "school": "Evocation"},
        {"name": "Spare The Dying", "school": "Necromancy"},
        {"name": "Starry Wisp", "school": "Evocation"},
        {"name": "Thorn Whip", "school": "Transmutation"},
        {"name": "Thunderclap", "school": "Evocation"},
        {"name": "Toll The Dead", "school": "Necromancy"},
        {"name": "True Strike", "school": "Divination"},
        {"name": "Vicious Mockery", "school": "Enchantment"},
        {"name": "Word Of Radiance", "school": "Evocation"},
    ],
    1: [
        {"name": "Armor Of Agathys", "school": "Abjuration"},
        {"name": "Arms Of Hadar", "school": "Conjuration"},
        {"name": "Bane", "school": "Enchantment"},
        {"name": "Bless", "school": "Enchantment"},
        {"name": "Burning Hands", "school": "Evocation"},
        {"name": "Charm Person", "school": "Enchantment"},
        {"name": "Chromatic Orb", "school": "Evocation"},
        {"name": "Color Spray", "school": "Illusion"},
        {"name": "Command", "school": "Enchantment"},
        {"name": "Compelled Duel", "school": "Enchantment"},
        {"name": "Cure Wounds", "school": "Abjuration"},
        {"name": "Detect Evil And Good", "school": "Divination"},
        {"name": "Detect Magic", "school": "Divination"},
        {"name": "Dissonant Whispers", "school": "Enchantment"},
        {"name": "Divine Favor", "school": "Transmutation"},
        {"name": "Divine Smite", "school": "Evocation"},
        {"name": "Ensnaring Strike", "school": "Conjuration"},
        {"name": "Entangle", "school": "Conjuration"},
        {"name": "Expeditious Retreat", "school": "Transmutation"},
        {"name": "Faerie Fire", "school": "Evocation"},
        {"name": "False Life", "school": "Necromancy"},
        {"name": "Feather Fall", "school": "Transmutation"},
        {"name": "Find Familiar", "school": "Conjuration"},
        {"name": "Fog Cloud", "school": "Conjuration"},
        {"name": "Goodberry", "school": "Conjuration"},
        {"name": "Grease", "school": "Conjuration"},
        {"name": "Guiding Bolt", "school": "Evocation"},
        {"name": "Hail Of Throns", "school": "Conjuration"},
        {"name": "Healing Word", "school": "Abjuration"},
        {"name": "Hellish Rebuke", "school": "Evocation"},
        {"name": "Heroism", "school": "Enchantment"},
        {"name": "Hex", "school": "Enchantment"},
        {"name": "Hunter's Mark", "school": "Divination"},
        {"name": "Ice Knife", "school": "Conjuration"},
        {"name": "Inflict Wounds", "school": "Necromancy"},
        {"name": "Jump", "school": "Transmutation"},
        {"name": "Longstridedr", "school": "Transmutation"},
        {"name": "Mage Armor", "school": "Abjuration"},
        {"name": "Magic Missile", "school": "Evocation"},
        {"name": "Protection From Evil And Good", "school": "Abjuration"},
        {"name": "Ray Of Sickness", "school": "Necromancy"},
        {"name": "Sanctuary", "school": "Abjuration"},
        {"name": "Searing Smite", "school": "Evocation"},
        {"name": "Shield", "school": "Abjuration"},
        {"name": "Shield Of Faith", "school": "Abjuration"},
        {"name": "Sleep", "school": "Enchantment"},
        {"name": "Tasha's Hideous Laughter", "school": "Enchantment"},
        {"name": "Thunderous Smite", "school": "Evocation"},
        {"name": "Thunderwave", "school": "Evocation"},
        {"name": "With Bolt", "school": "Evocation"},
        {"name": "Wrathful Smite", "school": "Necromancy"},
    ],
    2: [
        {"name": "Aid", "school": "Abjuration"},
        {"name": "Arcane Lock", "school": "Abjuration"},
        {"name": "Arcane Vigor", "school": "Abjuration"},
        {"name": "Barkskin", "school": "Transmutation"},
        {"name": "Blindness/Deafness", "school": "Transmutation"},
        {"name": "Blur", "school": "Illusion"},
        {"name": "Cloud Of Daggers", "school": "Conjuration"},
        {"name": "Continual Flame", "school": "Evocation"},
        {"name": "Cordon Of Arrows", "school": "Transmutation"},
        {"name": "Crown Of Madness", "school": "Enchantment"},
        {"name": "Darkness", "school": "Evocation"},
        {"name": "Dragon's Breath", "school": "Transmutation"},
        {"name": "Enchance Ability", "school": "Transmutation"},
        {"name": "Enlarge/Reduce", "school": "Transmutation"},
        {"name": "Find Steed", "school": "Conjuration"},
        {"name": "Flame Blade", "school": "Evocation"},
        {"name": "Flaming Sphere", "school": "Conjuration"},
        {"name": "Gust Of Wind", "school": "Evocation"},
        {"name": "Heat Metal", "school": "Transmutation"},
        {"name": "Hold Person", "school": "Enchantment"},
        {"name": "Invisibility", "school": "Illusion"},
        {"name": "Lesser Restoration", "school": "Abjuration"},
        {"name": "Levitate", "school": "Transmutation"},
        {"name": "Magic Weapon", "school": "Transmutation"},
        {"name": "Melf's Acid Arrow", "school": "Evocation"},
        {"name": "Mind Spike", "school": "Divination"},
        {"name": "Mirror Image", "school": "Illusion"},
        {"name": "Misty Step", "school": "Conjuration"},
        {"name": "Moonbeam", "school": "Evocation"},
        {"name": "Nystul's Magic Aura", "school": "Illusion"},
        {"name": "Phantasmal Force", "school": "Illusion"},
        {"name": "Prayer Of Healing", "school": "Abjuration"},
        {"name": "Protection From Poison", "school": "Abjuration"},
        {"name": "Ray Of Enfeeblement", "school": "Necromancy"},
        {"name": "Scorching Ray", "school": "Evocation"},
        {"name": "See Invisibility", "school": "Divination"},
        {"name": "Shatter", "school": "Evocation"},
        {"name": "Shining Smite", "school": "Transmutation"},
        {"name": "Silence", "school": "Illusion"},
        {"name": "Spider Climb", "school": "Transmutation"},
        {"name": "Spike Growth", "school": "Transmutation"},
        {"name": "Spiritual Weapon", "school": "Evocation"},
        {"name": "Summon Beast", "school": "Conjuration"},
        {"name": "Warding Bond", "school": "Abjuration"},
        {"name": "Web", "school": "Conjuration"},
    ],
    3: [
        {"name": "Animate Dead", "school": "Necromancy"},
        {"name": "Aura Of Vitality", "school": "Abjuration"},
        {"name": "Beacon Of Hope", "school": "Abjuration"},
        {"name": "Bestow Curse", "school": "Necromancy"},
        {"name": "Blinding Smite", "school": "Evocation"},
        {"name": "Blink", "school": "Transmutation"},
        {"name": "Call Lightning", "school": "Conjuration"},
        {"name": "Conjure Animals", "school": "Conjuration"},
        {"name": "Conjure Barrage", "school": "Conjuration"},
        {"name": "Counterspell", "school": "Abjuration"},
        {"name": "Crusader's Mantle", "school": "Evocation"},
        {"name": "Daylight", "school": "Evocation"},
        {"name": "Dispel Magic", "school": "Abjuration"},
        {"name": "Elemental Weapon", "school": "Transmutation"},
        {"name": "Fear", "school": "Illusion"},
        {"name": "Feign Death", "school": "Necromancy"},
        {"name": "Fireball", "school": "Evocation"},
        {"name": "Fly", "school": "Transmutation"},
        {"name": "Gaseous Form", "school": "Transmutation"},
        {"name": "Glyph Of Warding", "school": "Abjuration"},
        {"name": "Haste", "school": "Transmutation"},
        {"name": "Hunger Of Hadar", "school": "Conjuration"},
        {"name": "Hypnotic Pattern", "school": "Illusion"},
        {"name": "Lightning Arrow", "school": "Transmutation"},
        {"name": "Lightning Bolt", "school": "Evocation"},
        {"name": "Magic Circle", "school": "Abjuration"},
        {"name": "Mass Healing Word", "school": "Abjuration"},
        {"name": "Meld Into Stone", "school": "Transmutation"},
        {"name": "Phantom Steed", "school": "Illusion"},
        {"name": "Plant Growth", "school": "Transmutation"},
        {"name": "Protection From Energy", "school": "Abjuration"},
        {"name": "Remove Curse", "school": "Abjuration"},
        {"name": "Revivify", "school": "Necromancy"},
        {"name": "Sleet Storm", "school": "Conjuration"},
        {"name": "Slow", "school": "Transmutation"},
        {"name": "Spirit Guardians", "school": "Conjuration"},
        {"name": "Stinking Cloud", "school": "Conjuration"},
        {"name": "Summon Fey", "school": "Conjuration"},
        {"name": "Summon Undead", "school": "Necromancy"},
        {"name": "Vampiric Touch", "school": "Necromancy"},
        {"name": "Wind Wall", "school": "Evocation"},
    ],
    4: [
        {"name": "Aura Of Life", "school": "Abjuration"},
        {"name": "Aura Of Purity", "school": "Abjuration"},
        {"name": "Banishment", "school": "Abjuration"},
        {"name": "Blight", "school": "Necromancy"},
        {"name": "Charm Monster", "school": "Enchantment"},
        {"name": "Compulsion", "school": "Enchantment"},
        {"name": "Confusion", "school": "Enchantment"},
        {"name": "Conjure Minor Elementals", "school": "Conjuration"},
        {"name": "Conjure Woodlands Beings", "school": "Conjuration"},
        {"name": "Death Ward", "school": "Abjuration"},
        {"name": "Dimension Door", "school": "Conjuration"},
        {"name": "Dominate Beast", "school": "Enchantment"},
        {"name": "Evard's Black Tentacles", "school": "Conjuration"},
        {"name": "Fabricate", "school": "Transmutation"},
        {"name": "Fire Shield", "school": "Evocation"},
        {"name": "Fount Of Moonlight", "school": "Evocation"},
        {"name": "Freedom Of Movement", "school": "Abjuration"},
        {"name": "Gaint Insect", "school": "Conjuration"},
        {"name": "Grasping Vine", "school": "Conjuration"},
        {"name": "Greater Invisibility", "school": "Illusion"},
        {"name": "Guardian Of Faith", "school": "Conjuration"},
        {"name": "Hallucinatory Terrain", "school": "Illusion"},
        {"name": "Ice Storm", "school": "Evocation"},
        {"name": "Locate Creature", "school": "Divination"},
        {"name": "Mordenkainen's Faithful Hound", "school": "Conjuration"},
        {"name": "Otiluke's Resilient Sphere", "school": "Abjuration"},
        {"name": "Phantasmal Killer", "school": "Illusion"},
        {"name": "Polymorph", "school": "Transmutation"},
        {"name": "Staggering Smite", "school": "Enchantment"},
        {"name": "Stone Shape", "school": "Transmutation"},
        {"name": "Stoneskin", "school": "Transmutation"},
        {"name": "Summon Aberration", "school": "Conjuration"},
        {"name": "Summon Construct", "school": "Conjuration"},
        {"name": "Summon Elemental", "school": "Conjuration"},
        {"name": "Vitriolic Sphere", "school": "Evocation"},
        {"name": "Wall Of Fire", "school": "Evocation"},
    ],
    5: [
        {"name": "Animate Objects", "school": "Transmutation"},
        {"name": "Antilife Shell", "school": "Abjuration"},
        {"name": "Awaken", "school": "Transmutation"},
        {"name": "Banishing Smite", "school": "Conjuration"},
        {"name": "Bigby's Hand", "school": "Evocation"},
        {"name": "Circle Of Power", "school": "Abjuration"},
        {"name": "Cloudkill", "school": "Conjuration"},
        {"name": "Cone Of Cold", "school": "Evocation"},
        {"name": "Conjure Elemental", "school": "Conjuration"},
        {"name": "Conjure Volley", "school": "Conjuration"},
        {"name": "Contagion", "school": "Necromancy"},
        {"name": "Creation", "school": "Illusion"},
        {"name": "Destructive Wave", "school": "Evocation"},
        {"name": "Dispel Evil And Good", "school": "Abjuration"},
        {"name": "Dominate Person", "school": "Enchantment"},
        {"name": "Flame Strike", "school": "Evocation"},
        {"name": "Geas", "school": "Enchantment"},
        {"name": "Greater Restoration", "school": "Abjuration"},
        {"name": "Hallow", "school": "Abjuration"},
        {"name": "Hold Monster", "school": "Enchantment"},
        {"name": "Insect Plague", "school": "Conjuration"},
        {"name": "Jallarzi's Storm Of Radiance", "school": "Evocation"},
        {"name": "Mass Cure Wounds", "school": "Abjuration"},
        {"name": "Mislead", "school": "Illusion"},
        {"name": "Passwall", "school": "Transmutation"},
        {"name": "Raise Dead", "school": "Necromancy"},
        {"name": "Reincarnate", "school": "Necromancy"},
        {"name": "Steel Wind Strike", "school": "Conjuration"},
        {"name": "Summon Celestial", "school": "Conjuration"},
        {"name": "Summon Dragon", "school": "Conjuration"},
        {"name": "Swift Quiver", "school": "Transmutation"},
        {"name": "Synaptic Static", "school": "Enchantment"},
        {"name": "Telekinesis", "school": "Transmutation"},
        {"name": "Tree Stride", "school": "Conjuration"},
        {"name": "Wall Of Force", "school": "Evocation"},
        {"name": "Wall Of Stone", "school": "Evocation"},
        {"name": "Yolande's Regal Presence", "school": "Enchantment"},
    ],
    6: [
        {"name": "Arcane Gate", "school": "Conjuration"},
        {"name": "Blade Barrier", "school": "Evocation"},
        {"name": "Chain Lightning", "school": "Evocation"},
        {"name": "Circle Of Death", "school": "Necromancy"},
        {"name": "Conjure Fey", "school": "Conjuration"},
        {"name": "Contingency", "school": "Abjuration"},
        {"name": "Create Undead", "school": "Necromancy"},
        {"name": "Disintegrate", "school": "Transmutation"},
        {"name": "Eyebite", "school": "Necromancy"},
        {"name": "Flesh To Stone", "school": "Transmutation"},
        {"name": "Globe Of Invulnerability", "school": "Abjuration"},
        {"name": "Harm", "school": "Necromancy"},
        {"name": "Heal", "school": "Abjuration"},
        {"name": "Heroe's Feast", "school": "Conjuration"},
        {"name": "Move Earth", "school": "Transmutation"},
        {"name": "Otiluke's Freezing Sphere", "school": "Evocation"},
        {"name": "Otto's Irresistible Dance", "school": "Enchantment"},
        {"name": "Planar Ally", "school": "Conjuration"},
        {"name": "Summon Fiend", "school": "Conjuration"},
        {"name": "Sunbeam", "school": "Evocation"},
        {"name": "True Seeing", "school": "Divination"},
        {"name": "Wall Of Ice", "school": "Evocation"},
        {"name": "Wall Of Thorns", "school": "Conjuration"},
        {"name": "Wind Walk", "school": "Transmutation"},
    ],
    7: [
        {"name": "Conjure Celestial", "school": "Conjuration"},
        {"name": "Delayed Blast Fireball", "school": "Evocation"},
        {"name": "Divine Word", "school": "Evocation"},
        {"name": "Etherealness", "school": "Conjuration"},
        {"name": "Finger Of Death", "school": "Necromancy"},
        {"name": "Fire Storm", "school": "Evocation"},
        {"name": "Forcecage", "school": "Evocation"},
        {"name": "Mordenkainen's Sword", "school": "Evocation"},
        {"name": "Power Word Fortify", "school": "Enchantment"},
        {"name": "Primastic Spray", "school": "Evocation"},
        {"name": "Regenerate", "school": "Transmutation"},
        {"name": "Resurrection", "school": "Necromancy"},
        {"name": "Reverse Gravity", "school": "Transmutation"},
        {"name": "Sequester", "school": "Transmutation"},
        {"name": "Simulacrum", "school": "Illusion"},
        {"name": "Teleport", "school": "Conjuration"},
    ],
    8: [
        {"name": "Animal Shapes", "school": "Transmutation"},
        {"name": "Antimagic Field", "school": "Abjuration"},
        {"name": "Befuddlement", "school": "Enchantment"},
        {"name": "Clone", "school": "Necromancy"},
        {"name": "Dominate Monster", "school": "Enchantment"},
        {"name": "Earthquake", "school": "Transmutation"},
        {"name": "Holy Aura", "school": "Abjuration"},
        {"name": "Incendiary Cloud", "school": "Conjuration"},
        {"name": "Maze", "school": "Conjuration"},
        {"name": "Mind Blank", "school": "Abjuration"},
        {"name": "Power Word Stun", "school": "Enchantment"},
        {"name": "Sunburst", "school": "Evocation"},
        {"name": "Tsunami", "school": "Conjuration"},
    ],
    9: [
        {"name": "Foresight", "school": "Divination"},
        {"name": "Gate", "school": "Conjuration"},
        {"name": "Imprisonment", "school": "Abjuration"},
        {"name": "Mass Heal", "school": "Abjuration"},
        {"name": "Meteor Swarm", "school": "Evocation"},
        {"name": "Power Word Heal", "school": "Enchantment"},
        {"name": "Power Word Kill", "school": "Enchantment"},
        {"name": "Primastic Wall", "school": "Abjuration"},
        {"name": "Shapechange", "school": "Transmutation"},
        {"name": "Storm Of Vengeance", "school": "Conjuration"},
        {"name": "Time Stop", "school": "Transmutation"},
        {"name": "True Polymorph", "school": "Transmutation"},
        {"name": "True Resurrection", "school": "Necromancy"},
        {"name": "Weird", "school": "Illusion"},
    ],
}

magic_items = {
    "common": {
        "Armor": ["Breastplate", "Chain Mail", "Chain Shirt", "Half Plate Armor", "Hide Armor",
                  "Leather Armor", "Padded Armor", "Plate Armor", "Ring Mail",
                  "Scale Mail", "Shield", "Splint Armor", "Studded Leather Armor"],
        "Potion": ["Potion of Climbing", "Potion Of Healing"],
        "Ring": ["Ring"],
        "Rod": ["Rod"],
        "Scroll": ["generate"],
        "Staff": ["Staff"],
        "Wand": ["Wand"],
        "Weapon": ["Battleaxe", "Club", "Dagger", "Flail", "Glaive", "Greataxe", "Greatclub",
                   "Halberd", "Hand Crossbow", "Handaxe", "Heavy Crossbow", "Javelin", "Lance",
                   "Light Crossbow", "Light Hammer", "Longbow", "Longsword", "Mace", "Maul", "Morningstar",
                   "Pike", "Quarterstaff", "Rapier", "Scimitar", "Shortbow", "Shortsword", "Sickle", "Sling",
                   "Spear", "Trident", "War Pick", "Warhammer", "Whip"],
    },
    "uncommon": {
        "Armor": ["Adamantine Breastplate", "Adamantine Chain Mail", "Adamantine Half Plate Armor",
                  "Adamantine Plate Armor", "Adamantine Ring Mail", "Adamantine Scale Mail", "Adamantine Splint Armor",
                  "enspelled", "Mariner's Breastplate Armor", "Mariner's Chain Mail Armor", "Mariner's Chain Shirt Armor",
                  "Mariner's Half Plate Armor", "Mariner's Hide Armor", "Mariner's Leather Armor", "Mariner's Padded Armor",
                  "Mariner's Plate Armor", "Mariner's Ring Mail", "Mariner's Scale Mail", "Mariner's Splint Armor",
                  "Mariner's Studded Leather Armor", "Mithral Brestplate Armor", "Mithral Chain Mail Armor",
                  "Mithral Chain Shirt Armor", "Mithral Half Plate Armor", "Mithral Plate Armor", "Mithral Ring Mail Armor",
                  "Mithral Scale Mail Armor", "Mithral Splint Armor", "Sentinel Shield", "Shield +1"],
        "Potion": ["Oil Of Slipperiness", "Potion Of Fire Breath", "Potion Of Greater Healing", "Potion Of Growth",
                   "Potion Of Hill Giant Strength", "Potion Of Poison", "Potion Of Pugilism", "Potion Of Acid Resistance",
                   "Potion Of Cold Resistance", "Potion Of Fire Resistance", "Potion Of Force Resistance",
                   "Potion Of Lightning Resistance", "Potion Of Necrotic Resistance", "Potion Of Poison Resistance",
                   "Potion Of Psychic Resistance", "Potion Of Radiant Resistance", "Potion Of Thunder Resistance"],
        "Ring": ["Ring Of Jumping", "Ring Of Mind Shielding", "Ring Of Warmth"],
        "Rod": ["Immovable Rod", "Rod Of The Pact Keeper +1"],
        "Scroll": ["generate"],
        "Staff": ["enspelled", "Staff Of The Adder", "Staff Of The Python"],
        "Wand": ["Wand Of Magic Detection", "Wand Of Magic Missiles", "Wand Of Secrets", "Wand Of Web",
                 "Wand Of The War Mage +1"],
        "Weapon": ["Adamantine Battleaxe", "Adamantine Club", "Adamantine Dagger", "Adamantine Flail", "Adamantine Glaive",
                   "Adamantine Greataxe", "Adamantine Greatclub", "Adamantine Greatsword", "Adamantine Halberd", "Adamantine Handaxe",
                   "Adamantine Javelin", "Adamantine Lance", "Adamantine Light Hammer", "Adamantine Longsword", "Adamantine Mace",
                   "Adamantine Maul", "Adamantine Morningstar", "Adamantine Pike", "Adamantine Quarterstaff", "Adamantine Rapier",
                   "Adamantine Scimitar", "Adamantine Shortsword", "Adamantine Sickle", "Adamantine Spear", "Adamantine Trident",
                   "Adamantine War Pick", "Adamantine Warhammer", "Adamantine Whip", "Arrow +1", "Bolt +1", "enspelled",
                   "Javelin Of Lightning", "Glaive Of Vengeance", "Greatsword Of Vengeance", "Longsword Of Vengeance", "Rapier Of Vengeance",
                   "Scimitar Of Vengeance", "Shortsword Of Vengeance", "Trident Of Fish Command", "Battleaxe Of Warning", "Club Of Warning",
                   "Dagger Of Warning", "Flail Of Warning", "Glaive Of Warning", "Greataxe Of Warning", "Greatclub Of Warning",
                   "Greatsword Of Warning", "Halberd Of Warning", "Hand Crossbow Of Warning", "Javelin Of Warning", "Lance Of Warning",
                   "Light Crossbow Of Warning", "Light Hammer Of Warning", "Longbow Of Warning", "Longsword Of Warning", "Mace Of Warning",
                   "Maul Of Warning", "Morningstar Of Warning", "Pike Of Warning", "Quarterstaff Of Warning", "Rapier Of Warning",
                   "Scimitar Of Warning", "Shortbow Of Warning", "Shortsword Of Warning", "Sickle Of Warning", "Spear Of Warning", "Trident Of Warning",
                   "War Pick Of Warning", "Warhammer Of Warning", "Whip Of Warning", "Battleaxe +1", "Club +1", "Dagger +1", "Flail +1", "Glaive +1",
                   "Greataxe +1", "Greatclub +1", "Greatsword +1", "Halberd +1", "Hand Crossbow +1", "Handaxe +1", "Heavy Crossbow +1", "Javelin +1",
                   "Lance +1", "Light Crossbow +1", "Light Hammer +1", "Longbow +1", "Longsword +1", "Mace +1", "Maul +1", "Morningstar +1", "Pike +1",
                   "Quarterstaff +1", "Rapier +1", "Scimitar +1", "Shortbow +1", "Shortsword +1", "Sickle +1", "Spear +1", "Trident +1", "War Pick +1",
                   "Warhammer +1", "Whip +1"]
    },
    "rare": {
        "Armor": ["Armor Of Resistance", "Armor Of Vulnerability", "Armor +1", "enspelled", "Arrow-catching Shield", "Elven Chain",
                  "Glamoured Studded Leather", "Shield Of Missile Attraction", "Shield +2"],
        "Potion": ["Elixir Of Health", "Oil Of Etherealness", "Potion Of Diminution", "Potion Of Fire Giant Strength", "Potion Of Frost Giant Strength",
                   "Potion Of Gaseous Form", "Potion Of Heroism", "Potion Of Invisibility", "Potion Of Invulnerability", "Potion Of Mind Reading",
                   "Potion Of Stone Giant Strength", "Potion Of Superior Healing"],
        "Ring": ["Ring Of Animal Influence", "Ring Of Evasion", "Ring Of Feather Falling", "Ring Of Free Action", "Ring Of Protection",
                 "Ring Of Resistance", "Ring Of Spell Storing", "Ring Of X-Ray Vision", "Ring Of The Ram"],
        "Rod": ["Rod Of Rulership", "Rod Of The Pact Keeper +2", "Tentacle Rod"],
        "Scroll": ["generate"],
        "Staff": ["enspelled", "Staff Of Charming", "Staff Of Healing", "Staff Of Swarming Insects", "Staff Of Withering", "Staff Of The Woodlands"],
        "Wand": ["Wand Of Binding", "Wand Of Enemy Detection", "Wand Of Fear", "Wand Of Fireballs", "Wand Of Lightning Bolts", "Wand Of Paralysis",
                 "Wand Of Wonder", "Wand Of The War Mage +2"],
        "Weapon": ["Ammunition +2", "Berserker Axe", "Dagger Of Venom", "Dragon Slayer", "enspelled", "Flame Tongue", "Giant Slayer", "Mace Of Disruption",
                   "Mace Of Smiting", "Mace Of Terror", "Sun Blade", "Sword Of Life Stealing", "Sword Of Wounding", "Vicious Weapon", "Weapon +2"]
    },
    "very rare": {
        "Armor": ["Animated Shield", "Armor +2", "enspelled", "Demon Armor", "Dragon Scale Mail", "Dwarven Plate", "Shield +3", "Shield Of The Cavalier",
                  "Spellguard Shield"],
        "Potion": ["Oil Of Sharpness", "Potion Of Cloud Giant Strength", "Potion Of Flying", "Potion Of Invisibility", "Potion Of Speed", "Potion Of Supreme Healing",
                   "Potion Of Vitality"],
        "Ring": ["Ring Of Regeneration", "Ring Of Shooting Stars", "Ring Of Telekinesis"],
        "Rod": ["Rod Of Absorption", "Rod Of Alertness", "Rod Of The Pact Keeper +3"],
        "Scroll": ["generate"],
        "Staff": ["enspelled", "Quarterstaff Of The Acrobat", "Staff Of Fire", "Staff Of Frost", "Staff Of Power", "Staff Of Striking",
                  "Staff Of Thunder And Lightning"],
        "Wand": ["Wand Of Polymorph", "Wand Of The War Mage +3"],
        "Weapon": ["Ammunition +3", "Arrow Of Slaying", "Dancing Sword", "Dwarven Thrower", "Energy Bow", "enspelled", "Executioner's Axe", "Frost Brand",
                   "Lute Of Thunderous Thumping", "Nine Lives Stealer", "Oathbow", "Scimitar Of Speed", "Sword Of Sharpness", "Thunderous Greatclub",
                   "Weapon +3"]
    },
    "legendary": {
        "Armor": ["Armor Of Invulnerability", "Armor +3", "Efreeti Chain", "enspelled", "Plate Armor Of Etherealness"],
        "Potion": ["Draught Of The Colossus", "Potion Of Giant Size", "Potion Of Storm Giant Strength", "Skygrinder's Tonic"],
        "Ring": ["Ring Of Air Elemental Command", "Ring Of Djinni Summoning", "Ring Of Earth Elemental Command", "Ring Of Fire Elemental Command",
                 "Ring Of Invisibility", "Ring Of Spell Tuning", "Ring Of Water Elemental Command"],
        "Rod": ["Rod Of Lordly Might", "Rod Of Resurrection", "Boomstick"],
        "Scroll": ["generate"],
        "Staff": ["enspelled", "Staff Of The Magi"],
        "Wand": ["Spindle Of Fate", "Dual Wands Of Spell Twinning", "Ling Kuo's Magnificent Ink Brush", "Temporal Wand", "True Wand"],
        "Weapon": ["Defender", "enspelled", "Hammer Of Thunderbolts", "Holy Avenger", "Luck Blade", "Moonblade", "Sword Of Answering",
                   "Vorpal Sword"]
    }
}

possible_rarities = {
    "common": [0, 1],
    "uncommon": [2, 3],
    "rare": [4, 5],
    "very rare": [6, 7, 8],
    "legendary": [9]
}

enspell_levels_by_rarity = {
    "uncommon": [0, 1],
    "rare": [2, 3],
    "very rare": [4, 5],
    "legendary": [6, 7, 8]
}

def generate_divine_blessing():
    return random.choice(divine_blessings)

def get_rations():
    roll = random.randint(1, 10)
    if roll <= 5:
        return 0
    elif roll <= 9:
        return 1
    else:
        return 2

def generate_scroll_for_rarity(rarity):
    levels = possible_rarities[rarity]
    level = random.choice(levels)
    spell = random.choice(spells[level])["name"]
    level_label = "Cantrip" if level == 0 else f"Level {level}"
    return f"Spell Scroll {level_label} {spell}"

def generate_enspell_armor(rarity):
    levels = enspell_levels_by_rarity.get(rarity, [0])
    level = random.choice(levels)
    spell = random.choice(spells[level])["name"]
    
    level_label = "Cantrip" if level == 0 else f"Level {level}"
    
    valid_armors = [armor for armor in magic_items["common"]["Armor"] if armor != "Shield"]
    base_armor = random.choice(valid_armors)
    
    return f"Enspelled {base_armor} {level_label} {spell}"

def generate_enspell_staff(rarity):
    levels = enspell_levels_by_rarity.get(rarity, [0])
    level = random.choice(levels)
    spell = random.choice(spells[level])["name"]
    
    level_label = "Cantrip" if level == 0 else f"Level {level}"
    
    return f"Enspelled Staff {level_label} {spell}"

def generate_enspell_weapon(rarity):
    levels = enspell_levels_by_rarity.get(rarity, [0])
    level = random.choice(levels)
    spell = random.choice(spells[level])["name"]
    
    level_label = "Cantrip" if level == 0 else f"Level {level}"
    
    valid_weapons = [weapon for weapon in magic_items["common"]["Weapon"]]
    base_weapon = random.choice(valid_weapons)
    
    return f"Enspelled {base_weapon} {level_label} {spell}"

def get_random_magic_item(rarity):
    category = random.choice(list(magic_items[rarity].keys()))
    item_list = magic_items[rarity][category]
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

def generate_shop_encounter(rarity1, rarity2):
    shop_inventory = {}
    
    for category in magic_items[rarity1].keys():
        # Decide the 2:1 rarity distribution
        if random.choice([True, False]):
            primary, secondary = rarity1, rarity2
        else:
            primary, secondary = rarity2, rarity1
        
        items = []
        
        # Generate 2 items from primary rarity
        for _ in range(2):
            item_list = magic_items[primary][category]
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
        item_list = magic_items[secondary][category]
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
        
    return {
        "type": "Shop Encounter",
        "rarity_mix": {primary: 2, secondary: 1},
        "items_by_category": shop_inventory
    }

def generate_encounter(encounter_number):
    
    if encounter_number == 5:
        return generate_shop_encounter("uncommon", "rare")
    elif encounter_number == 10:
        return {"note": "Revisit to last shop"}
    elif encounter_number == 16:
        return generate_shop_encounter("rare", "very rare")
    elif encounter_number == 21:
        return  {"note": "Revisit to last shop"}
    elif encounter_number == 27:
        return generate_shop_encounter("very rare", "legendary")
    elif encounter_number == 32:
        return {"note": "Revisit to last shop"}
    elif encounter_number == 38:
        return generate_shop_encounter("legendary", "legendary")
    
    if encounter_number == 1:
        allowed_rarities = ["common", "uncommon"]
        xp = 600
        gold = 100
        monster_list = random.sample(monsters["1/2"], 2) + random.sample(monsters["1/4"], 2)
    elif encounter_number == 2:
        allowed_rarities = ["common", "uncommon"]
        xp = 900
        gold = 100
        monster_list = random.sample(monsters["1"], 2) + random.sample(monsters["1/2"], 2)
    elif encounter_number == 3:
        allowed_rarities = ["common", "uncommon"]
        xp = 1050
        gold = 200
        monster_list = random.sample(monsters["1"], 2) + random.sample(monsters["1/2"], 3)
    elif encounter_number == 4:
        allowed_rarities = ["common", "uncommon"]
        xp = 1425
        gold = 200
        monster_list = random.sample(monsters["2"], 1) + random.sample(monsters["1"], 2) + random.sample(monsters["1/2"], 1)
    elif encounter_number == 6:
        allowed_rarities = ["uncommon"]
        xp = 1575
        gold = 300
        monster_list = random.sample(monsters["2"], 1) + random.sample(monsters["1"], 2) + random.sample(monsters["1/2"], 2)
    elif encounter_number == 7:
        allowed_rarities = ["uncommon"]
        xp = 1725
        gold = 300
        monster_list = random.sample(monsters["2"], 1) + random.sample(monsters["1"], 2) + random.sample(monsters["1/2"], 3)
    elif encounter_number == 8:
        allowed_rarities = ["uncommon"]
        xp = 3000
        gold = 400
        monster_list = random.sample(monsters["3"], 1) + random.sample(monsters["2"], 2) + random.sample(monsters["1"], 2)
    elif encounter_number == 9:
        allowed_rarities = ["uncommon"]
        xp = 3425
        gold = 400
        monster_list = random.sample(monsters["3"], 1) + random.sample(monsters["2"], 2) + random.sample(monsters["1"], 3)
    elif encounter_number == 11:
        allowed_rarities = ["very rare"]
        xp = 4350
        gold = 4000
        monster_list = random.sample(monsters["5"], 1) + random.sample(monsters["3"], 1) + random.sample(monsters["1"], 2)
    elif encounter_number == 12:
        allowed_rarities = ["uncommon", "rare"]
        xp = 4650
        gold = 500
        monster_list = random.sample(monsters["4"], 2) + random.sample(monsters["2"], 1) + random.sample(monsters["1"], 2)
    elif encounter_number == 13:
        allowed_rarities = ["uncommon", "rare"]
        xp = 5700
        gold = 500
        monster_list = random.sample(monsters["5"], 1) + random.sample(monsters["4"], 1) + random.sample(monsters["2"], 2)
    elif encounter_number == 14:
        allowed_rarities = ["uncommon", "rare"]
        xp = 6075
        gold = 600
        monster_list = random.sample(monsters["5"], 1) + random.sample(monsters["4"], 1) + random.sample(monsters["3"], 1) + random.sample(monsters["2"], 1)
    elif encounter_number == 15:
        allowed_rarities = ["uncommon", "rare"]
        xp = 6825
        gold = 600
        monster_list = random.sample(monsters["6"], 1) + random.sample(monsters["4"], 1) + random.sample(monsters["3"], 1) + random.sample(monsters["2"], 1)
    elif encounter_number == 17:
        allowed_rarities = ["rare"]
        xp = 7200
        gold = 700
        monster_list = random.sample(monsters["6"], 1) + random.sample(monsters["4"], 1) + random.sample(monsters["3"], 2)
    elif encounter_number == 18:
        allowed_rarities = ["rare"]
        xp = 8700
        gold = 700
        monster_list = random.sample(monsters["7"], 1) + random.sample(monsters["5"], 1) + random.sample(monsters["3"], 1) + random.sample(monsters["1"], 2)
    elif encounter_number == 19:
        allowed_rarities = ["rare"]
        xp = 9450
        gold = 800
        monster_list = random.sample(monsters["7"], 1) + random.sample(monsters["5"], 1) + random.sample(monsters["3"], 1) + random.sample(monsters["2"], 2)
    elif encounter_number == 20:
        allowed_rarities = ["rare"]
        xp = 10500
        gold = 800
        monster_list = random.sample(monsters["8"], 1) + random.sample(monsters["4"], 2) + random.sample(monsters["2"], 2)
    elif encounter_number == 23:
        allowed_rarities = ["rare", "very rare"]
        xp = 10425
        gold = 4000
        monster_list = random.sample(monsters["9"], 1) + random.sample(monsters["4"], 1) + random.sample(monsters["2"], 1) + random.sample(monsters["1"], 2)
    elif encounter_number == 24:
        allowed_rarities = ["rare", "very rare"]
        xp = 11475
        gold = 4000
        monster_list = random.sample(monsters["9"], 1) + random.sample(monsters["5"], 1) + random.sample(monsters["2"], 1) + random.sample(monsters["1"], 2)
    elif encounter_number == 25:
        allowed_rarities = ["rare", "very rare"]
        xp = 15000
        gold = 5000
        monster_list = random.sample(monsters["10"], 1) + random.sample(monsters["6"], 1) + random.sample(monsters["4"], 1) + random.sample(monsters["3"], 1)
    elif encounter_number == 26:
        allowed_rarities = ["rare", "very rare"]
        xp = 17250
        gold = 5000
        monster_list = random.sample(monsters["11"], 1) + random.sample(monsters["7"], 1) + random.sample(monsters["3"], 2)
    elif encounter_number == 28:
        allowed_rarities = ["very rare"]
        xp = 20100
        gold = 6000
        monster_list = random.sample(monsters["12"], 1) + random.sample(monsters["8"], 1) + random.sample(monsters["4"], 1)
    elif encounter_number == 29:
        allowed_rarities = ["very rare"]
        xp = 20550
        gold = 6000
        monster_list = random.sample(monsters["12"], 1) + random.sample(monsters["8"], 1) + random.sample(monsters["3"], 2)
    elif encounter_number == 30:
        allowed_rarities = ["very rare"]
        xp = 23850
        gold = 7000
        monster_list = random.sample(monsters["13"], 1) + random.sample(monsters["9"], 1) + random.sample(monsters["2"], 2)
    elif encounter_number == 31:
        allowed_rarities = ["very rare"]
        xp = 27150
        gold = 7000
        monster_list = random.sample(monsters["14"], 1) + random.sample(monsters["10"], 1) + random.sample(monsters["3"], 1)
    elif encounter_number == 33:
        allowed_rarities = ["legendary"]
        xp = 29700
        gold = 200000
        monster_list = random.sample(monsters["16"], 1) + random.sample(monsters["6"], 1) + random.sample(monsters["4"], 1) + random.sample(monsters["3"], 2)
    elif encounter_number == 34:
        allowed_rarities = ["very rare", "legendary"]
        xp = 34500
        gold = 50000
        monster_list = random.sample(monsters["15"], 1) + random.sample(monsters["14"], 1) + random.sample(monsters["9"], 2)
    elif encounter_number == 35:
        allowed_rarities = ["very rare", "legendary"]
        xp = 34800
        gold = 50000
        monster_list = random.sample(monsters["16"], 1) + random.sample(monsters["13"], 1) + random.sample(monsters["10"], 1) + random.sample(monsters["8"], 1)
    elif encounter_number == 36:
        allowed_rarities = ["legendary"]
        xp = 42600
        gold = 100000
        monster_list = random.sample(monsters["17"], 1) + random.sample(monsters["14"], 1) + random.sample(monsters["11"], 1) + random.sample(monsters["10"], 1)
    elif encounter_number == 37:
        allowed_rarities = ["legendary"]
        xp = 0
        gold = 100000
        chosen_cr = random.choice(["17", "18", "19"])
        monster_list = random.sample(monsters[chosen_cr], 1) + random.sample(monsters["14"], 2) + random.sample(monsters["11"], 1) + random.sample(monsters["8"], 1)
    elif encounter_number == 39:
        allowed_rarities = ["legendary"]
        xp = 0
        gold = 0
        chosen_cr = random.choice(["20", "21", "22", "23", "24"])
        monster_list = random.sample(monsters[chosen_cr], 1) + random.sample(monsters["15"], 1) + random.sample(monsters["5"], 2)
    if encounter_number == 22:
        allowed_rarities = ["very rare"]
        xp = 12000
        gold = 40000
        monster_list = random.sample(monsters["10"], 1) + random.sample(monsters["3"], 3)
        magic_loot = [get_random_magic_item(random.choice(allowed_rarities)) for _ in range(8)]
    else:
        magic_loot = [get_random_magic_item(random.choice(allowed_rarities)) for _ in range(4)]
    
    encounter = {
        "monsters": monster_list,
        "xp": xp,
        "gold": gold,
        "magic_items": magic_loot,
        "rations": get_rations()
    }
    
    return encounter

def generate_all_encounters(total_encounters):
    all_encounters = []
    for i in range(1, total_encounters + 1):
        encounter = generate_encounter(i)
        all_encounters.append(encounter)
    return all_encounters

def print_encounter(encounter, number):
    print(f"\n--- Generating Encounter {number} ---")
    time.sleep(0.3)
    
    if encounter.get("type") == "Shop Encounter":
        print(f"Type: Shop Encounter")
        print(f"Rarity Distribution: {encounter['rarity_mix']}\n")
        time.sleep(0.3)
        for category, items in encounter["items_by_category"].items():
            print(f"{category}:")
            for item in items:
                print(f" - {item}")
                time.sleep(0.2)
            print()
    else:
        for key, value in encounter.items():
            print(f"{key.capitalize()}: ", end="")
            time.sleep(0.3)
            
            if isinstance(value, list):
                print()
                for item in value:
                    print(f" - {item}")
                    time.sleep(0.2)
            else:
                print(value)
            time.sleep(0.3)

if __name__ == "__main__":
    divine_blessing_for_run = generate_divine_blessing()
    print("\n=== Divine Blessing For This Run ===")
    print(f" {divine_blessing_for_run}")
    print("=======================================\n")
    encounters = generate_all_encounters(39)
    for i, encounter in enumerate(encounters, start=1):
        print_encounter(encounter, i)
        time.sleep(0.3)