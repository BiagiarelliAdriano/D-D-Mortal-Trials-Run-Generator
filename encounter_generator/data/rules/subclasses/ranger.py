"""
Subclass definitions for the Ranger class.
"""

RANGER_SUBCLASSES = {
    "beast_master": {
        "id": "beast_master",
        "name": "Beast Master",
        "description": "Beast Masters represent the ideal of the hunter and their loyal companion. By bonding with a primal beast, these rangers combine their own martial skill with the ferocity of the wild, creating a unified force that can strike from land, sea, or sky.",
        "features": {
            3: [
                {
                    "id": "beast_master_primal_companion",
                    "name": "Primal Companion",
                    "summary": "Summon a primal beast (Land, Sea, or Sky). Command it as a Bonus Action or by forgoing an attack.",
                    "details": {
                        "types": ["Beast of the Land", "Beast of the Sea", "Beast of the Sky"],
                        "command": "Bonus Action to command (or forgo 1 attack from Attack action for Beast's Strike)",
                        "combat": "Acts on your turn; Dodges unless commanded",
                        "revival": "Magic Action + Spell Slot (1 min casting time) if died within 1 hour",
                        "summons": "Change beast type/appearance on Long Rest"
                    }
                }
            ],
            7: [
                {
                    "id": "beast_master_exceptional_training",
                    "name": "Exceptional Training",
                    "summary": "Command beast as a BA to Dash, Disengage, Dodge, or Help. Beast can deal Force damage.",
                    "details": {
                        "bonus_action_commands": ["Dash", "Disengage", "Dodge", "Help"],
                        "damage_type_choice": "Force or normal damage type on hit"
                    }
                }
            ],
            11: [
                {
                    "id": "beast_master_bestial_fury",
                    "name": "Bestial Fury",
                    "summary": "Beast's Strike can be used twice. Beast deals extra Force damage to Hunter's Mark targets.",
                    "details": {
                        "beasts_strike_multiattack": "Beast uses Beast's Strike twice when commanded",
                        "hunters_mark_synergy": "Deals extra Force damage (equal to Hunter's Mark bonus) on first hit per turn vs marked target"
                    }
                }
            ],
            15: [
                {
                    "id": "beast_master_share_spell",
                    "name": "Share Spell",
                    "summary": "Spells targeting yourself also affect your companion within 30ft.",
                    "details": {
                        "range": "30ft",
                        "effect": "Any spell you cast targeting yourself affects both you and your beast"
                    }
                }
            ]
        }
    },
    "fey_wanderer": {
        "id": "fey_wanderer",
        "name": "Fey Wanderer",
        "description": "As a Fey Wanderer, you tread with one foot in the Mortal Realm and the other in the Fey Realm. You bring the joy and the terror of the Fey to your enemies and allies alike, wielding the power of your otherworldly charm and the sting of psychic trauma.",
        "features": {
            3: [
                {
                    "id": "fey_wanderer_spells",
                    "name": "Fey Wanderer Spells",
                    "summary": "You always have certain spells prepared as you gain levels in this class.",
                    "details": {
                        "spells": {
                            3: ["Charm Person"],
                            5: ["Misty Step"],
                            9: ["Summon Fey"],
                            13: ["Dimension Door"],
                            17: ["Mislead"]
                        },
                        "fey_gift": "You possess a fey blessing (e.g., illusory butterflies, dancing shadow, or antlers)."
                    }
                },
                {
                    "id": "fey_wanderer_dreadful_strike",
                    "name": "Dreadful Strike",
                    "summary": "Once per turn, deal extra Psychic damage (1d4, increases at lvl 11) on a weapon hit.",
                    "details": {
                        "damage": "1d4 Psychic (increases to 1d6 at level 11)",
                        "limit": "Once per turn"
                    }
                },
                {
                    "id": "fey_wanderer_otherworldly_glamour",
                    "name": "Otherworldly Glamour",
                    "summary": "Gain a bonus to Charisma checks equal to Wisdom mod. Gain proficiency in one Charisma skill.",
                    "details": {
                        "bonus": "Wisdom modifier (min +1) to all Charisma checks",
                        "skill_choice": ["Deception", "Performance", "Persuasion"]
                    }
                }
            ],
            7: [
                {
                    "id": "fey_wanderer_beguiling_twist",
                    "name": "Beguiling Twist",
                    "summary": "Advantage on saves vs Charm/Fear. Reaction: redirect a successful Charm/Fear save to a new target within 120ft.",
                    "details": {
                        "passive": "Advantage on saving throws to avoid or end Charmed or Frightened",
                        "action": "Reaction",
                        "trigger": "Creature within 120ft succeeds on a save vs Charms or Fear",
                        "effect": "Force a different creature (120ft) to make Wisdom save or be Charmed/Frightened for 1 min"
                    }
                }
            ],
            11: [
                {
                    "id": "fey_wanderer_fey_reinforcements",
                    "name": "Fey Reinforcements",
                    "summary": "Cast Summon Fey without components or once per Long Rest for free. Can remove concentration (1 min duration).",
                    "details": {
                        "free_cast": "1/Long Rest without a spell slot",
                        "material_bypass": "No material components required",
                        "concentration_buff": "Can cast without Concentration (duration reduces to 1 minute)"
                    }
                }
            ],
            15: [
                {
                    "id": "fey_wanderer_misty_wanderer",
                    "name": "Misty Wanderer",
                    "summary": "Cast Misty Step for free (Wis mod/Long Rest) and bring a passenger.",
                    "details": {
                        "free_casts": "Wisdom modifier (minimum 1)",
                        "recharge": "Long Rest",
                        "passenger": "Bring one willing creature within 5ft to an unoccupied space within 5ft of destination"
                    }
                }
            ]
        }
    },
    "gloom_stalker": {
        "id": "gloom_stalker",
        "name": "Gloom Stalker",
        "description": "Gloom Stalkers are at home in the darkest places: deep under the earth, in gloomy alleyways, and in primeval forests. Most people fear the dark, but a Gloom Stalker ventures into it with confidence, seeking to ambush threats before they can reach the light.",
        "features": {
            3: [
                {
                    "id": "gloom_stalker_spells",
                    "name": "Gloom Stalker Spells",
                    "summary": "You always have certain spells prepared as you gain levels in this class.",
                    "details": {
                        "spells": {
                            3: ["Disguise Self"],
                            5: ["Rope Trick"],
                            9: ["Fear"],
                            13: ["Greater Invisibility"],
                            17: ["Seeming"]
                        }
                    }
                },
                {
                    "id": "gloom_stalker_dread_ambusher",
                    "name": "Dread Ambusher",
                    "summary": "Combat start: +10ft Speed. Weapons deal +2d6 Psychic damage (once per turn, Wis mod/LR). Add Wis mod to Initiative.",
                    "details": {
                        "speed_boost": "+10ft Speed on first turn of combat",
                        "extra_damage": "2d6 Psychic (once per turn; increases to 2d8 at lvl 11)",
                        "damage_uses": "Wisdom modifier (minimum 1)",
                        "damage_recharge": "Long Rest",
                        "initiative_bonus": "Add Wisdom modifier to Initiative rolls"
                    }
                },
                {
                    "id": "gloom_stalker_umbral_sight",
                    "name": "Umbral Sight",
                    "summary": "Gain or increase Darkvision (60ft). You are Invisible to creatures using Darkvision in total darkness.",
                    "details": {
                        "darkvision": "60ft (or +60ft if already possessed)",
                        "invisibility": "Invisible to any creature that relies on Darkvision to see you while in total darkness"
                    }
                }
            ],
            7: [
                {
                    "id": "gloom_stalker_iron_mind",
                    "name": "Iron Mind",
                    "summary": "Gain proficiency in Wisdom saving throws (or Int/Cha if already proficient).",
                    "details": {
                        "proficiency": "Wisdom saving throws",
                        "alternative": "Intelligence or Charisma if already proficient in Wisdom"
                    }
                }
            ],
            11: [
                {
                    "id": "gloom_stalker_stalkers_flurry",
                    "name": "Stalker's Flurry",
                    "summary": "Dread Ambusher damage becomes 2d8. Dealing extra damage allows an extra attack or AoE Fear effect.",
                    "details": {
                        "damage_upgrade": "Dread Ambusher extra damage becomes 2d8",
                        "flurry_options": [
                            "Make an extra attack vs a different creature within 5ft of target",
                            "Wisdom save (120ft) or Frightened for all creatures within 10ft of target"
                        ]
                    }
                }
            ],
            15: [
                {
                    "id": "gloom_stalker_shadowy_dodge",
                    "name": "Shadowy Dodge",
                    "summary": "Reaction: impose Disadvantage on an attack against you and teleport 30ft.",
                    "details": {
                        "action": "Reaction",
                        "trigger": "Creature makes an attack roll against you",
                        "effect": "Impose Disadvantage on the roll; teleport up to 30ft to an unoccupied space"
                    }
                }
            ]
        }
    },
    "hunter": {
        "id": "hunter",
        "name": "Hunter",
        "description": "Emulating the Hunter archetype means accepting your role as the bulwark between civilization and the terrors of the wilderness. As you walk the Hunter's path, you learn specialized techniques for fighting the threats you face, from raging ogres and hordes of orcs to towering giants and terrifying dragons.",
        "features": {
            3: [
                {
                    "id": "hunter_lore",
                    "name": "Hunter's Lore",
                    "summary": "While a creature is marked by your Hunter's Mark, you know its Immunities, Resistances, and Vulnerabilities.",
                    "details": {
                        "condition": "Target must be marked by Hunter's Mark",
                        "information": "Immunities, Resistances, and Vulnerabilities revealed"
                    }
                },
                {
                    "id": "hunter_prey",
                    "name": "Hunter's Prey",
                    "summary": "Choose Colossus Slayer (+1d8 dmg to wounded) or Horde Breaker (extra attack). Replace on Short/Long Rest.",
                    "details": {
                        "options": {
                            "colossus_slayer": "Extra 1d8 damage on weapon hit if target is missing HP (once per turn)",
                            "horde_breaker": "Once per turn: make an extra weapon attack against a different creature within 5ft of original target"
                        },
                        "special": "Can swap option on Short or Long Rest"
                    }
                }
            ],
            7: [
                {
                    "id": "hunter_defensive_tactics",
                    "name": "Defensive Tactics",
                    "summary": "Choose Escape the Horde (OAs have Disadvantange) or Multiattack Defense (AC bonus vs same attacker). Replace on Short/Long Rest.",
                    "details": {
                        "options": {
                            "escape_the_horde": "Opportunity Attacks have Disadvantage against you",
                            "multiattack_defense": "When hit, the attacker has Disadvantage on all other attacks against you this turn"
                        },
                        "special": "Can swap option on Short or Long Rest"
                    }
                }
            ],
            11: [
                {
                    "id": "hunter_superior_hunters_prey",
                    "name": "Superior Hunter's Prey",
                    "summary": "Once per turn, deal Hunter's Mark extra damage to a second creature within 30ft of the first damaged target.",
                    "details": {
                        "trigger": "Deal damage to a creature marked by Hunter's Mark",
                        "effect": "Deal that spell's extra damage to a different creature within 30ft"
                    }
                }
            ],
            15: [
                {
                    "id": "hunter_superior_hunters_defense",
                    "name": "Superior Hunter's Defense",
                    "summary": "Reaction: gain Resistance to an incoming damage type until the end of the turn.",
                    "details": {
                        "action": "Reaction",
                        "trigger": "Take damage",
                        "effect": "Gain Resistance to that damage type (and all instances of it) until the end of the current turn"
                    }
                }
            ]
        }
    }
}
