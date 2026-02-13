"""
Subclass definitions for the Bard class.
"""

BARD_SUBCLASSES = {
    "dance": {
        "id": "dance",
        "name": "College Of Dance",
        "description": "Bards of the College of Dance believe that movement is the ultimate expression of magic. They weave spells into their choreography, turning every step into a flourish of arcane power and every gesture into a dazzling display of grace and precision.",
        "features": {
            3: [
                {
                    "id": "dance_dazzling_footwork",
                    "name": "Dazzling Footwork",
                    "summary": "While unarmored/unshielded: Advantage on Dance-based Performance, AC = 10 + DEX + CHA, for free Unarmed Strike when expending Inspiration.",
                    "details": {
                        "unarmored_ac": "10 + Dexterity modifier + Charisma modifier",
                        "unarmed_strike": {
                            "trigger": "Expend Bardic Inspiration as Action/Bonus/Reaction",
                            "benefit": "One free Unarmed Strike as part of that action",
                            "damage_bonus": "Can use DEX instead of STR",
                            "damage_amount": "Bardic Inspiration die + DEX modifier (Bludgeoning)"
                        },
                        "performance_advantage": "Advantage on Charisma (Performance) involving dancing"
                    }
                }
            ],
            6: [
                {
                    "id": "dance_inspiring_movement",
                    "name": "Inspiring Movement",
                    "summary": "Reaction: expend Inspiration to move up to half Speed (no OA) and allow an ally to do the same.",
                    "details": {
                        "trigger": "Enemy you see ends turn within 5ft",
                        "action": "Reaction",
                        "cost": "One use of Bardic Inspiration",
                        "effect": "Move up to half speed; one ally within 30ft can also move half speed as a Reaction",
                        "restriction": "No Opportunity Attacks provoked by this movement"
                    }
                },
                {
                    "id": "dance_tandem_footwork",
                    "name": "Tandem Footwork",
                    "summary": "Expend Inspiration when rolling Initiative to add BI die to yours and nearby allies' rolls.",
                    "details": {
                        "trigger": "Roll Initiative",
                        "cost": "One use of Bardic Inspiration",
                        "effect": "Add BI die roll to your Initiative and that of allies within 30ft who can see/hear you"
                    }
                }
            ],
            14: [
                {
                    "id": "dance_leading_evasion",
                    "name": "Leading Evasion",
                    "summary": "Gain Evasion benefits for DEX saves (no damage on success, half on failure) and share it with nearby allies.",
                    "details": {
                        "effect": "No damage on successful DEX save, half damage on failed save",
                        "sharing": "Share benefit with allies within 5ft making the same save",
                        "restriction": "Can't use while Incapacitated"
                    }
                }
            ]
        }
    },
    "glamour": {
        "id": "glamour",
        "name": "College Of Glamour",
        "description": "Bards of the College of Glamour trace their origins to the realm of the Verdant Realm. Their magic is an unearthly beauty that can both inspire and terrify, allowing them to bend the minds of others and cloak themselves in a majestic aura that makes them nearly untouchable.",
        "features": {
            3: [
                {
                    "id": "glamour_beguiling_magic",
                    "name": "Beguiling Magic",
                    "summary": "Always have Charm Person and Mirror Image prepared; can Charm/Frighten a creature after casting Enchantment/Illusion spells.",
                    "details": {
                        "spells_prepared": ["Charm Person", "Mirror Image"],
                        "effect": "After casting Enchantment/Illusion spell with a slot, target within 60ft makes WIS save or is Charmed/Frightened for 1 minute",
                        "recharge": "Long Rest or expend one use of Bardic Inspiration"
                    }
                },
                {
                    "id": "glamour_mantle_of_inspiration",
                    "name": "Mantle Of Inspiration",
                    "summary": "Bonus Action: expend Inspiration to grant Temp HP and Reaction movement to allies.",
                    "details": {
                        "action": "Bonus Action",
                        "cost": "One use of Bardic Inspiration",
                        "range": "60ft",
                        "targets": "Up to Charisma modifier allies (min 1)",
                        "benefit": "Temp HP equal to 2x Bardic Inspiration die roll; allies can use Reaction to move up to their Speed without Opportunity Attacks"
                    }
                }
            ],
            6: [
                {
                    "id": "glamour_mantle_of_majesty",
                    "name": "Mantle Of Majesty",
                    "summary": "Cast Command as a Bonus Action without a slot for 1 minute; Charmed creatures auto-fail saves.",
                    "details": {
                        "spells_prepared": ["Command"],
                        "action": "Bonus Action (initial cast and subsequent casts)",
                        "duration": "1 minute (Concentration)",
                        "effect": "Cast Command for free; Charmed targets auto-fail the save",
                        "recharge": "Long Rest or expend a level 3+ spell slot"
                    }
                }
            ],
            14: [
                {
                    "id": "glamour_unbreakable_majesty",
                    "name": "Unbreakable Majesty",
                    "summary": "Bonus Action for 1 minute: attackers must pass a CHA save or miss their first hit of the turn.",
                    "details": {
                        "action": "Bonus Action",
                        "duration": "1 minute",
                        "effect": "First time a creature hits you on a turn, they must pass a CHA save vs your spell save DC or the attack misses",
                        "recharge": "Short or Long Rest"
                    }
                }
            ]
        }
    },
    "lore": {
        "id": "lore",
        "name": "College Of Lore",
        "description": "Bards of the College of Lore are collectors of knowledge, fragments of history, and scraps of arcane lore. They use their wit to uncover truths others miss and their magic to master spells beyond the reach of most, making them the ultimate versatile masters of the spoken and written word.",
        "features": {
            3: [
                {
                    "id": "lore_bonus_proficiencies",
                    "name": "Bonus Proficiencies",
                    "summary": "Gain proficiency with three skills of your choice.",
                    "details": {
                        "skills": {
                            "choose": 3,
                            "options": "Any"
                        }
                    }
                },
                {
                    "id": "lore_cutting_words",
                    "name": "Cutting Words",
                    "summary": "Reaction: expend Inspiration to subtract from a creature's damage, ability check, or attack roll.",
                    "details": {
                        "action": "Reaction",
                        "trigger": "Creature within 60ft makes damage roll or succeeds on ability check/attack roll",
                        "cost": "One use of Bardic Inspiration",
                        "effect": "Subtract Bardic Inspiration die roll from the target's roll"
                    }
                }
            ],
            6: [
                {
                    "id": "lore_magical_discoveries",
                    "name": "Magical Discoveries",
                    "summary": "Learn two spells from Cleric, Druid, or Wizard lists; swappable on level up.",
                    "details": {
                        "spells_count": 2,
                        "lists": ["Cleric", "Druid", "Wizard"],
                        "restriction": "Must be a Cantrip or a spell for which you have slots",
                        "swapping": "Replace one spell whenever you gain a Bard level"
                    }
                }
            ],
            14: [
                {
                    "id": "lore_peerless_skill",
                    "name": "Peerless Skill",
                    "summary": "Add Inspiration die to a failed check or attack. Die isn't expended if you still fail.",
                    "details": {
                        "trigger": "Fail an ability check or attack roll",
                        "cost": "One use of Bardic Inspiration",
                        "effect": "Add BI die to the d20 roll",
                        "special": "Bardic Inspiration is NOT expended if the roll still fails"
                    }
                }
            ]
        }
    },
    "valor": {
        "id": "valor",
        "name": "College Of Valor",
        "description": "Bards of the College of Valor are daring skalds who preserve the memory of great heroes and inspire a new generation of legends. They thrive in the thick of battle, weaving magic and steel together to bolster their allies' defenses and amplify their strikes.",
        "features": {
            3: [
                {
                    "id": "valor_combat_inspiration",
                    "name": "Combat Inspiration",
                    "summary": "Inspiration die can be used to add to AC as a Reaction when hit, or add to damage after a hit.",
                    "details": {
                        "options": [
                            "Defense: Reaction to add BI die to AC when hit",
                            "Offense: Roll BI die to add damage immediately after hitting a target"
                        ]
                    }
                },
                {
                    "id": "valor_martial_training",
                    "name": "Martial Training",
                    "summary": "Proficiency with Martial weapons, Medium armor, and Shields; weapons serve as Spellcasting Focus.",
                    "details": {
                        "proficiencies": {
                            "weapons": ["Martial"],
                            "armor": ["Medium"],
                            "shields": ["Shields"]
                        },
                        "focus": "Can use Simple or Martial weapons as a Spellcasting Focus for Bard spells"
                    }
                }
            ],
            6: [
                {
                    "id": "valor_extra_attack",
                    "name": "Extra Attack",
                    "summary": "Attack twice; can replace one attack with a Cantrip (1-action casting time).",
                    "details": {
                        "attacks": 2,
                        "special": "One attack can be replaced by a 1-action cantrip"
                    }
                }
            ],
            14: [
                {
                    "id": "valor_battle_magic",
                    "name": "Battle Magic",
                    "summary": "Bonus Action: make one weapon attack after casting a 1-action spell.",
                    "details": {
                        "trigger": "Cast a spell with a casting time of 1 action",
                        "action": "Bonus Action",
                        "effect": "One weapon attack"
                    }
                }
            ]
        }
    }
}
