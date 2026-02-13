"""
Subclass definitions for the Barbarian class.
"""

BARBARIAN_SUBCLASSES = {
    "berserker": {
        "id": "berserker",
        "name": "Path Of The Berserker",
        "description": "For some barbarians, rage is a means to an end—that end being violence. The Path of the Berserker is a path of untamed fury, slick with blood. As you enter the berserker's rage, you thrill in the chaos of battle, heedless of your own health or well-being.",
        "features": {
            3: [
                {
                    "id": "berserker_frenzy",
                    "name": "Frenzy",
                    "summary": "Deal extra d6s of damage (equal to Rage Bonus) on your first Reckless Attack hit each turn.",
                    "details": {
                        "damage_die": "d6",
                        "die_count": "Rage Bonus",
                        "restriction": "First hit on turn, must use Reckless Attack while Raging"
                    }
                }
            ],
            6: [
                {
                    "id": "berserker_mindless_rage",
                    "name": "Mindless Rage",
                    "summary": "Immunity to Charmed and Frightened conditions while Raging; ends existing effects upon entering Rage."
                }
            ],
            10: [
                {
                    "id": "berserker_retaliation",
                    "name": "Retaliation",
                    "summary": "Use a Reaction to make a melee attack against a creature within 5ft that deals damage to you."
                }
            ],
            14: [
                {
                    "id": "berserker_intimidating_presence",
                    "name": "Intimidating Presence",
                    "summary": "Bonus Action to Frighten creatures in a 30ft Emanation (WIS save); can recharge by expending a Rage use.",
                    "details": {
                        "action": "Bonus Action",
                        "area": "30ft Emanation",
                        "save_dc": "8 + STR mod + Proficiency Bonus",
                        "recharge": "Long Rest or expend one Rage use"
                    }
                }
            ]
        }
    },
    "wild_heart": {
        "id": "wild_heart",
        "name": "Path Of The Wild Heart",
        "description": "The Path of the Wild Heart is a journey that brings a barbarian into spiritual kinship with the natural world. Your rage is not just fury; it is a primal connection to the animal spirits that guide and protect you.",
        "features": {
            3: [
                {
                    "id": "wild_heart_animal_speaker",
                    "name": "Animal Speaker",
                    "summary": "Cast Beast Sense and Speak with Animals as Rituals using Wisdom.",
                    "details": {
                        "spells": ["Beast Sense", "Speak with Animals"],
                        "casting_mode": "Ritual only",
                        "ability": "Wisdom"
                    }
                },
                {
                    "id": "wild_heart_rage_of_the_wilds",
                    "name": "Rage of the Wilds",
                    "summary": "Choose an animal spirit benefit whenever you activate your Rage.",
                    "details": {
                        "options": {
                            "Bear": "Resistance to all damage types except Force, Necrotic, Psychic, and Radiant.",
                            "Eagle": "Dash and Disengage as part of the Bonus Action used to Rage; can take both as a Bonus Action while Raging.",
                            "Wolf": "Allies have Advantage on attack rolls against enemies within 5ft of you."
                        }
                    }
                }
            ],
            6: [
                {
                    "id": "wild_heart_aspect_of_the_wilds",
                    "name": "Aspect of the Wilds",
                    "summary": "Gain a permanent animal aspect, swappable on a Long Rest.",
                    "details": {
                        "options": {
                            "Owl": "Gain 60ft Darkvision (or +60ft if you already have it).",
                            "Panther": "Gain a Climb Speed equal to your Speed.",
                            "Salmon": "Gain a Swim Speed equal to your Speed."
                        },
                        "recharge": "Long Rest (to swap)"
                    }
                }
            ],
            10: [
                {
                    "id": "wild_heart_nature_speaker",
                    "name": "Nature Speaker",
                    "summary": "Cast Commune with Nature as a Ritual using Wisdom.",
                    "details": {
                        "spells": ["Commune with Nature"],
                        "casting_mode": "Ritual only",
                        "ability": "Wisdom"
                    }
                }
            ],
            14: [
                {
                    "id": "wild_heart_power_of_the_wilds",
                    "name": "Power of the Wilds",
                    "summary": "Gain an advanced animal spirit benefit whenever you activate your Rage.",
                    "details": {
                        "options": {
                            "Falcon": "Gain a Fly Speed equal to your Speed while unarmored.",
                            "Lion": "Enemies within 5ft have Disadvantage vs targets other than you or another Wild Heart Barbarian.",
                            "Ram": "Melee hits can knock Large or smaller creatures Prone."
                        }
                    }
                }
            ]
        }
    },
    "world_tree": {
        "id": "world_tree",
        "name": "Path Of The World Tree",
        "description": "Barbarians who follow the Path of the World Tree draw their power from the cosmic ash that connects the planes. Your rage is a manifesting of the tree's eternal vitality, allowing you to shield allies with spectral roots and traverse the multiverse through its ethereal branches.",
        "features": {
            3: [
                {
                    "id": "world_tree_vitality",
                    "name": "Vitality Of The Tree",
                    "summary": "Gain Temp HP on Rage; grant Temp HP to allies within 10ft at the start of each turn.",
                    "details": {
                        "on_rage": "Gain Temp HP equal to Barbarian level",
                        "turn_start": {
                            "target": "Another creature within 10ft",
                            "amount": "Rage Damage bonus in d6s"
                        },
                        "restriction": "Temp HP vanishes when Rage ends"
                    }
                }
            ],
            6: [
                {
                    "id": "world_tree_branches",
                    "name": "Branches Of The Tree",
                    "summary": "Reaction to teleport a creature starting its turn within 30ft to a space within 5ft of you (STR save).",
                    "details": {
                        "action": "Reaction",
                        "range": "30ft",
                        "save_dc": "8 + STR mod + Proficiency Bonus",
                        "effect": "Teleport to unoccupied space within 5ft of you; can reduce speed to 0"
                    }
                }
            ],
            10: [
                {
                    "id": "world_tree_battering_roots",
                    "name": "Battering Roots",
                    "summary": "+10ft reach with Heavy/Versatile weapons; can use Push/Topple mastery in addition to another.",
                    "details": {
                        "reach_bonus": "+10ft (Heavy/Versatile weapons)",
                        "mastery_bonus": "Activate Push or Topple in addition to another property"
                    }
                }
            ],
            14: [
                {
                    "id": "world_tree_travel",
                    "name": "Travel Along The Tree",
                    "summary": "Teleport up to 60ft as a Bonus Action while Raging; once per Rage, teleport 150ft with up to 6 allies.",
                    "details": {
                        "action": "Bonus Action",
                        "standard_range": "60ft",
                        "extended_range": {
                            "uses": "Once per Rage",
                            "distance": "150ft",
                            "allies": "Up to 6 willing creatures within 10ft"
                        }
                    }
                }
            ]
        }
    },
    "zealot": {
        "id": "zealot",
        "name": "Path Of The Zealot",
        "description": "Some barbarians are chosen by gods to serve as divine instruments of destruction. The Path of the Zealot is a burning flame of faith that fuels your rage, granting you divine power to strike down foes and the resilience to transcend death itself.",
        "features": {
            3: [
                {
                    "id": "zealot_divine_fury",
                    "name": "Divine Fury",
                    "summary": "First hit while Raging deals extra 1d6 + half level damage (Radiant/Necrotic).",
                    "details": {
                        "damage_die": "1d6",
                        "modifier": "Barbarian Level / 2 (round down)",
                        "damage_types": ["Radiant", "Necrotic"],
                        "restriction": "Once per turn, while Raging"
                    }
                },
                {
                    "id": "zealot_warrior_of_the_gods",
                    "name": "Warrior Of The Gods",
                    "summary": "Pool of d12s to heal yourself as a Bonus Action.",
                    "details": {
                        "heal_die": "d12",
                        "pool_size": {
                            "type": "level-based",
                            "scaling": {
                                "3-5": 4,
                                "6-11": 5,
                                "12-16": 6,
                                "17-20": 7
                            }
                        },
                        "recharge": "Long Rest"
                    }
                }
            ],
            6: [
                {
                    "id": "zealot_fanatical_focus",
                    "name": "Fanatical Focus",
                    "summary": "Once per Rage, reroll a failed save with a bonus equal to your Rage Bonus.",
                    "details": {
                        "uses": "Once per active Rage",
                        "bonus": "Rage Damage bonus"
                    }
                }
            ],
            10: [
                {
                    "id": "zealot_zealous_presence",
                    "name": "Zealous Presence",
                    "summary": "Bonus Action to grant Advantage on attacks/saves to 10 allies within 60ft until next turn.",
                    "details": {
                        "action": "Bonus Action",
                        "range": "60ft",
                        "targets": "Up to 10 other creatures",
                        "recharge": "Long Rest or expend one Rage use"
                    }
                }
            ],
            14: [
                {
                    "id": "zealot_rage_of_the_gods",
                    "name": "Rage Of The Gods",
                    "summary": "Assume a divine warrior form (Fly/Hover, resistances); expend Rage as Reaction to prevent 0 HP.",
                    "details": {
                        "form_benefits": {
                            "speed": "Fly Speed (equal to Speed), can Hover",
                            "resistance": ["Necrotic", "Psychic", "Radiant"],
                            "duration": "1 minute or until 0 HP"
                        },
                        "death_prevention": {
                            "action": "Reaction",
                            "range": "30ft",
                            "cost": "Expend one Rage use",
                            "effect": "Target HP becomes equal to your Barbarian level instead of 0"
                        },
                        "recharge": "Long Rest"
                    }
                }
            ]
        }
    }
}
