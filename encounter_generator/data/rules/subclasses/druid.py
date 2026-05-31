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
                    "description": "Whenever you finish a Long Rest, choose one type of land: arid, polar, temperate, or tropical. Consult the table below that corresponds to the chosen type; you have the spells listed for your Druid level and lower prepared. \n *-Arid Land-* \n Lv3: Blur, Burning Hands, Fire Bolt. \n Lv5: Fireball. \n Lv7: Blight. \n Lv9: Wall of Stone. \n *-Polar Land-* \n Lv3: Fog Cloud, Hold Person, Ray of Frost. \n Lv5: Sleet Storm. \n Lv7: Ice Storm. \n Lv9: Cone of Cold. \n *-Temperate Land-* \n Lv3: Misty Step, Shocking Grasp, Sleep. \n Lv5: Lightning Bolt. \n Lv7: Freedom of Movement. \n Lv9: Tree Stride. \n *-Tropical Land-* \n Lv3: Acid Splash, Ray of Sickness, Web. \n Lv5: Stinking Cloud. \n Lv7: Polymorph. \n Lv9: Insect Plague.",
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
                    "description": "As a Magic action, you can expend a use of your Wild Shape and choose a point within 60 feet of yourself. Vitality-giving flowers and life-draining thorns appear for a moment in a 10-foot-radius Sphere centered on that point. Each creature of your choice in the Sphere must make a Constitution saving throw against your spell save DC, taking 2d6 Necrotic damage on a failed save or half as much damage on a successful one. One creature of your choice in that area regains 2d6 Hit Points. \n The damage and healing increase by 1d6 when you reach Druid levels 10 (3d6) and 14 (4d6).",
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
                    "description": "You can cast one of the level 1+ spells that you have prepared from your Circle Spells feature without expending a spell slot, and you must finish a Long Rest before you do so again. \n In addition, when you finish a Short Rest, you can choose expended spell slots to recover. The spell slots can have a combined level that is equal to or less than half your Druid level (round up), and none of them can be level 6+. For example, if you're a level 6 Druid, you can recover up to three levels' worth of spell slots. You can recover a level 3 spell slot, a level 2 and a level 1 spell slot, or three level 1 spell slots. Once you recover spell slots with this feature, you can't do so again until you finish a Long Rest.",
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
                    "description": "You are immune to the Poisoned condition, and you have Resistance to a damage type associated with your current land choice in the Circle Spells feature, as shown in the Nature's Ward table. \n Arid = Fire. \n Polar = Cold. \n Temperate = Lightning. \n Tropical = Poison.",
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
                    "description": "As a Magic action, you can expend a use of your Wild Shape and cause spectral trees and vines to appear in a 15-foot Cube on the ground within 120 feet of yourself. They last there for 1 minute or until you have the Incapacitated condition or die. You and your allies have Half Cover while in that area, and your allies gain the current Resistance of your Nature's Ward while there. \n As a Bonus Action, you can move the Cube up to 60 feet to ground within 120 feet of yourself.",
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
                    "description": "When you reach a Druid level specified in the Circle of the Moon Spells table, you thereafter always have the listed spells prepared. \n In addition, you can cast the spells from this feature while you're in a Wild Shape form. \n Lv3: Cure Wounds, Moonbeam, Starry Wisp. \n Lv5: Conjure Animals. \n Lv7: Fount of Moonlight. \n Lv9: Mass Cure Wounds.",
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
                    "description": "You can channel lunar magic when you assume a Wild Shape form, granting you the benefits below. \n Challenge Rating. The maximum Challenge Rating for the form equals your Druid level divided by 3 (round down). \n Armor Class. Until you leave the form, your AC equals 13 plus your Wisdom modifier if that total is higher than the Beast's AC. \n Temporary Hit Points. You gain a number of Temporary Hit Points equal to three times your Druid level.",
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
                    "description": "While in a Wild Shape form, you gain the following benefits. \n Lunar Radiance. Each of your attacks in a Wild Shape form can deal its normal damage type or Radiant damage. You make this choice each time you hit with those attacks. \n Increased Toughness. You can add your Wisdom modifier to your Constitution saving throws.",
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
                    "description": "You magically transport yourself, reappearing amid a burst of moonlight. As a Bonus Action, you teleport up to 30 feet to an unoccupied space you can see, and you have Advantage on the next attack roll you make before the end of this turn. \n You can use this feature a number of times equal to your Wisdom modifier (minimum of once), and you regain all expended uses when you finish a Long Rest. You can also regain uses by expending a level 2+ spell slot for each use you want to restore (no action required).",
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
                    "description": "The power of the moon suffuses you, granting you the following benefits. \n Improved Lunar Radiance. Once per turn, you can deal an extra 2d10 Radiant damage to a target you hit with a Wild Shape form's attack. \n Shared Moonlight. Whenever you use Moonlight Step, you can also teleport one willing creature. That creature must be within 10 feet of you, and you teleport it to an unoccupied space you can see within 10 feet of your destination space.",
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
                    "description": "When you reach a Druid level specified in the Circle of the Sea Spells table, you thereafter always have the listed spells prepared. \n Lv3: Fog Cloud, Gust of Wind, Ray of Frost, Shatter, Thunderwave. \n Lv5: Lightning Bolt, Water Breathing. \n Lv7: Control Water, Ice Storm. \n Lv9: Conjure Elemental, Hold Monster.",
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
                    "description": "As a Bonus Action, you can expend a use of your Wild Shape to manifest a 5-foot Emanation that takes the form of ocean spray that surrounds you for 10 minutes. It ends early if you dismiss it (no action required), manifest it again, or have the Incapacitated condition. \n When you manifest the Emanation and as a Bonus Action on your subsequent turns, you can choose another creature you can see in the Emanation. The target must succeed on a Constitution saving throw against your spell save DC or take Cold damage and, if the creature is Large or smaller, be pushed up to 15 feet away from you. To determine this damage, roll a number of d6s equal to your Wisdom modifier (minimum of one die).",
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
                    "description": "The size of the Emanation created by your Wrath of the Sea increases to 10 feet. In addition, you gain a Swim Speed equal to your Speed.",
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
                    "description": "Your Wrath of the Sea confers two more benefits while active, as detailed below. Flight. You gain a Fly Speed equal to your Speed. Resistance. You have Resistance to Cold, Lightning, and Thunder damage.",
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
                    "description": "Instead of manifesting the Emanation of Wrath of the Sea around yourself, you can manifest it around one willing creature within 60 feet of yourself. That creature gains all the benefits of the Emanation and uses your spell save DC and Wisdom modifier for it. \n In addition, you can manifest the Emanation around both the other creature and yourself if you expend two uses of your Wild Shape instead of one when manifesting it.",
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
                    "description": "You've created a star chart as part of your heavenly studies. It is a Tiny object, and you can use it as a Spellcasting Focus for your Druid spells. You determine its form by rolling on the Star Map table or by choosing one. \n While holding the map, you have the Guidance and Guiding Bolt spells prepared, and you can cast Guiding Bolt without expending a spell slot. You can cast it in that way a number of times equal to your Wisdom modifier (minimum of once), and you regain all expended uses when you finish a Long Rest. \n If you lose the map, you can perform a 1-hour ceremony to magically create a replacement. This ceremony can be performed during a Short or Long Rest, and it destroys the previous map. \n *1d6:* \n 1 = A scroll bearing depictions of constellations. \n 2 = A stone tablet with fine holes drilled through it. \n 3 = An owlbear hide tooled with stellar symbols. \n 4 = A collection of maps bound in an ebony cover. \n 5 = A crystal engraved with starry patterns. \n 6 = A glass disk etched with constellations.",
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
                    "description": "As a Bonus Action, you can expend a use of your Wild Shape feature to take on a starry form rather than shape-shifting. \n While in your starry form, you retain your game statistics, but your body becomes luminous, your joints glimmer like stars, and glowing lines connect them as on a star chart. This form sheds Bright Light in a 10-foot radius and Dim Light for an additional 10 feet. The form lasts for 10 minutes. It ends early if you dismiss it (no action required), have the Incapacitated condition, or use this feature again. \n Whenever you assume your starry form, choose which of the following constellations glimmers on your body; your choice gives you certain benefits while in the form. \n *-Archer-* A constellation of an archer appears on you. When you activate this form and as a Bonus Action on your subsequent turns while it lasts, you can make a ranged spell attack, hurling a luminous arrow that targets one creature within 60 feet of yourself. On a hit, the attack deals Radiant damage equal to 1d8 plus your Wisdom modifier. \n *-Chalice-* A constellation of a life-giving goblet appears on you. Whenever you cast a spell using a spell slot that restores Hit Points to a creature, you or another creature within 30 feet of you can regain Hit Points equal to 1d8 plus your Wisdom modifier. \n *-Dragon-* A constellation of a wise dragon appears on you. When you make an Intelligence or a Wisdom check or a Constitution saving throw to maintain Concentration, you can treat a roll of 9 or lower on the d20 as a 10.",
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
                    "description": "Whenever you finish a Long Rest, you can consult your Star Map for omens and roll a die. Until you finish your next Long Rest, you gain access to a special Reaction based on whether you rolled an even or an odd number on the die: \n Weal (even). Whenever a creature you can see within 30 feet of you is about to make a D20 Test, you can take a Reaction to roll 1d6 and add the number rolled to the total. \n Woe (odd). Whenever a creature you can see within 30 feet of you is about to make a D20 Test, you can take a Reaction to roll 1d6 and subtract the number rolled from the total. \n You can use this Reaction a number of times equal to your Wisdom modifier (minimum of once), and you regain all expended uses when you finish a Long Rest.",
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
                    "description": "The constellations of your Starry Form improve. The 1d8 of the Archer and the Chalice becomes 2d8, and while the Dragon is active, you have a Fly Speed of 20 feet and can hover. Moreover, at the start of each of your turns while in your Starry Form, you can change which constellation glimmers on your body.",
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
                    "description": "While in your Starry Form, you become partially incorporeal, giving you Resistance to Bludgeoning, Piercing, and Slashing damage.",
                    "details": {
                        "effect": "Gain Resistance to physical damage (B/P/S) while transformed"
                    }
                }
            ]
        }
    }
}
