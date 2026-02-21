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
                    "details": {
                        "initial_spells": "Choose two Abjuration spells (lvl 0-2) for your spellbook",
                        "progression_spells": "Add one Abjuration spell for free whenever you gain access to a new level of Wizard spell slots"
                    }
                },
                {
                    "id": "abjurer_arcane_ward",
                    "name": "Arcane Ward",
                    "summary": "Create a protective ward when casting Abjuration spells that absorbs damage.",
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
                    "details": {
                        "initial_spells": "Choose two Divination spells (lvl 0-2) for your spellbook",
                        "progression_spells": "Add one Divination spell for free whenever you gain access to a new level of Wizard spell slots"
                    }
                },
                {
                    "id": "diviner_portent",
                    "name": "Portent",
                    "summary": "Record two d20 rolls after a Long Rest to replace any d20 tests you or others make.",
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
                    "details": {
                        "initial_spells": "Choose two Evocation spells (lvl 0-2) for your spellbook",
                        "progression_spells": "Add one Evocation spell for free whenever you gain access to a new level of Wizard spell slots"
                    }
                },
                {
                    "id": "evoker_potent_cantrip",
                    "name": "Potent Cantrip",
                    "summary": "Damaging cantrips deal half damage on a miss or successful save.",
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
                    "details": {
                        "initial_spells": "Choose two Illusion spells (lvl 0-2) for your spellbook",
                        "progression_spells": "Add one Illusion spell for free whenever you gain access to a new level of Wizard spell slots"
                    }
                },
                {
                    "id": "illusionist_improved_illusions",
                    "name": "Improved Illusions",
                    "summary": "No Verbal components for Illusion spells; +60ft range; enhanced Minor Illusion.",
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
