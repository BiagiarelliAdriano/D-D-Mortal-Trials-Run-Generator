BARBARIAN = {
    "name": "Barbarian",
    "description": (
        """Barbarians are relentless warriors empowered by primal forces surging from within. Their fury is not
            just rage, it's a physical manifestation of raw survival instinct, ancient spirit guidance, or the wrath
            of a world out of balance.""",
    ),
    "primary_ability": "Strength",
    "hit_die": "d12",
    "proficiencies": {
        "saving_throws": ["Strength", "Constitution"],
        "skills": ["Choose two: ", "Animal Handling", "Athletics", "Intimidation", "Nature", "Perception", "Survival"],
        "weapons": ["Simple", "Martial"],
        "armor": ["Light", "Medium", "Shields"],
        "tools": [],
    },
    "starting_equipment": [
        "Choice A: Greataxe, 4 Handaxes, Explorer's Pack, 15 GP",
        "Choice B: 75 GP"
    ],
    "features": {
        1: [
            {
                "name": "Rage",
                "summary": "Enter a state of primal fury, granting bonuses to damage, resistances, and Strength-based rolls.",
                "details": {
                    "uses": {
                        "1-2": 2,
                        "3-5": 3,
                        "6-11": 4,
                        "12-16": 5,
                        "17-20": 6
                    },
                    "bonuses": {
                        "damage_bonus": {
                            "1-8": "+2",
                            "9-15": "+3",
                            "16-20": "+4"
                        },
                        "resistance": ["Bludgeoning", "Piercing", "Slashing"],
                        "advantages": ["Strength checks", "Strength saving throws"]
                    },
                    "duration": "Until end of next turn, extendable. Up to 10 minutes max."
                }
            },
            {
                "name": "Unarmored Defense",
                "summary": "AC = 10 + DEX + CON when not wearing armor; can still use a shield."
            },
            {
                "name": "Weapon Mastery",
                "summary": "Gain mastery of two melee weapons; increases at higher levels.",
                "scaling": {
                    "1-3": 2,
                    "4-9": 3,
                    "10-20": 4
                }
            }
        ],
        2: [
            {
                "name": "Danger Sense",
                "summary": "Advantage on Dexterity saves while not Incapacitated."
            },
            {
                "name": "Reckless Attack",
                "summary": "Gain Advantage on Strength attacks for the turn; attackers gain Advantage against you."
            }
        ],
        3: [
            {
                "name": "Barbarian Subclass",
                "summary": ["Choose a subclass: ", "Path of the Berserker", "Path of the Wild Heart", "Path of the World Tree", "Path of the Zealot"],
                "note": "Grants features at various levels."
            },
            {
                "name": "Primal Knowledge",
                "summary": "Gain 1 Barbarian skill; can use Strength for select ability checks while raging.",
                "skills_affected": ["Acrobatics", "Intimidation", "Perception", "Stealth", "Survival"]
            }
        ],
        4: [
            {
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        5: [
            {
                "name": "Extra Attack",
                "summary": "Attack twice when taking the Attack action."
            },
            {
                "name": "Fast Movement",
                "summary": "+10 ft movement while not wearing Heavy armor."
            }
        ],
        7: [
            {"name": "Feral Instinct", "summary": "Advantage on Initiative."},
            {"name": "Instinctive Pounce", "summary": "Move up to half speed when you Rage."}
        ],
        9: [
            {
                "name": "Brutal Strike",
                "summary": "Add 1d10 damage and choose an extra effect when attacking recklessly.",
                "effects": ["Forceful Blow", "Hamstring Blow"]
            }
        ],
        11: [
            {
                "name": "Relentless Rage",
                "summary": "Make Con save to avoid dropping to 0 HP; DC increases with each use until rest."
            }
        ],
        13: [
            {
                "name": "Improved Brutal Strike",
                "summary": "Add new options to Brutal Strike: Staggering Blow, Sundering Blow."
            }
        ],
        15: [
            {
                "name": "Persistent Rage",
                "summary": "Rage lasts 10 minutes without needing extensions; regains all Rage uses on Initiative (once per Long Rest)."
            }
        ],
        17: [
            {
                "name": "Brutal Strike Upgrade",
                "summary": "Damage increases to 2d10; apply two effects at once."
            }
        ],
        18: [
            {
                "name": "Indomitable Might",
                "summary": "Use Strength score instead of total if you roll lower on Strength checks/saves."
            }
        ],
        19: [
            {
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat."
            }
        ],
        20: [
            {
                "name": "Primal Champion",
                "summary": "Str and Con scores increase by 4, to a max of 25."
            }
        ]
    }
}

BARD = {
    "name": "Bard",
    "hit_die": "d8",
    "primary_ability": "Charisma",
    "saving_throws": ["Dexterity", "Charisma"],
    "armor_proficiencies": ["Light"],
    "weapon_proficiencies": ["Simple"],
    "tool_proficiencies": {
        "choose": 3,
        "options": ["Bagpipes", "Drum", "Dulcimer", "Flute", "Horn", "Lute", "Lyre", "Pan Flute", "Shawm", "Viol"]
    },
    "skill_proficiencies": {
        "choose": 3,
        "options": [
        "Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight", "Intimidation",
        "Investigation", "Medicine", "Nature", "Perception", "Performance", "Persuasion", "Religion",
        "Sleight of Hand", "Stealth", "Survival"
        ]
    },
    "starting_equipment": {
        "option_A": [
        "Leather Armor", "2 Daggers", "Musical Instrument (choice)", "Entertainer's Pack", "19 GP"
        ],
        "option_B": [
        "90 GP"
        ]
    },
    "description": """
        Bards weave magic through performance, turning memory, rhythm, and spoken word into tools of power.
        Driven by curiosity and the spark of creation, they collect fragments of history and myth, transforming
        them into magic and influence.
    """,
    "levels": {
        "1": {
        "features": [
            {
            "name": "Bardic Inspiration",
            "summary": """
                You can supernaturally inspire others through words, music, or dance. This inspiration is represented
                by your Bardic Inspiration die, which is a d6. Using Bardic Inspiration: As a Bonus Action, you can inspire
                another creature within 60ft who can see or hear you. They gain one Bardic Inspiration die. A creature can have
                only one Bardic Inspiration die at a time. Within the next hour when the creature fails a D20 Test, they can roll
                the die and add it to the d20. The die is expended when rolled.
            """,
            "details": {
                "uses": {
                "type": "ability-mod",
                "ability": "Charisma"
                },
                "recharge": "Long Rest",
                "die": {
                "1-4": "d6",
                "5-9": "d8",
                "10-14": "d10",
                "15-20": "d12"
                }
            }
            },
            {
            "name": "Spellcasting",
            "summary": """You can cast spells through bardic arts. You start with 2 cantrips and 4 prepared level 1 spells.
                Prepared spells increase as you level up. You use Charisma for spellcasting and can use a musical instrument
                as a spellcasting focus.
            """,
            "details": {
                "cantrips_known": {
                "1": 2,
                "4": 3,
                "10": 4
                },
                "spells_prepared": {
                "1": 4,
                "2": 5,
                "3": 6,
                "4": 7,
                "5": 9,
                "6": 10,
                "7": 11,
                "8": 12,
                "9": 14,
                "10": 15,
                "11": 16,
                "12": 16,
                "13": 17,
                "14": 17,
                "15": 18,
                "16": 18,
                "17": 19,
                "18": 20,
                "19": 21,
                "20": 22
                },
                "spell_slots": {
                "1": {"1": 2},
                "2": {"1": 3},
                "3": {"1": 4, "2": 2},
                "4": {"1": 4, "2": 3},
                "5": {"1": 4, "2": 3, "3": 2},
                "6": {"1": 4, "2": 3, "3": 3},
                "7": {"1": 4, "2": 3, "3": 3, "4": 1},
                "8": {"1": 4, "2": 3, "3": 3, "4": 2},
                "9": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 1},
                "10": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2},
                "11": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1},
                "12": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1},
                "13": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1, "7": 1},
                "14": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1, "7": 1},
                "15": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1, "7": 1, "8": 1},
                "16": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1, "7": 1, "8": 1},
                "17": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1, "7": 1, "8": 1, "9": 1},
                "18": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1, "7": 1, "8": 1, "9": 1},
                "19": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 2, "7": 1, "8": 1, "9": 1},
                "20": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 2, "7": 2, "8": 1, "9": 1}
                },
                "casting_ability": "Charisma",
                "focus": "Musical Instrument"
                    }
                }
            ]
        }
    }
}