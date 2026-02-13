from encounter_generator.data.rules.spell_tables import FULL_CASTER_SLOTS
from encounter_generator.data.rules.subclasses.barbarian import BARBARIAN_SUBCLASSES
from encounter_generator.data.rules.subclasses.bard import BARD_SUBCLASSES
from encounter_generator.data.rules.subclasses.cleric import CLERIC_SUBCLASSES
from encounter_generator.data.rules.subclasses.druid import DRUID_SUBCLASSES

BARBARIAN = {
    "id": "barbarian",
    "name": "Barbarian",
    "subclasses": BARBARIAN_SUBCLASSES,
    "description": """Barbarians are relentless warriors empowered by primal forces surging from within. Their fury is not
        just rage, it's a physical manifestation of raw survival instinct, ancient spirit guidance, or the wrath
        of a world out of balance.""",
    "primary_ability": "Strength",
    "hit_die": "d12",
    "proficiencies": {
        "saving_throws": ["Strength", "Constitution"],
        "armor": ["Light", "Medium", "Shields"],
        "weapons": ["Simple", "Martial"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Animal Handling", "Athletics", "Intimidation", "Nature", "Perception", "Survival"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Greataxe", "4 Handaxes", "Explorer's Pack"],
            "gold": 15
        },
        "option_b": {
            "gold": 75
        }
    },
    "features": {
        1: [
            {
                "id": "barbarian_rage",
                "name": "Rage",
                "summary": "Enter a state of primal fury, granting bonuses to damage, resistances, and Strength-based rolls.",
                "details": {
                    "uses": {
                        "type": "level-based",
                        "scaling": {
                            "1-2": 2,
                            "3-5": 3,
                            "6-11": 4,
                            "12-16": 5,
                            "17-20": 6
                        }
                    },
                    "bonuses": {
                        "damage_bonus": {
                            "type": "level-based",
                            "scaling": {
                                "1-8": 2,
                                "9-15": 3,
                                "16-20": 4
                            }
                        },
                        "resistance": ["Bludgeoning", "Piercing", "Slashing"],
                        "advantages": ["Strength checks", "Strength saving throws"]
                    },
                    "duration": "Until end of next turn, extendable. Up to 10 minutes max."
                }
            },
            {
                "id": "barbarian_unarmored_defense",
                "name": "Unarmored Defense",
                "summary": "AC = 10 + DEX + CON when not wearing armor; can still use a shield."
            },
            {
                "id": "barbarian_weapon_mastery",
                "name": "Weapon Mastery",
                "summary": "Gain mastery of two melee weapons; increases at higher levels.",
                "details": {
                    "weapons_mastered": {
                        "type": "level-based",
                        "scaling": {
                            "1-3": 2,
                            "4-9": 3,
                            "10-20": 4
                        }
                    }
                }
            }
        ],
        2: [
            {
                "id": "barbarian_danger_sense",
                "name": "Danger Sense",
                "summary": "Advantage on Dexterity saves while not Incapacitated."
            },
            {
                "id": "barbarian_reckless_attack",
                "name": "Reckless Attack",
                "summary": "Gain Advantage on Strength attacks for the turn; attackers gain Advantage against you."
            }
        ],
        3: [
            {
                "id": "barbarian_subclass",
                "name": "Barbarian Subclass",
                "summary": "Choose a subclass: Path of the Berserker, Path of the Wild Heart, Path of the World Tree, or Path of the Zealot.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": ["Path of the Berserker", "Path of the Wild Heart", "Path of the World Tree", "Path of the Zealot"]
                    },
                    "note": "Grants features at various levels."
                }
            },
            {
                "id": "barbarian_primal_knowledge",
                "name": "Primal Knowledge",
                "summary": "Gain 1 Barbarian skill; can use Strength for select ability checks while raging.",
                "details": {
                    "skills_affected": ["Acrobatics", "Intimidation", "Perception", "Stealth", "Survival"]
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        5: [
            {
                "id": "barbarian_extra_attack",
                "name": "Extra Attack",
                "summary": "Attack twice when taking the Attack action."
            },
            {
                "id": "barbarian_fast_movement",
                "name": "Fast Movement",
                "summary": "+10 ft movement while not wearing Heavy armor."
            }
        ],
        7: [
            {
                "id": "barbarian_feral_instinct",
                "name": "Feral Instinct",
                "summary": "Advantage on Initiative."
            },
            {
                "id": "barbarian_instinctive_pounce",
                "name": "Instinctive Pounce",
                "summary": "Move up to half speed when you Rage."
            }
        ],
        9: [
            {
                "id": "barbarian_brutal_strike",
                "name": "Brutal Strike",
                "summary": "Add 1d10 damage and choose an extra effect when attacking recklessly.",
                "details": {
                    "damage": "1d10",
                    "effects": ["Forceful Blow", "Hamstring Blow"]
                }
            }
        ],
        11: [
            {
                "id": "barbarian_relentless_rage",
                "name": "Relentless Rage",
                "summary": "Make Con save to avoid dropping to 0 HP; DC increases with each use until rest."
            }
        ],
        13: [
            {
                "id": "barbarian_improved_brutal_strike",
                "name": "Improved Brutal Strike",
                "summary": "Add new options to Brutal Strike: Staggering Blow, Sundering Blow."
            }
        ],
        15: [
            {
                "id": "barbarian_persistent_rage",
                "name": "Persistent Rage",
                "summary": "Rage lasts 10 minutes without needing extensions; regains all Rage uses on Initiative (once per Long Rest)."
            }
        ],
        17: [
            {
                "id": "barbarian_brutal_strike_upgrade",
                "name": "Brutal Strike Upgrade",
                "summary": "Damage increases to 2d10; apply two effects at once.",
                "details": {
                    "damage": "2d10",
                    "effects_count": 2
                }
            }
        ],
        18: [
            {
                "id": "barbarian_indomitable_might",
                "name": "Indomitable Might",
                "summary": "Use Strength score instead of total if you roll lower on Strength checks/saves."
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat."
            }
        ],
        20: [
            {
                "id": "barbarian_primal_champion",
                "name": "Primal Champion",
                "summary": "Str and Con scores increase by 4, to a max of 25."
            }
        ]
    }
}

BARD = {
    "id": "bard",
    "name": "Bard",
    "subclasses": BARD_SUBCLASSES,
    "description": """Bards weave magic through performance, turning memory, rhythm, and spoken word into tools of power.
        Driven by curiosity and the spark of creation, they collect fragments of history and myth, transforming
        them into magic and influence.""",
    "primary_ability": "Charisma",
    "hit_die": "d8",
    "proficiencies": {
        "saving_throws": ["Dexterity", "Charisma"],
        "armor": ["Light"],
        "weapons": ["Simple"],
        "tools": {
            "granted": [],
            "choose": 3,
            "options": ["Bagpipes", "Drum", "Dulcimer", "Flute", "Horn", "Lute", "Lyre", "Pan Flute", "Shawm", "Viol"]
        },
        "skills": {
            "granted": [],
            "choose": 3,
            "options": [
                "Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight", "Intimidation",
                "Investigation", "Medicine", "Nature", "Perception", "Performance", "Persuasion", "Religion",
                "Sleight of Hand", "Stealth", "Survival"
            ]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Leather Armor", "2 Daggers", "Musical Instrument (choice)", "Entertainer's Pack"],
            "gold": 19
        },
        "option_b": {
            "gold": 90
        }
    },
    "spellcasting": {
        "ability": "Charisma",
        "progression": "full",
        "preparation_mode": "learned",
        "focus": ["Musical Instrument"],
        "cantrips_known": {1: 2, 4: 3, 10: 4},
        "spells_prepared": {
            1: 4, 2: 5, 3: 6, 4: 7, 5: 9, 6: 10, 7: 11, 8: 12, 9: 14, 10: 15,
            11: 16, 12: 16, 13: 17, 14: 17, 15: 18, 16: 18, 17: 19, 18: 20, 19: 21, 20: 22
        }
    },
    "features": {
        1: [
            {
                "id": "bard_bardic_inspiration",
                "name": "Bardic Inspiration",
                "summary": """You can supernaturally inspire others through words, music, or dance. This inspiration is represented
                    by your Bardic Inspiration die, which is a d6. Using Bardic Inspiration: As a Bonus Action, you can inspire
                    another creature within 60ft who can see or hear you. They gain one Bardic Inspiration die. A creature can have
                    only one Bardic Inspiration die at a time. Within the next hour when the creature fails a D20 Test, they can roll
                    the die and add it to the d20. The die is expended when rolled.""",
                "details": {
                    "uses": {
                        "type": "ability-mod",
                        "ability": "Charisma"
                    },
                    "recharge": "Long Rest",
                    "die": {
                        "type": "level-based",
                        "scaling": {
                            "1-4": "d6",
                            "5-9": "d8",
                            "10-14": "d10",
                            "15-20": "d12"
                        }
                    }
                }
            },
            {
                "id": "bard_spellcasting",
                "name": "Spellcasting",
                "summary": """You can cast spells through bardic arts. You start with 2 cantrips and 4 prepared level 1 spells.
                    Prepared spells increase as you level up. You use Charisma for spellcasting and can use a musical instrument
                    as a spellcasting focus."""
            }
        ],
        2: [
            {
                "id": "bard_expertise_2",
                "name": "Expertise",
                "summary": "You gain Expertise in two of your skill proficiencies of your choice.",
                "details": {
                    "choice": {
                        "choose": 2,
                        "type": "skill_proficiency"
                    }
                }
            },
            {
                "id": "bard_jack_of_all_trades",
                "name": "Jack Of All Trades",
                "summary": "Add half your Proficiency Bonus (round down) to any ability check for skills you lack.",
                "details": {
                    "bonus": "1/2 Proficiency Bonus (down)"
                }
            }
        ],
        3: [
            {
                "id": "bard_subclass",
                "name": "Bard Subclass",
                "summary": "Choose a subclass: College Of Dance, College Of Glamour, College Of Lore, or College Of Valor.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": ["College Of Dance", "College Of Glamour", "College Of Lore", "College Of Valor"]
                    },
                    "note": "Grants features at various levels."
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        5: [
            {
                "id": "bard_font_of_inspiration",
                "name": "Font Of Inspiration",
                "summary": "Regain Bardic Inspiration on Short or Long Rest; can expend spell slots to regain uses.",
                "details": {
                    "recharge": "Short or Long Rest",
                    "spell_slot_conversion": "Expend 1 slot to regain 1 use (no Action required)"
                }
            }
        ],
        7: [
            {
                "id": "bard_countercharm",
                "name": "Countercharm",
                "summary": "Use a Reaction to cause a creature to reroll a failed save against Charm or Fear with Advantage.",
                "details": {
                    "reaction_trigger": "Failure against Charmed or Frightened",
                    "range": "30 ft",
                    "benefit": "Reroll with Advantage"
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        9: [
            {
                "id": "bard_expertise_9",
                "name": "Expertise",
                "summary": "Gain Expertise in two more skill proficiencies of your choice.",
                "details": {
                    "choice": {
                        "choose": 2,
                        "type": "skill_proficiency"
                    }
                }
            }
        ],
        10: [
            {
                "id": "bard_magical_secrets_10",
                "name": "Magical Secrets",
                "summary": "Prepare spells from Bard, Cleric, Druid, and Wizard lists when your Prepared Spells number increases.",
                "details": {
                    "list_access": ["Bard", "Cleric", "Druid", "Wizard"],
                    "note": "Chosen spells count as Bard spells."
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        18: [
            {
                "id": "bard_superior_inspiration",
                "name": "Superior Inspiration",
                "summary": "Regain Bardic Inspiration uses until you have at least two when rolling Initiative.",
                "details": {
                    "trigger": "Initiative",
                    "restoration": "Up to 2 uses"
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat."
            }
        ],
        20: [
            {
                "id": "bard_words_of_creation",
                "name": "Words Of Creation",
                "summary": "Always have Power Word Heal and Power Word Kill prepared; can target a second creature.",
                "details": {
                    "spells_granted": ["Power Word Heal", "Power Word Kill"],
                    "benefit": "Target a second creature within 10 ft of the first."
                }
            }
        ]
    }
}

CLERIC = {
    "id": "cleric",
    "name": "Cleric",
    "subclasses": CLERIC_SUBCLASSES,
    "description": """Clerics are intermediaries between the mortal world and they were given powers resembling those of the gods. 
        Empowered by divine magic, they serve as healers, protectors, and harbingers of their deity's will. 
        Wielding both holy light and martial might, a Cleric is a pillar of strength for any adventuring party.""",
    "primary_ability": "Wisdom",
    "hit_die": "d8",
    "proficiencies": {
        "saving_throws": ["Wisdom", "Charisma"],
        "armor": ["Light", "Medium", "Shields"],
        "weapons": ["Simple"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["History", "Insight", "Medicine", "Persuasion", "Religion"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Chain Shirt", "Shield", "Mace", "Holy Symbol", "Priest's Pack"],
            "gold": 7
        },
        "option_b": {
            "gold": 110
        }
    },
    "spellcasting": {
        "ability": "Wisdom",
        "progression": "full",
        "preparation_mode": "prepared",
        "focus": ["Holy Symbol"],
        "cantrips_known": {1: 3, 4: 4, 10: 5},
        "spells_prepared": {
            1: 4, 2: 5, 3: 6, 4: 7, 5: 9, 6: 10, 7: 11, 8: 12, 9: 14, 10: 15,
            11: 16, 12: 16, 13: 17, 14: 17, 15: 18, 16: 18, 17: 19, 18: 20, 19: 21, 20: 22
        }
    },
    "features": {
        1: [
            {
                "id": "cleric_spellcasting",
                "name": "Spellcasting",
                "summary": "You can cast spells through divine power. You start with 3 cantrips and use Wisdom as your spellcasting ability."
            },
            {
                "id": "cleric_divine_order",
                "name": "Divine Order",
                "summary": "Choose a sacred role: Protector (Martial weapons & Heavy armor) or Thaumaturge (extra cantrip & Wisdom bonus to Arcana/Religion).",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": [
                            {
                                "name": "Protector",
                                "benefit": "Proficiency with Martial weapons and training with Heavy armor."
                            },
                            {
                                "name": "Thaumaturge",
                                "benefit": "Gain one extra Cleric cantrip. Add Wisdom modifier (min +1) to Intelligence (Arcana or Religion) checks."
                            }
                        ]
                    }
                }
            }
        ],
        2: [
            {
                "id": "cleric_channel_divinity",
                "name": "Channel Divinity",
                "summary": "Use divine energy for special effects like Divine Spark or Turn Undead.",
                "details": {
                    "uses": {
                        "type": "level-based",
                        "scaling": {
                            "2-5": 2,
                            "6-17": 3,
                            "18-20": 4
                        }
                    },
                    "recharge": "Short Rest (regain 1), Long Rest (regain all)",
                    "save_dc": "8 + Proficiency Bonus + Wisdom modifier",
                    "effects": [
                        {
                            "name": "Divine Spark",
                            "summary": "Heal or damage a creature within 30ft.",
                            "details": {
                                "action": "Magic Action",
                                "range": "30 ft",
                                "scaling": {
                                    "2-6": "1d8 + WIS",
                                    "7-12": "2d8 + WIS",
                                    "13-17": "3d8 + WIS",
                                    "18-20": "4d8 + WIS"
                                },
                                "effect": "Restore HP or deal Necrotic/Radiant damage (Constitution save for half)."
                            }
                        },
                        {
                            "name": "Turn Undead",
                            "summary": "Undead within 30ft must save or be Frightened and Incapacitated for 1 minute. On their turn they try to move as far away from you as possible.",
                            "details": {
                                "action": "Magic Action",
                                "range": "30 ft",
                                "save": "Wisdom",
                                "duration": "1 minute or until damaged"
                            }
                        }
                    ]
                }
            }
        ],
        3: [
            {
                "id": "cleric_subclass",
                "name": "Cleric Subclass",
                "summary": "Choose a divine domain: Life, Light, Trickery, or War.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": ["Life Domain", "Light Domain", "Trickery Domain", "War Domain"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        5: [
            {
                "id": "cleric_sear_undead",
                "name": "Sear Undead",
                "summary": "Turn Undead deals Radiant damage equal to multiple d8s (Wisdom modifier) to those who fail their save.",
                "details": {
                    "damage": "Xd8 (where X is Wisdom modifier, min 1)",
                    "type": "Radiant",
                    "note": "Does not end the Turn Undead effect."
                }
            }
        ],
        7: [
            {
                "id": "cleric_blessed_strikes",
                "name": "Blessed Strikes",
                "summary": "Choose Divine Strike (+1d8 weapon damage) or Potent Spellcasting (+WIS to cantrip damage).",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": [
                            {
                                "name": "Divine Strike",
                                "benefit": "Once per turn, +1d8 Necrotic or Radiant damage on a weapon hit."
                            },
                            {
                                "name": "Potent Spellcasting",
                                "benefit": "Add Wisdom modifier to damage dealt with Cleric cantrips."
                            }
                        ]
                    }
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        10: [
            {
                "id": "cleric_divine_intervention",
                "name": "Divine Intervention",
                "summary": "As a Magic Action, cast any Cleric spell of level 5 or lower without a slot or components.",
                "details": {
                    "action": "Magic Action",
                    "limit": "Level 5 or lower Cleric spell",
                    "recharge": "Long Rest"
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        14: [
            {
                "id": "cleric_improved_blessed_strikes",
                "name": "Improved Blessed Strikes",
                "summary": "Your Blessed Strikes choice becomes more powerful.",
                "details": {
                    "divine_strike_upgrade": "+2d8 total damage",
                    "potent_spellcasting_upgrade": "Dealing cantrip damage also grants Temp HP (2x WIS mod) to you or an ally within 60ft."
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat."
            }
        ],
        20: [
            {
                "id": "cleric_greater_divine_intervention",
                "name": "Greater Divine Intervention",
                "summary": "Use Divine Intervention to cast a level 9 Cleric spell.",
                "details": {
                    "upgrade": "Can cast Level 9 Cleric spells",
                    "recharge_penalty": "If level 9 is used, cannot use again for 2d4 encounters."
                }
            }
        ]
    }
}

DRUID = {
    "id": "druid",
    "name": "Druid",
    "subclasses": DRUID_SUBCLASSES,
    "description": """Druids are conduits of the natural world's raw power, channeling the elements and assuming the 
        forms of beasts. They serve as guardians of the wilderness, balancing the cycles of life and death, 
        and drawing magic from the ancient rhythms of nature itself.""",
    "primary_ability": "Wisdom",
    "hit_die": "d8",
    "proficiencies": {
        "saving_throws": ["Intelligence", "Wisdom"],
        "armor": ["Light", "Shields"],
        "weapons": ["Simple"],
        "tools": {
            "granted": ["Herbalism Kit"],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Arcana", "Animal Handling", "Insight", "Medicine", "Nature", "Perception", "Religion", "Survival"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Leather Armor", "Shield", "Sickle", "Druidic Focus (Quarterstaff)", "Explorer's Pack", "Herbalism Kit"],
            "gold": 9
        },
        "option_b": {
            "gold": 50
        }
    },
    "spellcasting": {
        "ability": "Wisdom",
        "progression": "full",
        "preparation_mode": "prepared",
        "focus": ["Druidic Focus"],
        "cantrips_known": {1: 2, 4: 3, 10: 4},
        "spells_prepared": {
            1: 4, 2: 5, 3: 6, 4: 7, 5: 9, 6: 10, 7: 11, 8: 12, 9: 14, 10: 15,
            11: 16, 12: 16, 13: 17, 14: 17, 15: 18, 16: 18, 17: 19, 18: 20, 19: 21, 20: 22
        }
    },
    "features": {
        1: [
            {
                "id": "druid_spellcasting",
                "name": "Spellcasting",
                "summary": "Cast spells using Wisdom and a Druidic Focus; swap your entire spell list after a Long Rest."
            },
            {
                "id": "druid_druidic",
                "name": "Druidic",
                "summary": "Know the secret language of Druids and always have Speak with Animals prepared.",
                "details": {
                    "spells_granted": ["Speak with Animals"],
                    "language": "Druidic",
                    "hidden_messages_dc": 15
                }
            },
            {
                "id": "druid_primal_order",
                "name": "Primal Order",
                "summary": "Choose a sacred role: Magician (extra cantrip & Wisdom bonus to Arcana/Nature) or Warden (Martial weapons & Medium armor).",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": [
                            {
                                "name": "Magician",
                                "benefit": "Extra Druid cantrip. Add Wisdom modifier (min +1) to Intelligence (Arcana or Nature) checks."
                            },
                            {
                                "name": "Warden",
                                "benefit": "Proficiency with Martial weapons and training with Medium armor."
                            }
                        ]
                    }
                }
            }
        ],
        2: [
            {
                "id": "druid_wild_shape",
                "name": "Wild Shape",
                "summary": "Shape-shift into a Beast form as a Bonus Action.",
                "details": {
                    "uses": {
                        "type": "level-based",
                        "scaling": {
                            "2-5": 2,
                            "6-16": 3,
                            "17-20": 4
                        }
                    },
                    "recharge": "Short Rest (regain 1), Long Rest (regain all)",
                    "duration": "Hours equal to half Druid level",
                    "hp_granted": "Druid level (Temporary HP)",
                    "forms": {
                        "scaling": {
                            "2-3": {"known": 4, "max_cr": "1/4", "fly": False},
                            "4-7": {"known": 6, "max_cr": "1/2", "fly": False},
                            "8-20": {"known": 8, "max_cr": "1", "fly": True}
                        }
                    }
                }
            },
            {
                "id": "druid_wild_companion",
                "name": "Wild Companion",
                "summary": "Expend a spell slot or Wild Shape use to cast Find Familiar (Fey) as a Magic Action.",
                "details": {
                    "action": "Magic Action",
                    "resource": "Spell slot or Wild Shape use",
                    "familiar_type": "Fey",
                    "duration": "Until Long Rest"
                }
            }
        ],
        3: [
            {
                "id": "druid_subclass",
                "name": "Druid Subclass",
                "summary": "Choose a Druidic Circle: Land, Moon, Sea, or Stars.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": ["Circle Of The Land", "Circle Of The Moon", "Circle Of The Sea", "Circle Of The Stars"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        5: [
            {
                "id": "druid_wild_resurgence",
                "name": "Wild Resurgence",
                "summary": "Convert spell slots to Wild Shape uses, or once per Long Rest, convert a Wild Shape use into a Level 1 spell slot.",
                "details": {
                    "slot_to_wild_shape": "Expend spell slot to gain 1 use (if none left, 1/turn)",
                    "wild_shape_to_slot": "Expend 1 use to gain Level 1 slot (1/Long Rest)"
                }
            }
        ],
        7: [
            {
                "id": "druid_elemental_fury",
                "name": "Elemental Fury",
                "summary": "Choose Potent Spellcasting (+WIS to cantrip damage) or Primal Strike (+1d8 elemental damage on hits).",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": [
                            {
                                "name": "Potent Spellcasting",
                                "benefit": "Add Wisdom modifier to Druid cantrip damage."
                            },
                            {
                                "name": "Primal Strike",
                                "benefit": "Once per turn, +1d8 Cold, Fire, Lightning, or Thunder damage on a weapon or beast attack."
                            }
                        ]
                    }
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        15: [
            {
                "id": "druid_improved_elemental_fury",
                "name": "Improved Elemental Fury",
                "summary": "Your Elemental Fury choice becomes more powerful.",
                "details": {
                    "potent_spellcasting_upgrade": "Range increases by 300 ft for cantrips with range >= 10 ft.",
                    "primal_strike_upgrade": "Extra damage increases to 2d8."
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        18: [
            {
                "id": "druid_beast_spells",
                "name": "Beast Spells",
                "summary": "While using Wild Shape, you can cast spells in Beast form (unless material cost/consumption is involved).",
                "details": {
                    "restriction": "No spells with specified material cost or consumed components."
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat."
            }
        ],
        20: [
            {
                "id": "druid_archdruid",
                "name": "Archdruid",
                "summary": "Regain Wild Shape on Initiative, convert uses into powerful spell slots, and age slowly.",
                "details": {
                    "evergreen_wild_shape": "Regain 1 use on Initiative if none are left.",
                    "nature_magician": "Convert multiple Wild Shape uses into a single spell slot (1 use = 2 spell levels, 1/Long Rest).",
                    "longevity": "Age 1 year for every 10 years passed."
                }
            }
        ]
    }
}

FIGHTER = {
    "id": "fighter",
    "name": "Fighter",
    "description": """Fighters are masters of martial combat, skilled with a variety of weapons and armor. 
        Whether a disciplined soldier, a rugged mercenary, or a knightly champion, a Fighter excels on the 
        front lines, using tactical expertise and physical prowess to dominate the battlefield.""",
    "primary_ability": "Strength or Dexterity",
    "hit_die": "d10",
    "proficiencies": {
        "saving_throws": ["Strength", "Constitution"],
        "armor": ["Light", "Medium", "Heavy", "Shields"],
        "weapons": ["Simple", "Martial"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Acrobatics", "Animal Handling", "Athletics", "History", "Insight", "Intimidation", "Persuasion", "Perception", "Survival"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Chain Mail", "Greatsword", "Flail", "8 Javelins", "Dungeoneer's Pack"],
            "gold": 4
        },
        "option_b": {
            "items": ["Studded Leather Armor", "Scimitar", "Shortsword", "Longbow", "20 Arrows", "Quiver", "Dungeoneer's Pack"],
            "gold": 11
        },
        "option_c": {
            "gold": 155
        }
    },
    "features": {
        1: [
            {
                "id": "fighter_fighting_style",
                "name": "Fighting Style",
                "summary": "Gain a Fighting Style feat of your choice; can be replaced whenever you gain a Fighter level.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "type": "fighting_style_feat"
                    }
                }
            },
            {
                "id": "fighter_second_wind",
                "name": "Second Wind",
                "summary": "Use a Bonus Action to regain 1d10 + Fighter level HP.",
                "details": {
                    "uses": {
                        "type": "level-based",
                        "scaling": {
                            "1-3": 2,
                            "4-9": 3,
                            "10-20": 4
                        }
                    },
                    "recharge": "Short Rest (regain 1), Long Rest (regain all)",
                    "recovery": "1d10 + Fighter Level"
                }
            },
            {
                "id": "fighter_weapon_mastery",
                "name": "Weapon Mastery",
                "summary": "Learn the mastery properties of three weapons; can change one choice after a Long Rest.",
                "details": {
                    "base_masteries": 3,
                    "scaling": {
                        "1-3": 3,
                        "4-9": 4,
                        "10-15": 5,
                        "16-20": 6
                    }
                }
            }
        ],
        2: [
            {
                "id": "fighter_action_surge",
                "name": "Action Surge",
                "summary": "Take one additional action (except Magic) on your turn.",
                "details": {
                    "uses": {
                        "type": "level-based",
                        "scaling": {
                            "2-16": 1,
                            "17-20": 2
                        }
                    },
                    "recharge": "Short or Long Rest",
                    "restriction": "Only once per turn"
                }
            },
            {
                "id": "fighter_tactical_mind",
                "name": "Tactical Mind",
                "summary": "Expend a Second Wind use to add 1d10 to a failed ability check; use isn't expended if the check still fails.",
                "details": {
                    "benefit": "+1d10 to failed ability check",
                    "cost": "1 Second Wind use",
                    "special": "Not expended on failure"
                }
            }
        ],
        3: [
            {
                "id": "fighter_subclass",
                "name": "Fighter Subclass",
                "summary": "Choose a martial archetype: Battle Master, Champion, Eldritch Knight, or Psi Warrior.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": ["Battle Master", "Champion", "Eldritch Knight", "Psi Warrior"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        5: [
            {
                "id": "fighter_extra_attack",
                "name": "Extra Attack",
                "summary": "Attack twice when taking the Attack action."
            },
            {
                "id": "fighter_tactical_shift",
                "name": "Tactical Shift",
                "summary": "Move up to half your speed without provoking opportunity attacks when using Second Wind."
            }
        ],
        6: [
            {
                "id": "feat_or_asi_6",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        9: [
            {
                "id": "fighter_indomitable",
                "name": "Indomitable",
                "summary": "Reroll a failed saving throw with a bonus equal to your Fighter level.",
                "details": {
                    "uses": {
                        "type": "level-based",
                        "scaling": {
                            "9-12": 1,
                            "13-16": 2,
                            "17-20": 3
                        }
                    },
                    "recharge": "Long Rest",
                    "bonus": "Fighter Level"
                }
            },
            {
                "id": "fighter_tactical_master",
                "name": "Tactical Master",
                "summary": "Replace a weapon's mastery property with Push, Sap, or Slow for an attack.",
                "details": {
                    "options": ["Push", "Sap", "Slow"]
                }
            }
        ],
        11: [
            {
                "id": "fighter_extra_attack_2",
                "name": "Two Extra Attacks",
                "summary": "Attack three times when taking the Attack action."
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        13: [
            {
                "id": "fighter_studied_attacks",
                "name": "Studied Attacks",
                "summary": "Gain Advantage on your next attack roll against a creature if you miss it."
            }
        ],
        14: [
            {
                "id": "feat_or_asi_14",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat."
            }
        ],
        20: [
            {
                "id": "fighter_extra_attack_3",
                "name": "Three Extra Attacks",
                "summary": "Attack four times when taking the Attack action."
            }
        ]
    }
}

MONK = {
    "id": "monk",
    "name": "Monk",
    "description": """Monks are masters of martial arts who harness the energy within their bodies to achieve 
        extraordinary physical and mental feats. They value discipline and focus, transforming their own 
        bodies into lethal weapons while moving with supernatural speed and grace.""",
    "primary_ability": "Dexterity and Wisdom",
    "hit_die": "d8",
    "proficiencies": {
        "saving_throws": ["Strength", "Dexterity"],
        "armor": [],
        "weapons": ["Simple", "Martial (with Light property)"],
        "tools": {
            "granted": [],
            "choose": 1,
            "options": [
                "Alchemist's Supplies", "Brewer's Supplies", "Calligrapher's Supplies", "Carpenter's Tools",
                "Cartographer's Tools", "Cobbler's Tools", "Cook's Utensils", "Glassblower's Tools",
                "Jeweler's Tools", "Leatherworker's Tools", "Mason's Tools", "Painter's Supplies",
                "Potter's Tools", "Smith's Tools", "Tinker's Tools", "Weaver's Tools", "Woodcarver's Tools",
                "Bagpipes", "Drum", "Dulcimer", "Flute", "Horn", "Lute", "Lyre", "Pan Flute", "Shawm", "Viol"
            ]
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Acrobatics", "Athletics", "History", "Insight", "Religion", "Stealth"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Spear", "5 Daggers", "Artisan's Tools or Musical Instrument (choice)", "Explorer's Pack"],
            "gold": 11
        },
        "option_b": {
            "gold": 50
        }
    },
    "features": {
        1: [
            {
                "id": "monk_martial_arts",
                "name": "Martial Arts",
                "summary": "Use Dexterity for unarmed strikes and Monk weapons, roll Martial Arts dice for damage, and make an unarmed strike as a Bonus Action.",
                "details": {
                    "bonus_action_attack": "1 Unarmed Strike",
                    "die": {
                        "type": "level-based",
                        "scaling": {
                            "1-4": "1d6",
                            "5-10": "1d8",
                            "11-16": "1d10",
                            "17-20": "1d12"
                        }
                    },
                    "dex_for_unarmed": True,
                    "dex_save_dc": "8 + Proficiency Bonus + Dexterity modifier (for Grapple/Shove)"
                }
            },
            {
                "id": "monk_unarmored_defense",
                "name": "Unarmored Defense",
                "summary": "AC = 10 + DEX + WIS when not wearing armor or using a Shield."
            }
        ],
        2: [
            {
                "id": "monk_focus",
                "name": "Monk's Focus",
                "summary": "Harness Focus Points to fuel special features: Flurry of Blows, Patient Defense, and Step of the Wind.",
                "details": {
                    "points": {
                        "type": "level-based",
                        "scaling": {
                            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                            "11": 11, "12": 12, "13": 13, "14": 14, "15": 15, "16": 16, "17": 17, "18": 18, "19": 19, "20": 20
                        }
                    },
                    "recharge": "Short or Long Rest",
                    "save_dc": "8 + Proficiency Bonus + Wisdom modifier",
                    "effects": [
                        {
                            "name": "Flurry Of Blows",
                            "cost": "1 Focus Point",
                            "benefit": "Two Unarmed Strikes as a Bonus Action."
                        },
                        {
                            "name": "Patient Defense",
                            "cost": "0 or 1 Focus Point",
                            "benefit": "Bonus Action Disengage; or expend 1 point for both Disengage and Dodge."
                        },
                        {
                            "name": "Step Of The Wind",
                            "cost": "0 or 1 Focus Point",
                            "benefit": "Bonus Action Dash; or expend 1 point for both Disengage and Dash, with double jump distance."
                        }
                    ]
                }
            },
            {
                "id": "monk_unarmored_movement",
                "name": "Unarmored Movement",
                "summary": "Increase Speed while not wearing armor or using a Shield.",
                "details": {
                    "scaling": {
                        "2-5": "+10 ft",
                        "6-9": "+15 ft",
                        "10-13": "+20 ft",
                        "14-17": "+25 ft",
                        "18-20": "+30 ft"
                    }
                }
            },
            {
                "id": "monk_uncanny_metabolism",
                "name": "Uncanny Metabolism",
                "summary": "Once per Long Rest, regain all Focus Points and some HP when rolling Initiative.",
                "details": {
                    "trigger": "Initiative",
                    "healing": "Monk Level + Martial Arts Die",
                    "recharge": "Long Rest"
                }
            }
        ],
        3: [
            {
                "id": "monk_deflect_attacks",
                "name": "Deflect Attacks",
                "summary": "Use a Reaction to reduce damage from Bludgeoning, Piercing, or Slashing attacks.",
                "details": {
                    "reaction": "When hit by Physical attack",
                    "reduction": "1d10 + DEX + Monk Level",
                    "redirect_cost": "1 Focus Point (if damage reduced to 0)",
                    "redirect_damage": "2 Martial Arts Dice + DEX"
                }
            },
            {
                "id": "monk_subclass",
                "name": "Monk Subclass",
                "summary": "Choose a monastic tradition: Warrior of Mercy, Shadow, Elements, or Open Hand.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": ["Warrior of Mercy", "Warrior of Shadow", "Warrior of the Elements", "Warrior of the Open Hand"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            },
            {
                "id": "monk_slow_fall",
                "name": "Slow Fall",
                "summary": "Reduce falling damage by 5x Monk Level as a Reaction."
            }
        ],
        5: [
            {
                "id": "monk_extra_attack",
                "name": "Extra Attack",
                "summary": "Attack twice when taking the Attack action."
            },
            {
                "id": "monk_stunning_strike",
                "name": "Stunning Strike",
                "summary": "Expend 1 Focus Point to stun a target until your next turn on a failed Con save.",
                "details": {
                    "cost": "1 Focus Point",
                    "save": "Constitution",
                    "fail": "Stunned until start of next turn",
                    "success": "Speed halved, next attack against it has Advantage"
                }
            }
        ],
        6: [
            {
                "id": "monk_empowered_strikes",
                "name": "Empowered Strikes",
                "summary": "Unarmed strikes can deal Force damage instead of Bludgeoning."
            }
        ],
        7: [
            {
                "id": "monk_evasion",
                "name": "Evasion",
                "summary": "Take half damage on failed Dex saves and no damage on successes."
            }
        ],
        9: [
            {
                "id": "monk_acrobatic_movement",
                "name": "Acrobatic Movement",
                "summary": "Move along vertical surfaces and across liquids without falling."
            }
        ],
        10: [
            {
                "id": "monk_heightened_focus",
                "name": "Heightened Focus",
                "summary": "Your Flurry of Blows, Patient Defense, and Step of the Wind become more powerful.",
                "details": {
                    "flurry_upgrade": "Three Unarmed Strikes instead of two.",
                    "defense_upgrade": "Gain Temporary HP (2x Martial Arts dice).",
                    "step_upgrade": "Move a willing creature with you."
                }
            },
            {
                "id": "monk_self_restoration",
                "name": "Self-Restoration",
                "summary": "Remove Charmed, Frightened, or Poisoned at end of turn; no exhaustion from lack of food/drink."
            }
        ],
        13: [
            {
                "id": "monk_deflect_energy",
                "name": "Deflect Energy",
                "summary": "Deflect Attacks now works against any damage type."
            }
        ],
        14: [
            {
                "id": "monk_disciplined_survivor",
                "name": "Disciplined Survivor",
                "summary": "Proficiency in all saving throws; expend 1 Focus Point to reroll a failed save.",
                "details": {
                    "cost": "1 Focus Point (on failed save)",
                    "benefit": "Reroll saving throw"
                }
            }
        ],
        15: [
            {
                "id": "monk_perfect_focus",
                "name": "Perfect Focus",
                "summary": "Regain Focus Points up to 4 if you have 3 or fewer when rolling Initiative."
            }
        ],
        18: [
            {
                "id": "monk_superior_defense",
                "name": "Superior Defense",
                "summary": "Expend 3 Focus Points for 1 minute of resistance to all damage except Force.",
                "details": {
                    "cost": "3 Focus Points",
                    "duration": "1 minute",
                    "benefit": "Resistance to all damage except Force"
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat."
            }
        ],
        20: [
            {
                "id": "monk_body_and_mind",
                "name": "Body And Mind",
                "summary": "Dexterity and Wisdom scores increase by 4, to a maximum of 25."
            }
        ]
    }
}

PALADIN = {
    "id": "paladin",
    "name": "Paladin",
    "description": """Paladins are holy warriors bound by sacred oaths to serve a higher power or cause. 
        They combine martial prowess with divine magic, using their power to heal the wounded, 
        smite the wicked, and protect their allies with powerful auras of grace and courage.""",
    "primary_ability": "Strength and Charisma",
    "hit_die": "d10",
    "proficiencies": {
        "saving_throws": ["Wisdom", "Charisma"],
        "armor": ["Light", "Medium", "Heavy", "Shields"],
        "weapons": ["Simple", "Martial"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Athletics", "Insight", "Intimidation", "Medicine", "Persuasion", "Religion"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Chain Mail", "Shield", "Longsword", "6 Javelins", "Holy Symbol", "Priest's Pack"],
            "gold": 9
        },
        "option_b": {
            "gold": 150
        }
    },
    "spellcasting": {
        "ability": "Charisma",
        "progression": "half",
        "preparation_mode": "prepared",
        "focus": ["Holy Symbol"],
        "spells_prepared": {
            1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 6, 7: 7, 8: 7, 9: 9, 10: 9,
            11: 10, 12: 10, 13: 11, 14: 11, 15: 12, 16: 12, 17: 14, 18: 14, 19: 15, 20: 15
        }
    },
    "features": {
        1: [
            {
                "id": "paladin_lay_on_hands",
                "name": "Lay On Hands",
                "summary": "Use a healing pool (5x Paladin Level) to restore HP or remove Poisoned as a Bonus Action.",
                "details": {
                    "pool": "5 * Paladin Level",
                    "action": "Bonus Action",
                    "poison_removal_cost": 5
                }
            },
            {
                "id": "paladin_spellcasting",
                "name": "Spellcasting",
                "summary": "Cast Paladin spells using Charisma and a Holy Symbol; swap one spell after a Long Rest."
            },
            {
                "id": "paladin_weapon_mastery",
                "name": "Weapon Mastery",
                "summary": "Use mastery properties of two weapons; can change choices after a Long Rest.",
                "details": {
                    "masteries": 2
                }
            }
        ],
        2: [
            {
                "id": "paladin_fighting_style",
                "name": "Fighting Style",
                "summary": "Gain a Fighting Style feat or choose Blessed Warrior for two Cleric cantrips.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": [
                            {"name": "Fighting Style Feat", "type": "fighting_style_feat"},
                            {"name": "Blessed Warrior", "benefit": "2 Cleric cantrips (Charisma-based)"}
                        ]
                    }
                }
            },
            {
                "id": "paladin_smite",
                "name": "Paladin's Smite",
                "summary": "Divine Smite is always prepared; can cast it once per Long Rest without a spell slot.",
                "details": {
                    "spells_granted": ["Divine Smite"],
                    "free_cast": "1/Long Rest"
                }
            }
        ],
        3: [
            {
                "id": "paladin_channel_divinity",
                "name": "Channel Divinity",
                "summary": "Harness divine energy for effects like Divine Sense.",
                "details": {
                    "uses": {
                        "type": "level-based",
                        "scaling": {
                            "3-10": 2,
                            "11-20": 3
                        }
                    },
                    "recharge": "Short Rest (regain 1), Long Rest (regain all)",
                    "effects": [
                        {
                            "name": "Divine Sense",
                            "action": "Bonus Action",
                            "duration": "10 minutes",
                            "benefit": "Identify Celestial, Fiend, or Undead within 60ft."
                        }
                    ]
                }
            },
            {
                "id": "paladin_subclass",
                "name": "Paladin Subclass",
                "summary": "Choose a Sacred Oath: Devotion, Glory, Ancients, or Vengeance.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": ["Oath Of Devotion", "Oath Of Glory", "Oath Of The Ancients", "Oath Of Vengeance"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        5: [
            {
                "id": "paladin_extra_attack",
                "name": "Extra Attack",
                "summary": "Attack twice when taking the Attack action."
            },
            {
                "id": "paladin_faithful_steed",
                "name": "Faithful Steed",
                "summary": "Find Steed is always prepared; can cast it once per Long Rest without a spell slot.",
                "details": {
                    "spells_granted": ["Find Steed"],
                    "free_cast": "1/Long Rest"
                }
            }
        ],
        6: [
            {
                "id": "paladin_aura_of_protection",
                "name": "Aura Of Protection",
                "summary": "You and allies within 10ft gain a bonus to saving throws equal to your Charisma modifier.",
                "details": {
                    "range": "10 ft",
                    "bonus": "Charisma modifier (min +1)"
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        9: [
            {
                "id": "paladin_abjure_foes",
                "name": "Abjure Foes",
                "summary": "Expend a Channel Divinity use to Frighten multiple creatures within 60ft.",
                "details": {
                    "action": "Magic action",
                    "cost": "1 Channel Divinity use",
                    "targets": "Charisma modifier (min 1)",
                    "range": "60 ft"
                }
            }
        ],
        10: [
            {
                "id": "paladin_aura_of_courage",
                "name": "Aura Of Courage",
                "summary": "You and allies in your aura have immunity to the Frightened condition."
            }
        ],
        11: [
            {
                "id": "paladin_radiant_strikes",
                "name": "Radiant Strikes",
                "summary": "Melee attacks and unarmed strikes deal an extra 1d8 Radiant damage.",
                "details": {
                    "extra_uses": {
                        "type": "level-based",
                        "scaling": {
                            "11-20": 3
                        },
                        "note": "Gain 3rd Channel Divinity use at level 11"
                    }
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        14: [
            {
                "id": "paladin_restoring_touch",
                "name": "Restoring Touch",
                "summary": "Lay On Hands can remove several conditions (Blinded, Charmed, etc.) for 5 points each.",
                "details": {
                    "conditions": ["Blinded", "Charmed", "Deafened", "Frightened", "Paralyzed", "Stunned"],
                    "cost_per_condition": 5
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        18: [
            {
                "id": "paladin_aura_expansion",
                "name": "Aura Expansion",
                "summary": "Your Aura of Protection range increases to 30ft."
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat."
            }
        ]
    }
}

RANGER = {
    "id": "ranger",
    "name": "Ranger",
    "description": """Rangers are masters of the wilderness, combining martial skill with primal magic. 
        They excel at tracking and hunting dangerous foes, using their deep connection to nature to 
        navigate treacherous terrain and strike with deadly precision.""",
    "primary_ability": "Dexterity and Wisdom",
    "hit_die": "d10",
    "proficiencies": {
        "saving_throws": ["Strength", "Dexterity"],
        "armor": ["Light", "Medium", "Shields"],
        "weapons": ["Simple", "Martial"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 3,
            "options": ["Animal Handling", "Athletics", "Insight", "Investigation", "Nature", "Perception", "Stealth", "Survival"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Studded Leather Armor", "Scimitar", "Shortsword", "Longbow", "20 Arrows", "Quiver", "Druidic Focus (spring of mistletoe)", "Explorer's Pack"],
            "gold": 7
        },
        "option_b": {
            "gold": 150
        }
    },
    "spellcasting": {
        "ability": "Wisdom",
        "progression": "half",
        "preparation_mode": "prepared",
        "focus": ["Druidic Focus"],
        "spells_prepared": {
            1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 6, 7: 7, 8: 7, 9: 9, 10: 9,
            11: 10, 12: 10, 13: 11, 14: 11, 15: 12, 16: 12, 17: 14, 18: 14, 19: 15, 20: 15
        }
    },
    "features": {
        1: [
            {
                "id": "ranger_spellcasting",
                "name": "Spellcasting",
                "summary": "Cast Ranger spells using Wisdom and a Druidic Focus; swap one spell after a Long Rest.",
                "details": {
                    "spells_lvl_1": 2
                }
            },
            {
                "id": "ranger_favored_enemy",
                "name": "Favored Enemy",
                "summary": "Hunter's Mark is always prepared; can cast it without a spell slot several times per Long Rest.",
                "details": {
                    "spells_granted": ["Hunter's Mark"],
                    "free_casts": {
                        "type": "level-based",
                        "scaling": {
                            "1-4": 2,
                            "5-8": 3,
                            "9-12": 4,
                            "13-16": 5,
                            "17-20": 6
                        }
                    },
                    "recharge": "Long Rest"
                }
            },
            {
                "id": "ranger_weapon_mastery",
                "name": "Weapon Mastery",
                "summary": "Use mastery properties of two weapons; can change choices after a Long Rest.",
                "details": {
                    "masteries": 2
                }
            }
        ],
        2: [
            {
                "id": "ranger_deft_explorer",
                "name": "Deft Explorer",
                "summary": "Gain Expertise in one skill and learn two languages.",
                "details": {
                    "expertise_choice": 1,
                    "languages": 2
                }
            },
            {
                "id": "ranger_fighting_style",
                "name": "Fighting Style",
                "summary": "Gain a Fighting Style feat or choose Druidic Warrior for two Druid cantrips.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": [
                            {"name": "Fighting Style Feat", "type": "fighting_style_feat"},
                            {"name": "Druidic Warrior", "benefit": "2 Druid cantrips (Wisdom-based)"}
                        ]
                    }
                }
            }
        ],
        3: [
            {
                "id": "ranger_subclass",
                "name": "Ranger Subclass",
                "summary": "Choose a Ranger Archetype: Beast Master, Fey Wanderer, Gloom Stalker, or Hunter.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": ["Beast Master", "Fey Wanderer", "Gloom Stalker", "Hunter"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        5: [
            {
                "id": "ranger_extra_attack",
                "name": "Extra Attack",
                "summary": "Attack twice when taking the Attack action."
            }
        ],
        6: [
            {
                "id": "ranger_roving",
                "name": "Roving",
                "summary": "Speed increases by 10ft when not wearing heavy armor; gain Climb and Swim speeds.",
                "details": {
                    "speed_bonus": "+10 ft",
                    "modes": ["Climb", "Swim"],
                    "restriction": "No Heavy Armor"
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        9: [
            {
                "id": "ranger_expertise",
                "name": "Expertise",
                "summary": "Gain Expertise in two more skill proficiencies.",
                "details": {
                    "expertise_choice": 2
                }
            }
        ],
        10: [
            {
                "id": "ranger_tireless",
                "name": "Tireless",
                "summary": "Give yourself Temporary HP and decrease Exhaustion level on a Short Rest.",
                "details": {
                    "temp_hp": "1d8 + Wisdom modifier",
                    "temp_hp_uses": "Wisdom modifier (min 1)",
                    "exhaustion_recovery": "Short Rest decreases level by 1",
                    "recharge": "Long Rest"
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        13: [
            {
                "id": "ranger_relentless_hunter",
                "name": "Relentless Hunter",
                "summary": "Damage cannot break your Concentration on Hunter's Mark."
            }
        ],
        14: [
            {
                "id": "ranger_natures_veil",
                "name": "Nature's Veil",
                "summary": "Use a Bonus Action to become Invisible until the end of your next turn.",
                "details": {
                    "action": "Bonus Action",
                    "uses": "Wisdom modifier (min 1)",
                    "recharge": "Long Rest"
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        17: [
            {
                "id": "ranger_precise_hunter",
                "name": "Precise Hunter",
                "summary": "Advantage on attack rolls against the creature marked by your Hunter's Mark."
            }
        ],
        18: [
            {
                "id": "ranger_feral_senses",
                "name": "Feral Senses",
                "summary": "Gain Blindsight with a range of 30ft.",
                "details": {
                    "range": "30 ft"
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat."
            }
        ],
        20: [
            {
                "id": "ranger_foe_slayer",
                "name": "Foe Slayer",
                "summary": "Hunter's Mark damage die increases to d10."
            }
        ]
    }
}

ROGUE = {
    "id": "rogue",
    "name": "Rogue",
    "description": """Rogues are masters of stealth, skill, and precision. They excel at exploiting 
        their enemies' weaknesses, striking with deadly accuracy when their foes are distracted, 
        and using a vast array of tools and talents to overcome any obstacle.""",
    "primary_ability": "Dexterity",
    "hit_die": "d8",
    "proficiencies": {
        "saving_throws": ["Dexterity", "Intelligence"],
        "armor": ["Light"],
        "weapons": ["Simple", "Martial (with Finesse or Light properties)"],
        "tools": {
            "granted": ["Thieves' Tools"],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 4,
            "options": ["Acrobatics", "Athletics", "Deception", "Insight", "Intimidation", "Investigation", "Perception", "Persuasion", "Sleight of Hand", "Stealth"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Leather Armor", "2 Daggers", "Shortsword", "Shortbow", "20 Arrows", "Quiver", "Thieves' Tools", "Burglar's Pack"],
            "gold": 8
        },
        "option_b": {
            "gold": 100
        }
    },
    "features": {
        1: [
            {
                "id": "rogue_expertise_1",
                "name": "Expertise",
                "summary": "Gain Expertise in two of your skill proficiencies.",
                "details": {
                    "expertise_choice": 2
                }
            },
            {
                "id": "rogue_sneak_attack",
                "name": "Sneak Attack",
                "summary": "Deal extra damage once per turn when attacking with Advantage or an ally nearby.",
                "details": {
                    "die": {
                        "type": "level-based",
                        "formula": "(level + 1) // 2",
                        "scaling": {
                            "1-2": "1d6", "3-4": "2d6", "5-6": "3d6", "7-8": "4d6", "9-10": "5d6",
                            "11-12": "6d6", "13-14": "7d6", "15-16": "8d6", "17-18": "9d6", "19-20": "10d6"
                        }
                    },
                    "restriction": "Finesse or Ranged weapon"
                }
            },
            {
                "id": "rogue_thieves_cant",
                "name": "Thieves' Cant",
                "summary": "You know Thieves' Cant and one other language of your choice.",
                "details": {
                    "languages": ["Thieves' Cant", "Choice of 1"]
                }
            },
            {
                "id": "rogue_weapon_mastery",
                "name": "Weapon Mastery",
                "summary": "Use mastery properties of two weapons; can change choices after a Long Rest.",
                "details": {
                    "masteries": 2
                }
            }
        ],
        2: [
            {
                "id": "rogue_cunning_action",
                "name": "Cunning Action",
                "summary": "On your turn, you can take a Bonus Action to Dash, Disengage, or Hide."
            }
        ],
        3: [
            {
                "id": "rogue_subclass",
                "name": "Rogue Subclass",
                "summary": "Choose a Rogue Archetype: Arcane Trickster, Assassin, Soulknife, or Thief.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": ["Arcane Trickster", "Assassin", "Soulknife", "Thief"]
                    }
                }
            },
            {
                "id": "rogue_steady_aim",
                "name": "Steady Aim",
                "summary": "Bonus Action to gain Advantage on next attack; reduces speed to 0.",
                "details": {
                    "action": "Bonus Action",
                    "restriction": "Cannot have moved, reduces speed to 0 for turn"
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        5: [
            {
                "id": "rogue_cunning_strike",
                "name": "Cunning Strike",
                "summary": "Forgo Sneak Attack damage dice to add special effects to your strike.",
                "details": {
                    "effects": [
                        {"name": "Poison", "cost": "1d6", "save": "Constitution", "fail": "Poisoned (1 min)"},
                        {"name": "Trip", "cost": "1d6", "save": "Dexterity", "fail": "Prone (Large or smaller)"},
                        {"name": "Withdraw", "cost": "1d6", "benefit": "Move half speed without Opportunity Attacks"}
                    ],
                    "save_dc": "8 + Proficiency Bonus + Dexterity modifier"
                }
            },
            {
                "id": "rogue_uncanny_dodge",
                "name": "Uncanny Dodge",
                "summary": "Use a Reaction to halve damage from an attack you can see."
            }
        ],
        6: [
            {
                "id": "rogue_expertise_6",
                "name": "Expertise",
                "summary": "Gain Expertise in two more skill proficiencies.",
                "details": {
                    "expertise_choice": 2
                }
            }
        ],
        7: [
            {
                "id": "rogue_evasion",
                "name": "Evasion",
                "summary": "Take half damage on failed Dex saves and no damage on successes."
            },
            {
                "id": "rogue_reliable_talent",
                "name": "Reliable Talent",
                "summary": "Treat any d20 roll of 9 or lower as a 10 for skill and tool checks you are proficient in."
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        10: [
            {
                "id": "feat_or_asi_10",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores (Unique extra feat for Rogues)."
            }
        ],
        11: [
            {
                "id": "rogue_improved_cunning_strike",
                "name": "Improved Cunning Strike",
                "summary": "Use up to two Cunning Strike effects simultaneously, paying the total cost."
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        14: [
            {
                "id": "rogue_devious_strikes",
                "name": "Devious Strikes",
                "summary": "Unlock more powerful Cunning Strike options.",
                "details": {
                    "additional_effects": [
                        {"name": "Daze", "cost": "2d6", "save": "Constitution", "fail": "Limited to move, Action, or Bonus Action"},
                        {"name": "Knock Out", "cost": "6d6", "save": "Constitution", "fail": "Unconscious (1 min or damage)"},
                        {"name": "Obscure", "cost": "3d6", "save": "Dexterity", "fail": "Blinded until end of next turn"}
                    ]
                }
            }
        ],
        15: [
            {
                "id": "rogue_slippery_mind",
                "name": "Slippery Mind",
                "summary": "Gain proficiency in Wisdom and Charisma saving throws.",
                "details": {
                    "saving_throws_granted": ["Wisdom", "Charisma"]
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        18: [
            {
                "id": "rogue_elusive",
                "name": "Elusive",
                "summary": "Attack rolls cannot have Advantage against you unless you are Incapacitated."
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat."
            }
        ],
        20: [
            {
                "id": "rogue_stroke_of_luck",
                "name": "Stroke Of Luck",
                "summary": "Turn a failed d20 test into a 20.",
                "details": {
                    "recharge": "Short or Long Rest"
                }
            }
        ]
    }
}

SORCERER = {
    "id": "sorcerer",
    "name": "Sorcerer",
    "description": """Sorcerers carry a magical birthright conferred upon them by an exotic bloodline, 
        some otherworldly influence, or exposure to unknown cosmic forces. Their magic is not 
        studied but innate, flowing from a wellspring of power within.""",
    "primary_ability": "Charisma",
    "hit_die": "d6",
    "proficiencies": {
        "saving_throws": ["Constitution", "Charisma"],
        "armor": [],
        "weapons": ["Simple"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Arcana", "Deception", "Insight", "Intimidation", "Persuasion", "Religion"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Spear", "2 Daggers", "Arcane Focus (crystal)", "Dungeoneer's Pack"],
            "gold": 28
        },
        "option_b": {
            "gold": 50
        }
    },
    "spellcasting": {
        "ability": "Charisma",
        "progression": "full",
        "preparation_mode": "learned",
        "focus": ["Arcane Focus"],
        "cantrips_known": {1: 4, 4: 5, 10: 6},
        "spells_prepared": {
            1: 2, 2: 4, 3: 6, 4: 7, 5: 9, 6: 10, 7: 11, 8: 12, 9: 14, 10: 15,
            11: 16, 12: 16, 13: 17, 14: 17, 15: 18, 16: 18, 17: 19, 18: 20, 19: 21, 20: 22
        }
    },
    "features": {
        1: [
            {
                "id": "sorcerer_spellcasting",
                "name": "Spellcasting",
                "summary": "Cast Sorcerer spells using Charisma and an Arcane Focus; can swap one spell on level up."
            },
            {
                "id": "sorcerer_innate_sorcery",
                "name": "Innate Sorcery",
                "summary": "Use a Bonus Action to unleash magic for 1 minute, increasing Spell Save DC and gaining Advantage on spell attacks.",
                "details": {
                    "action": "Bonus Action",
                    "duration": "1 minute",
                    "uses": 2,
                    "recharge": "Long Rest",
                    "benefits": ["+1 to Spell Save DC", "Advantage on Sorcerer spell attack rolls"]
                }
            }
        ],
        2: [
            {
                "id": "sorcerer_font_of_magic",
                "name": "Font Of Magic",
                "summary": "Harness Sorcery Points to create spell slots or fuel Metamagic.",
                "details": {
                    "points": {
                        "type": "level-based",
                        "scaling": {
                            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                            "11": 11, "12": 12, "13": 13, "14": 14, "15": 15, "16": 16, "17": 17, "18": 18, "19": 19, "20": 20
                        }
                    },
                    "recharge": "Long Rest",
                    "flexible_casting": {
                        "slot_creation_costs": {
                            "1": 2, "2": 3, "3": 5, "4": 6, "5": 7
                        }
                    }
                }
            },
            {
                "id": "sorcerer_metamagic",
                "name": "Metamagic",
                "summary": "Alter your spells using Sorcery Points.",
                "details": {
                    "options_known": {
                        "type": "level-based",
                        "scaling": {
                            "2-9": 2,
                            "10-16": 4,
                            "17-20": 6
                        }
                    }
                }
            }
        ],
        3: [
            {
                "id": "sorcerer_subclass",
                "name": "Sorcerer Subclass",
                "summary": "Choose a Sorcerous Origin: Aberrant, Clockwork, Draconic, or Wild Magic.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": ["Aberrant Sorcery", "Clockwork Sorcery", "Draconic Sorcery", "Wild Magic Sorcery"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        5: [
            {
                "id": "sorcerer_sorcerous_restoration",
                "name": "Sorcerous Restoration",
                "summary": "Once per Long Rest, regain Sorcery Points equal to half your level on a Short Rest.",
                "details": {
                    "trigger": "Short Rest",
                    "amount": "Level / 2 (round down)",
                    "recharge": "Long Rest"
                }
            }
        ],
        7: [
            {
                "id": "sorcerer_sorcery_incarnate",
                "name": "Sorcery Incarnate",
                "summary": "Spend 2 Sorcery Points to activate Innate Sorcery; use up to two Metamagics per spell while active.",
                "details": {
                    "cost_to_activate": "2 Sorcery Points",
                    "benefit": "Dual Metamagic use while Innate Sorcery is active"
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat."
            }
        ],
        20: [
            {
                "id": "sorcerer_arcane_apotheosis",
                "name": "Arcane Apotheosis",
                "summary": "While Innate Sorcery is active, use one Metamagic per turn for free.",
                "details": {
                    "benefit": "Free Metamagic once per turn during Innate Sorcery"
                }
            }
        ]
    }
}

WARLOCK = {
    "id": "warlock",
    "name": "Warlock",
    "description": """Warlocks are seekers of knowledge that lie hidden in the fabric of the multiverse. 
        Through pacts made with mysterious beings of great power, warlocks unlock magical effects, 
        both subtle and spectacular.""",
    "primary_ability": "Charisma",
    "hit_die": "d8",
    "proficiencies": {
        "saving_throws": ["Wisdom", "Charisma"],
        "armor": ["Light"],
        "weapons": ["Simple"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Arcana", "Deception", "History", "Intimidation", "Investigation", "Nature", "Religion"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Leather Armor", "Sickle", "2 Daggers", "Arcane Focus (orb)", "Book (occult lore)", "Scholar's Pack"],
            "gold": 15
        },
        "option_b": {
            "gold": 100
        }
    },
    "spellcasting": {
        "ability": "Charisma",
        "progression": "pact",
        "preparation_mode": "learned",
        "focus": ["Arcane Focus"],
        "cantrips_known": {1: 2, 4: 3, 10: 4},
        "spells_prepared": {
            1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 10,
            11: 11, 12: 11, 13: 12, 14: 12, 15: 13, 16: 13, 17: 14, 18: 14, 19: 15, 20: 15
        }
    },
    "features": {
        1: [
            {
                "id": "warlock_eldritch_invocations",
                "name": "Eldritch Invocations",
                "summary": "Gain fragments of forbidden knowledge that grant you magical abilities.",
                "details": {
                    "invocations_known": {
                        "type": "level-based",
                        "scaling": {
                            "1": 1, "2": 3, "5": 5, "7": 6, "9": 7, "12": 8, "15": 9, "18": 10
                        }
                    }
                }
            },
            {
                "id": "warlock_pact_magic",
                "name": "Pact Magic",
                "summary": "Cast Warlock spells using Charisma and an Arcane Focus; slots recharge on a Short Rest."
            }
        ],
        2: [
            {
                "id": "warlock_magical_cunning",
                "name": "Magical Cunning",
                "summary": "Once per Long Rest, spend 1 minute to regain half your Pact Magic spell slots (round up).",
                "details": {
                    "recharge": "Long Rest",
                    "benefit": "Regain half Pact Magic slots (round up)"
                }
            }
        ],
        3: [
            {
                "id": "warlock_subclass",
                "name": "Warlock Subclass",
                "summary": "Choose a Otherworldly Patron: Archfey, Celestial, Fiend, or Great Old One.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": ["Archfey Patron", "Celestial Patron", "Fiend Patron", "Great Old One Patron"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        9: [
            {
                "id": "warlock_contact_patron",
                "name": "Contact Patron",
                "summary": "Contact Other Plane is always prepared; cast it once for free with auto-success to contact your patron.",
                "details": {
                    "spells_granted": ["Contact Other Plane"],
                    "free_cast_benefit": "Auto-success on saving throw",
                    "recharge": "Long Rest"
                }
            }
        ],
        11: [
            {
                "id": "warlock_mystic_arcanum_6",
                "name": "Mystic Arcanum (Level 6)",
                "summary": "Choose a level 6 Warlock spell to cast once per Long Rest without a spell slot.",
                "details": {
                    "arcanum_level": 6,
                    "recharge": "Long Rest"
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        13: [
            {
                "id": "warlock_mystic_arcanum_7",
                "name": "Mystic Arcanum (Level 7)",
                "summary": "Choose a level 7 Warlock spell to cast once per Long Rest without a spell slot.",
                "details": {
                    "arcanum_level": 7,
                    "recharge": "Long Rest"
                }
            }
        ],
        15: [
            {
                "id": "warlock_mystic_arcanum_8",
                "name": "Mystic Arcanum (Level 8)",
                "summary": "Choose a level 8 Warlock spell to cast once per Long Rest without a spell slot.",
                "details": {
                    "arcanum_level": 8,
                    "recharge": "Long Rest"
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        17: [
            {
                "id": "warlock_mystic_arcanum_9",
                "name": "Mystic Arcanum (Level 9)",
                "summary": "Choose a level 9 Warlock spell to cast once per Long Rest without a spell slot.",
                "details": {
                    "arcanum_level": 9,
                    "recharge": "Long Rest"
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat."
            }
        ],
        20: [
            {
                "id": "warlock_eldritch_master",
                "name": "Eldritch Master",
                "summary": "Magical Cunning now regains all expended Pact Magic spell slots."
            }
        ]
    }
}

WIZARD = {
    "id": "wizard",
    "name": "Wizard",
    "description": """Wizards are supreme magic-users, defined and united as a class by the spells 
        they cast. Drawing on the subtle weave of magic that permeates the cosmos, wizards cast 
        spells of explosive fire, arcing lightning, subtle deception, and brute-force mind control.""",
    "primary_ability": "Intelligence",
    "hit_die": "d6",
    "proficiencies": {
        "saving_throws": ["Intelligence", "Wisdom"],
        "armor": [],
        "weapons": ["Simple"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Arcana", "History", "Insight", "Investigation", "Medicine", "Nature", "Religion"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["2 Daggers", "Arcane Focus (Quarterstaff)", "Robe", "Spellbook", "Scholar's Pack"],
            "gold": 5
        },
        "option_b": {
            "gold": 55
        }
    },
    "spellcasting": {
        "ability": "Intelligence",
        "progression": "full",
        "preparation_mode": "prepared",
        "focus": ["Arcane Focus", "Spellbook"],
        "cantrips_known": {1: 3, 4: 4, 10: 5},
        "spells_prepared": {
            1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9, 7: 10, 8: 11, 9: 12, 10: 13,
            11: 16, 12: 16, 13: 17, 14: 18, 15: 19, 16: 20, 17: 21, 18: 22, 19: 23, 20: 25
        },
        "spellbook": {
            "initial_spells": 6,
            "spells_per_level": 2,
            "weight": "3 lbs",
            "pages": 100
        }
    },
    "features": {
        1: [
            {
                "id": "wizard_spellcasting",
                "name": "Spellcasting",
                "summary": "Cast Wizard spells using Intelligence; replace one cantrip after a Long Rest."
            },
            {
                "id": "wizard_ritual_adept",
                "name": "Ritual Adept",
                "summary": "Cast any Wizard spell in your spellbook as a ritual if it has the Ritual tag, even if not prepared."
            },
            {
                "id": "wizard_arcane_recovery",
                "name": "Arcane Recovery",
                "summary": "Regain spell slots on a Short Rest equal to half your Wizard level (max level 5 slots).",
                "details": {
                    "recharge": "Long Rest",
                    "max_slot_level": 5,
                    "recovery_amount": "Wizard Level / 2 (round up)"
                }
            }
        ],
        2: [
            {
                "id": "wizard_scholar",
                "name": "Scholar",
                "summary": "Gain Expertise in one proficient academic skill.",
                "details": {
                    "expertise_choice_options": ["Arcana", "History", "Investigation", "Medicine", "Nature", "Religion"]
                }
            }
        ],
        3: [
            {
                "id": "wizard_subclass",
                "name": "Wizard Subclass",
                "summary": "Choose an Arcane Tradition: Abjurer, Diviner, Evoker, or Illusionist.",
                "details": {
                    "choice": {
                        "choose": 1,
                        "options": ["Abjurer", "Diviner", "Evoker", "Illusionist"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        5: [
            {
                "id": "wizard_memorize_spell",
                "name": "Memorize Spell",
                "summary": "After a Short Rest, swap one prepared level 1+ spell for another in your spellbook."
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores."
            }
        ],
        18: [
            {
                "id": "wizard_spell_mastery",
                "name": "Spell Mastery",
                "summary": "Cast a chosen level 1 and level 2 spell at will; can swap choices after a Long Rest.",
                "details": {
                    "at_will_levels": [1, 2]
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat."
            }
        ],
        20: [
            {
                "id": "wizard_signature_spell",
                "name": "Signature Spell",
                "summary": "Choose two level 3 spells to cast once each per Short/Long Rest without a spell slot.",
                "details": {
                    "signature_level": 3,
                    "recharge": "Short or Long Rest"
                }
            }
        ]
    }
}






