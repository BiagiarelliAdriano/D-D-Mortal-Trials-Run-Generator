"""
Subclass definitions for the Wizard class.
"""

WIZARD_SUBCLASSES = {
    "abjurer": {
        "id": "abjurer",
        "name": "Abjurer",
        "description": "As an Abjurer, you specialize in magic that blocks, banishes, and protects. You are a master of defensive wards and counter-magic, weaving protective barriers that can absorb physical blows and magical energy alike. Your presence on the battlefield provides a pillar of security for your allies, as you negate the most dangerous of enemy spells.",
        "features": {
            3: [
                {
                    "id": "abjurer_abjuration_savant",
                    "name": "Abjuration Savant",
                    "summary": "Free Abjuration spells for your spellbook (two at lvl 3, plus one per new slot level).",
                    "description": "Choose two Wizard spells from the Abjuration school, each of which must be no higher than level 2, and add them to your spellbook for free. In addition, whenever you gain access to a new level of spell slots in this class, you can add one Wizard spell from the Abjuration school to your spellbook for free. The chosen spell must be of a level for which you have spell slots.",
                    "details": {
                        "initial_spells": "Choose two Abjuration spells (lvl 0-2) for your spellbook",
                        "progression_spells": "Add one Abjuration spell for free whenever you gain access to a new level of Wizard spell slots"
                    }
                },
                {
                    "id": "abjurer_arcane_ward",
                    "name": "Arcane Ward",
                    "summary": "Create a protective ward when casting Abjuration spells that absorbs damage.",
                    "description": "You can weave magic around yourself for protection. When you cast an Abjuration spell with a spell slot, you can simultaneously use a strand of the spell's magic to create a magical ward on yourself that lasts until you finish a Long Rest. The ward has a Hit Point maximum equal to twice your Wizard level plus your Intelligence modifier. Whenever you take damage, the ward takes the damage instead, and if you have any Resistances or Vulnerabilities, apply them before reducing the ward's Hit Points. If the damage reduces the ward to 0 Hit Points, you take any remaining damage. While the ward has 0 Hit Points, it can't absorb damage, but its magic remains. \n Whenever you cast an Abjuration spell with a spell slot, the ward regains a number of Hit Points equal to twice the level of the spell slot. Alternatively, as a Bonus Action, you can expend a spell slot, and the ward regains a number of Hit Points equal to twice the level of the spell slot expended. Once you create the ward, you can't create it again until you finish a Long Rest.",
                    "details": {
                        "hp_max": "Twice your Wizard level + Intelligence modifier",
                        "activation": "Cast an Abjuration spell with a spell slot",
                        "effect": "Ward takes damage before you; apply resistances/vulnerabilities first",
                        "recharge": {
                            "passive": "Cast an Abjuration spell with a slot: regain 2x slot level HP",
                            "active": "Bonus Action: Expend a spell slot to regain 2x slot level HP"
                        },
                        "duration": "Until Long Rest"
                    }
                }
            ],
            6: [
                {
                    "id": "abjurer_projected_ward",
                    "name": "Projected Ward",
                    "summary": "Reaction: Use your Arcane Ward to absorb damage for a creature within 30ft.",
                    "description": "When a creature that you can see within 30 feet of yourself takes damage, you can take a Reaction to cause your Arcane Ward to absorb that damage. If this damage reduces the ward to 0 Hit Points, the warded creature takes any remaining damage. If that creature has any Resistances or Vulnerabilities, apply them before reducing the ward's Hit Points.",
                    "details": {
                        "action": "Reaction",
                        "range": "30ft",
                        "effect": "Your Arcane Ward takes the damage for the target creature"
                    }
                }
            ],
            10: [
                {
                    "id": "abjurer_spell_breaker",
                    "name": "Spell Breaker",
                    "summary": "Counterspell/Dispel Magic are always prepared. Dispel Magic as Bonus Action. Failed attempts don't expend slots.",
                    "description": "You always have the Counterspell and Dispel Magic spells prepared. In addition, you can cast Dispel Magic as a Bonus Action, and you can add your Proficiency Bonus to its ability check. When you cast either spell with a spell slot, that slot isn't expended if the spell fails to stop a spell.",
                    "details": {
                        "spells_prepared": ["Counterspell", "Dispel Magic"],
                        "benefit_1": "Cast Dispel Magic as a Bonus Action",
                        "benefit_2": "Add Proficiency Bonus to Dispel Magic ability checks",
                        "benefit_3": "If Counterspell or Dispel Magic fails to stop a spell, the spell slot isn't expended"
                    }
                }
            ],
            14: [
                {
                    "id": "abjurer_spell_resistance",
                    "name": "Spell Resistance",
                    "summary": "Advantage on saves vs spells; Resistance to damage from spells.",
                    "description": "You have Advantage on saving throws against spells, and you have Resistance to the damage of spells.",
                    "details": {
                        "advantage": "Saving throws against spells",
                        "resistance": "Damage from spells"
                    }
                }
            ]
        }
    },
    "diviner": {
        "id": "diviner",
        "name": "Diviner",
        "description": "As a Diviner, you strive to part the veils of space, time, and opportunity so that you can see clearly. You work to master spells of discernment, remote viewing, supernatural knowing, and foresight. Your visions of the future allow you to substitute your own foretelling rolls for the whims of fate, ensuring that you and your allies are always one step ahead.",
        "features": {
            3: [
                {
                    "id": "diviner_divination_savant",
                    "name": "Divination Savant",
                    "summary": "Free Divination spells for your spellbook (two at lvl 3, plus one per new slot level).",
                    "description": "Choose two Wizard spells from the Divination school, each of which must be no higher than level 2, and add them to your spellbook for free. In addition, whenever you gain access to a new level of spell slots in this class, you can add one Wizard spell from the Divination school to your spellbook for free. The chosen spell must be of a level for which you have spell slots.",
                    "details": {
                        "initial_spells": "Choose two Divination spells (lvl 0-2) for your spellbook",
                        "progression_spells": "Add one Divination spell for free whenever you gain access to a new level of Wizard spell slots"
                    }
                },
                {
                    "id": "diviner_portent",
                    "name": "Portent",
                    "summary": "Record two d20 rolls after a Long Rest to replace any d20 tests you or others make.",
                    "description": "Glimpses of the future begin to press on your awareness. Whenever you finish a Long Rest, roll two d20s and record the numbers rolled. You can replace any D20 Test made by you or a creature that you can see with one of these foretelling rolls. You must choose to do so before the roll, and you can replace a roll in this way only once per turn. Each foretelling roll can be used only once. When you finish a Long Rest, you lose any unused foretelling rolls.",
                    "details": {
                        "activation": "Finish a Long Rest",
                        "effect": "Roll two d20s and record the numbers. Replace any d20 test within 60ft with one of these rolls.",
                        "limit": "Must choose to replace before the roll; once per turn per foretelling roll",
                        "duration": "Unused rolls are lost at the end of your next Long Rest"
                    }
                }
            ],
            6: [
                {
                    "id": "diviner_expert_divination",
                    "name": "Expert Divination",
                    "summary": "Regain a lower-level spell slot when you cast a Divination spell of level 2 or higher.",
                    "description": "Casting Divination spells comes so easily to you that it expends only a fraction of your spellcasting efforts. When you cast a Divination spell using a level 2+ spell slot, you regain one expended spell slot. The slot you regain must be of a level lower than the slot you expended and can't be higher than level 5.",
                    "details": {
                        "trigger": "Cast a Divination spell (lvl 2+)",
                        "benefit": "Regain one expended spell slot of a lower level (max lvl 5)"
                    }
                }
            ],
            10: [
                {
                    "id": "diviner_the_third_eye",
                    "name": "The Third Eye",
                    "summary": "Bonus Action: Gain Darkvision, language comprehension, or See Invisibility until your next rest.",
                    "description": "You can increase your powers of perception. As a Bonus Action, choose one of the following benefits, which lasts until you start a Short or Long Rest. You can't use this feature again until you finish a Short or Long Rest. \n *-Darkvision-* You gain Darkvision with a range of 120 feet. \n *-Greater Comprehension-* You can read any language. \n *-See Invisibility-* You can cast See Invisibility without expending a spell slot.",
                    "details": {
                        "action": "Bonus Action",
                        "options": [
                            "Darkvision (120ft)",
                            "Read any language",
                            "Cast See Invisibility without a spell slot"
                        ],
                        "duration": "Until you start a Short or Long Rest",
                        "recharge": "Short or Long Rest"
                    }
                }
            ],
            14: [
                {
                    "id": "diviner_greater_portent",
                    "name": "Greater Portent",
                    "summary": "Your Portent feature now grants three d20 rolls instead of two.",
                    "description": "The visions in your dreams intensify and paint a more accurate picture in your mind of what is to come. Roll three d20s for your Portent feature rather than two.",
                    "details": {
                        "benefit": "Roll three d20s for higher Portent feature instead of two"
                    }
                }
            ]
        }
    },
    "evoker": {
        "id": "evoker",
        "name": "Evoker",
        "description": "As an Evoker, you focus your study on magic that creates powerful elemental effects such as bitter cold, searing flame, rolling thunder, crackling lightning, and burning acid. You specialize in weaving raw energy into destructive spells, but you also master the art of shaping those effects to protect your allies from the brunt of your own magical onslaught.",
        "features": {
            3: [
                {
                    "id": "evoker_evocation_savant",
                    "name": "Evocation Savant",
                    "summary": "Free Evocation spells for your spellbook (two at lvl 3, plus one per new slot level).",
                    "description": "Choose two Wizard spells from the Evocation school, each of which must be no higher than level 2, and add them to your spellbook for free. In addition, whenever you gain access to a new level of spell slots in this class, you can add one Wizard spell from the Evocation school to your spellbook for free. The chosen spell must be of a level for which you have spell slots.",
                    "details": {
                        "initial_spells": "Choose two Evocation spells (lvl 0-2) for your spellbook",
                        "progression_spells": "Add one Evocation spell for free whenever you gain access to a new level of Wizard spell slots"
                    }
                },
                {
                    "id": "evoker_potent_cantrip",
                    "name": "Potent Cantrip",
                    "summary": "Damaging cantrips deal half damage on a miss or successful save.",
                    "description": "Your damaging cantrips affect even creatures that avoid the brunt of the effect. When you cast a cantrip at a creature and you miss with the attack roll or the target succeeds on a saving throw against the cantrip, the target takes half the cantrip's damage (if any) but suffers no additional effect from the cantrip.",
                    "details": {
                        "effect": "Half damage (if any) on missed attack or successful saving throw; no secondary effects apply"
                    }
                }
            ],
            6: [
                {
                    "id": "evoker_sculpt_spells",
                    "name": "Sculpt Spells",
                    "summary": "Choose allies to automatically succeed on saves and take no damage from your Evocation spells.",
                    "description": "You can create pockets of relative safety within the effects of your evocations. When you cast an Evocation spell that affects other creatures that you can see, you can choose a number of them equal to 1 plus the spell's level. The chosen creatures automatically succeed on their saving throws against the spell, and they take no damage if they would normally take half damage on a successful save.",
                    "details": {
                        "targets": "1 + spell level creatures you can see",
                        "effect": "Automatically succeed on saving throws; take no damage instead of half damage"
                    }
                }
            ],
            10: [
                {
                    "id": "evoker_empowered_evocation",
                    "name": "Empowered Evocation",
                    "summary": "Add your Intelligence modifier to one damage roll of any Wizard Evocation spell.",
                    "description": "Whenever you cast a Wizard spell from the Evocation school, you can add your Intelligence modifier to one damage roll of that spell.",
                    "details": {
                        "effect": "Add Intelligence modifier to one damage roll of an Evocation spell"
                    }
                }
            ],
            14: [
                {
                    "id": "evoker_overchannel",
                    "name": "Overchannel",
                    "summary": "Deal maximum damage with a damage-dealing spell of levels 1-5.",
                    "description": "You can increase the power of your spells. When you cast a Wizard spell with a spell slot of levels 1–5 that deals damage, you can deal maximum damage with that spell on the turn you cast it. The first time you do so, you suffer no adverse effect. If you use this feature again before you finish a Long Rest, you take 2d12 Necrotic damage for each level of the spell slot immediately after you cast it. This damage ignores Resistance and Immunity. Each time you use this feature again before finishing a Long Rest, the Necrotic damage per spell level increases by 1d12.",
                    "details": {
                        "effect": "Deal maximum damage with a damage-dealing Wizard spell (lvl 1-5)",
                        "cost": "First use is free; subsequent uses before LR deal 2d12 Necrotic damage per spell level (increases by 1d12 each use)",
                        "restriction": "Necrotic damage ignores Resistance and Immunity"
                    }
                }
            ]
        }
    },
    "illusionist": {
        "id": "illusionist",
        "name": "Illusionist",
        "description": "As an Illusionist, you focus your studies on magic that dazzles the senses, befuddles the mind, and fools even the wisest folks. Your magic is subtle, yet its effects can be as world-shaking as any bolt of fire. You specialize in weaving light and sound into intricate patterns, eventually learning to give your phantasms a touch of semi-reality.",
        "features": {
            3: [
                {
                    "id": "illusionist_illusion_savant",
                    "name": "Illusion Savant",
                    "summary": "Free Illusion spells for your spellbook (two at lvl 3, plus one per new slot level).",
                    "description": "Choose two Wizard spells from the Illusion school, each of which must be no higher than level 2, and add them to your spellbook for free. In addition, whenever you gain access to a new level of spell slots in this class, you can add one Wizard spell from the Illusion school to your spellbook for free. The chosen spell must be of a level for which you have spell slots.",
                    "details": {
                        "initial_spells": "Choose two Illusion spells (lvl 0-2) for your spellbook",
                        "progression_spells": "Add one Illusion spell for free whenever you gain access to a new level of Wizard spell slots"
                    }
                },
                {
                    "id": "illusionist_improved_illusions",
                    "name": "Improved Illusions",
                    "summary": "No Verbal components for Illusion spells; +60ft range; enhanced Minor Illusion.",
                    "description": "You can cast Illusion spells without providing Verbal components, and if an Illusion spell you cast has a range of 10+ feet, the range increases by 60 feet. You also know the Minor Illusion cantrip. If you already know it, you learn a different Wizard cantrip of your choice. The cantrip doesn't count against your number of cantrips known. You can create both a sound and an image with a single casting of Minor Illusion, and you can cast it as a Bonus Action.",
                    "details": {
                        "component_reduction": "No Verbal components for Illusion spells",
                        "range_bonus": "+60ft range to Illusion spells with 10ft+ range",
                        "minor_illusion": "Learn Minor Illusion (or another cantrip); image and sound in one casting; Bonus Action casting"
                    }
                }
            ],
            6: [
                {
                    "id": "illusionist_phantasmal_creatures",
                    "name": "Phantasmal Creatures",
                    "summary": "Summon Beast and Summon Fey prepared; can cast as Illusion (spectral) for free with half HP.",
                    "description": "You always have the Summon Beast and Summon Fey spells prepared. Whenever you cast either spell, you can change its school to Illusion, which causes the summoned creature to appear spectral. You can cast the Illusion version of each spell without expending a spell slot, but casting it without a slot halves the creature's Hit Points. Once you cast either spell without a spell slot, you must finish a Long Rest before you can cast the spell in that way again.",
                    "details": {
                        "prepared": ["Summon Beast", "Summon Fey"],
                        "special_casting": "Can change school to Illusion (spectral appearance)",
                        "free_use": "Can cast once per LR without a spell slot; creature has half HP"
                    }
                }
            ],
            10: [
                {
                    "id": "illusionist_illusory_self",
                    "name": "Illusory Self",
                    "summary": "Reaction: Interpose illusory duplicate to cause an attack to automatically miss.",
                    "description": "When a creature hits you with an attack roll, you can take a Reaction to interpose an illusory duplicate of yourself between the attacker and yourself. The attack automatically misses you, then the illusion dissipates. Once you use this feature, you can't use it again until you finish a Short or Long Rest. You can also restore your use of it by expending a level 2+ spell slot (no action required).",
                    "details": {
                        "action": "Reaction (when hit by an attack roll)",
                        "effect": "Attack automatically misses; illusion dissipates",
                        "recharge": "Short/Long Rest (or expend lvl 2+ spell slot)"
                    }
                }
            ],
            14: [
                {
                    "id": "illusionist_illusory_reality",
                    "name": "Illusory Reality",
                    "summary": "Bonus Action: Make one inanimate, nonmagical object in an illusion real for 1 minute.",
                    "description": "You have learned to weave shadow magic into your illusions to give them a semi-reality. When you cast an Illusion spell with a spell slot, you can choose one inanimate, nonmagical object that is part of the illusion and make that object real. You can do this on your turn as a Bonus Action while the spell is ongoing. The object remains real for 1 minute, during which it can't deal damage or give any conditions. For example, you can create an illusion of a bridge over a chasm and then make it real and cross it.",
                    "details": {
                        "trigger": "Cast an Illusion spell with a spell slot",
                        "action": "Bonus Action (while spell is ongoing)",
                        "effect": "One object in the illusion becomes real for 1 minute; cannot deal damage or give conditions"
                    }
                }
            ]
        }
    }
}
