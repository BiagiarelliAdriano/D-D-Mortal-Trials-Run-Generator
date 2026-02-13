"""
Subclass definitions for the Druid class.
"""

DRUID_SUBCLASSES = {
    "land": {
        "id": "land",
        "name": "Circle of the Land",
        "description": "The Circle of the Land is made up of mystics and sages who safeguard ancient knowledge and rites through a vast oral tradition. These druids meet within sacred circles of elder trees or standing stones to whisper primal secrets in Druidic and commune with the spirits of nature.",
        "features": {
            3: [
                {
                    "id": "land_spells",
                    "name": "Circle Of The Land Spells",
                    "summary": "Choose a land type (Arid, Polar, Temperate, Tropical) after a Long Rest to gain specific prepared spells.",
                    "details": {
                        "arid": {
                            3: ["Blur", "Burning Hands", "Fire Bolt"],
                            5: ["Fireball"],
                            7: ["Blight"],
                            9: ["Wall of Stone"]
                        },
                        "polar": {
                            3: ["Fog Cloud", "Hold Person", "Ray Of Frost"],
                            5: ["Sleet Storm"],
                            7: ["Ice Storm"],
                            9: ["Cone Of Cold"]
                        },
                        "temperate": {
                            3: ["Misty Step", "Shocking Grasp", "Sleep"],
                            5: ["Lightning Bolt"],
                            7: ["Freedom Of Movement"],
                            9: ["Tree Stride"]
                        },
                        "tropical": {
                            3: ["Acid Splash", "Ray Of Sickness", "Web"],
                            5: ["Stinking Cloud"],
                            7: ["Polymorph"],
                            9: ["Insect Plague"]
                        }
                    }
                },
                {
                    "id": "land_aid",
                    "name": "Land's Aid",
                    "summary": "Magic Action: expend Wild Shape to deal 2d6 Necrotic damage and heal 2d6 HP in a 10ft radius (increases at Lvl 10 and 14).",
                    "details": {
                        "action": "Magic Action",
                        "cost": "One use of Wild Shape",
                        "range": "60ft",
                        "area": "10ft radius Sphere",
                        "damage": {
                            "default": "2d6 Necrotic",
                            "level_10": "3d6 Necrotic",
                            "level_14": "4d6 Necrotic",
                            "save": "Con save for half"
                        },
                        "healing": {
                            "default": "2d6",
                            "level_10": "3d6",
                            "level_14": "4d6"
                        }
                    }
                }
            ],
            6: [
                {
                    "id": "land_natural_recovery",
                    "name": "Natural Recovery",
                    "summary": "Cast one level 1+ Circle Spell for free per Long Rest; recover spell slots (half Druid level) on Short Rest.",
                    "details": {
                        "free_cast": "One Lvl 1+ spell from Circle Spells per Long Rest",
                        "slot_recovery": {
                            "combined_level": "Druid Level / 2 (round up)",
                            "max_slot_level": 5,
                            "recharge": "One per Long Rest (during Short Rest)"
                        }
                    }
                }
            ],
            10: [
                {
                    "id": "land_natures_ward",
                    "name": "Nature's Ward",
                    "summary": "Immunity to Poisoned; gain Resistance based on current land choice.",
                    "details": {
                        "immunities": ["Poisoned"],
                        "resistances": {
                            "arid": "Fire",
                            "polar": "Cold",
                            "temperate": "Lightning",
                            "tropical": "Poison"
                        }
                    }
                }
            ],
            14: [
                {
                    "id": "land_natures_sanctuary",
                    "name": "Nature's Sanctuary",
                    "summary": "Magic Action: expend Wild Shape to create a 15ft Cube providing Half Cover and your land Resistance to allies.",
                    "details": {
                        "action": "Magic Action",
                        "cost": "One use of Wild Shape",
                        "range": "120ft",
                        "area": "15ft Cube",
                        "duration": "1 minute",
                        "benefits": [
                            "Half Cover for self and allies",
                            "Allies gain current Nature's Ward resistance"
                        ],
                        "move": "Bonus Action to move Cube 60ft (must stay within 120ft)"
                    }
                }
            ]
        }
    },
    "moon": {
        "id": "moon",
        "name": "Circle of the Moon",
        "description": "Druids of the Circle of the Moon are fierce guardians of the wilds. Their order gathers under the full moon to share news of the world and to perform rites of passage. They are masters of the shifting form, using their lunar magic to bond deeply with the animal kingdom.",
        "features": {
            3: [
                {
                    "id": "moon_circle_forms",
                    "name": "Circle Forms",
                    "summary": "Assume Wild Shape forms with CR up to Druid Level / 3; gain extra AC and Temp HP.",
                    "details": {
                        "max_cr": "Druid Level / 3 (round down)",
                        "armor_class": "13 + Wisdom modifier (if higher than Beast's AC)",
                        "temporary_hp": "3 * Druid Level"
                    }
                },
                {
                    "id": "moon_circle_spells",
                    "name": "Circle Of The Moon Spells",
                    "summary": "Always prepared; castable while in Wild Shape.",
                    "details": {
                        "cast_while_wildshaped": True,
                        "spells": {
                            3: ["Cure Wounds", "Moonbeam", "Starry Wisp"],
                            5: ["Conjure Animals"],
                            7: ["Fount Of Moonlight"],
                            9: ["Mass Cure Wounds"]
                        }
                    }
                }
            ],
            6: [
                {
                    "id": "moon_improved_circle_forms",
                    "name": "Improved Circle Forms",
                    "summary": "Attacks in Wild Shape deal normal or Radiant damage; add Wisdom modifier to Con saves.",
                    "details": {
                        "damage_type_choice": ["Normal", "Radiant"],
                        "saving_throw_bonus": "Add Wisdom modifier to Constitution saves while transformed"
                    }
                }
            ],
            10: [
                {
                    "id": "moon_moonlight_step",
                    "name": "Moonlight Step",
                    "summary": "Bonus Action: teleport 30ft and gain Advantage on the next attack roll; uses equal Wisdom mod.",
                    "details": {
                        "action": "Bonus Action",
                        "range": "30ft",
                        "effect": "Teleport + Advantage on next attack roll this turn",
                        "uses": "Wisdom modifier (minimum 1)",
                        "recharge": "Long Rest",
                        "alternative_recharge": "Expend a Level 2+ spell slot for one use (no action)"
                    }
                }
            ],
            14: [
                {
                    "id": "moon_lunar_form",
                    "name": "Lunar Form",
                    "summary": "Extra 2d10 Radiant damage once per turn in form; teleport an ally with Moonlight Step.",
                    "details": {
                        "on_hit_damage": "2d10 Radiant (once per turn)",
                        "teleport_ally": "Move 1 willing creature within 10ft with you (to space within 10ft of destination)"
                    }
                }
            ]
        }
    }
}
