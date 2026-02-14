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
    },
    "sea": {
        "id": "sea",
        "name": "Circle of the Sea",
        "description": "Druids of the Circle of the Sea draw their power from the depths of the ocean and the fury of the storm. They are as fluid as the tides and as relentless as a hurricane, capable of manifesting the crushing pressure and freezing cold of the abyss to sweep their enemies away.",
        "features": {
            3: [
                {
                    "id": "sea_circle_spells",
                    "name": "Circle Of The Sea Spells",
                    "summary": "Always prepared spells focused on water, ice, and storms.",
                    "details": {
                        "spells": {
                            3: ["Fog Cloud", "Gust of Wind", "Ray Of Frost", "Shatter", "Thunderwave"],
                            5: ["Lightning Bolt", "Water Breathing"],
                            7: ["Control Water", "Ice Storm"],
                            9: ["Conjure Elemental", "Hold Monster"]
                        }
                    }
                },
                {
                    "id": "sea_wrath_of_the_sea",
                    "name": "Wrath Of The Sea",
                    "summary": "Bonus Action: expend Wild Shape to create a 5ft ocean spray Emanation (10 min). Use Bonus Action to deal Cold damage and push creatures 15ft.",
                    "details": {
                        "action": "Bonus Action",
                        "cost": "One use of Wild Shape",
                        "duration": "10 minutes",
                        "area": "5ft Emanation (increases at Lvl 6)",
                        "effect": {
                            "trigger": "When manifested and as a subsequent Bonus Action",
                            "damage": "Wisdom modifier d6 Cold damage",
                            "forced_movement": "Push Large or smaller creatures up to 15ft away",
                            "save": "Con save vs spell save DC"
                        }
                    }
                }
            ],
            6: [
                {
                    "id": "sea_aquatic_affinity",
                    "name": "Aquatic Affinity",
                    "summary": "Wrath of the Sea Emanation grows to 10ft; gain Swim Speed equal to your Speed.",
                    "details": {
                        "emanation_size": "10ft",
                        "swim_speed": "Equal to walking Speed"
                    }
                }
            ],
            10: [
                {
                    "id": "sea_stormborn",
                    "name": "Stormborn",
                    "summary": "While Wrath of the Sea is active, gain Fly Speed and Resistance to Cold, Lightning, and Thunder.",
                    "details": {
                        "fly_speed": "Equal to walking Speed",
                        "resistances": ["Cold", "Lightning", "Thunder"]
                    }
                }
            ],
            14: [
                {
                    "id": "sea_oceanic_gift",
                    "name": "Oceanic Gift",
                    "summary": "Manifest Wrath of the Sea around others (60ft); expend two Wild Shapes to manifest it around both self and an ally.",
                    "details": {
                        "range": "60ft",
                        "effect": "Manifest Emanation around a willing creature",
                        "double_manifest": {
                            "cost": "Two uses of Wild Shape",
                            "targets": ["Self", "Willing creature within 60ft"]
                        }
                    }
                }
            ]
        }
    },
    "stars": {
        "id": "stars",
        "name": "Circle of the Stars",
        "description": "Druids of the Circle of the Stars have tracked the movements of celestial bodies and the patterns of the heavens for generations. They draw upon the starlight of the cosmos to empower their magic, using ancient star charts to navigate the mysteries of the multiverse.",
        "features": {
            3: [
                {
                    "id": "stars_star_map",
                    "name": "Star Map",
                    "summary": "Gain a Star Map Tiny object as a Focus; always have Guidance and Guiding Bolt prepared. Cast Guiding Bolt for free (Wisdom mod/day).",
                    "details": {
                        "object": "Tiny Star Map",
                        "form_options": [
                            "Scroll with constellations",
                            "Stone tablet with holes",
                            "Owlbear hide with stellar symbols",
                            "Maps bound in ebony",
                            "Crystal engraved with patterns",
                            "Glass disk etched with constellations"
                        ],
                        "granted_spells": ["Guidance", "Guiding Bolt"],
                        "free_casts": {
                            "spell": "Guiding Bolt",
                            "uses": "Wisdom modifier (minimum 1)",
                            "recharge": "Long Rest"
                        },
                        "replacement": "1 hour ceremony during Rest"
                    }
                },
                {
                    "id": "stars_starry_form",
                    "name": "Starry Form",
                    "summary": "Bonus Action: expend Wild Shape to take a luminous form for 10 min. Choose a constellation (Archer, Chalice, or Dragon) for unique benefits.",
                    "details": {
                        "action": "Bonus Action",
                        "cost": "One use of Wild Shape",
                        "duration": "10 minutes",
                        "light": "10ft Bright, 10ft Dim",
                        "constellations": {
                            "archer": "Bonus Action: make a ranged spell attack (60ft) for 1d8 + Wisdom mod Radiant damage.",
                            "chalice": "When casting a healing spell with a slot: you or creature within 30ft regain 1d8 + Wisdom mod HP.",
                            "dragon": "Intelligence/Wisdom checks and Concentration saves: treat 9 or lower as 10."
                        }
                    }
                }
            ],
            6: [
                {
                    "id": "stars_cosmic_omen",
                    "name": "Cosmic Omen",
                    "summary": "Roll d20 after Long Rest. Use Reaction to add (Weal - even) or subtract (Woe - odd) 1d6 from a creature's d20 Test within 30ft.",
                    "details": {
                        "trigger": "Creature within 30ft makes a d20 Test",
                        "action": "Reaction",
                        "uses": "Wisdom modifier (minimum 1)",
                        "recharge": "Long Rest",
                        "effects": {
                            "weal_even": "Add 1d6 to the total",
                            "woe_odd": "Subtract 1d6 from the total"
                        }
                    }
                }
            ],
            10: [
                {
                    "id": "stars_twinkling_constellation",
                    "name": "Twinkling Constellation",
                    "summary": "Starry Form improves: Archer/Chalice use 2d8; Dragon gains Fly speed (20ft, hover). Change constellation at start of turn.",
                    "details": {
                        "archer_upgrade": "2d8 + Wisdom mod",
                        "chalice_upgrade": "2d8 + Wisdom mod",
                        "dragon_upgrade": "Gain 20ft Fly Speed (hover)",
                        "flexibility": "Can change current constellation at start of turn while in form"
                    }
                }
            ],
            14: [
                {
                    "id": "stars_full_of_stars",
                    "name": "Full Of Stars",
                    "summary": "While in Starry Form, gain Resistance to Bludgeoning, Piercing, and Slashing damage.",
                    "details": {
                        "effect": "Gain Resistance to physical damage (B/P/S) while transformed"
                    }
                }
            ]
        }
    }
}
