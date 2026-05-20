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
                    "description": "While you aren't wearing armor or wielding a Shield, you gain the following benefits. \n *Dance Virtuoso*. You have Advantage on any Charisma (Performance) check you make that involves you dancing. \n *Unarmored Defense*. Your base Armor Class equals 10 plus your Dexterity and Charisma modifiers. \n *Agile Strikes*. When you expend a use of your Bardic Inspiration as part of an action, a Bonus Action, or a Reaction, you can make one Unarmed Strike as part of that action, Bonus Action, or Reaction. \n *Bardic Damage*. You can use Dexterity instead of Strength for the attack rolls of your Unarmed Strikes. When you deal damage with an Unarmed Strike, you can deal Bludgeoning damage equal to a roll of your Bardic Inspiration die plus your Dexterity modifier, instead of the strike's normal damage. This roll doesn't expend the die.",
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
                    "description": "When an enemy you can see ends its turn within 5 feet of you, you can take a Reaction and expend one use of your Bardic Inspiration to move up to half your Speed. Then one ally of your choice within 30 feet of you can also move up to half their Speed using their Reaction. None of this feature's movement provokes Opportunity Attacks.",
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
                    "description": "When you roll Initiative, you can expend one use of your Bardic Inspiration if you don't have the Incapacitated condition. When you do so, roll your Bardic Inspiration die; you and each ally within 30 feet of you who can see or hear you gains a bonus to Initiative equal to the number rolled.",
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
                    "description": "When you are subjected to an effect that allows you to make a Dexterity saving throw to take only half damage, you instead take no damage if you succeed on the saving throw and only half damage if you fail. If any creatures within 5 feet of you are making the same Dexterity saving throw, you can share this benefit with them for that save. You can't use this feature if you have the Incapacitated condition.",
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
                    "description": "You always have the Charm Person and Mirror Image spells prepared. In addition, immediately after you cast an Enchantment or Illusion spell using a spell slot, you can cause a creature you can see within 60 feet of yourself to make a Wisdom saving throw against your spell save DC. On a failed save, the target has the Charmed or Frightened condition (your choice) for 1 minute. The target repeats the save at the end of each of its turns, ending the effect on itself on a success. Once you use this benefit, you can't use it again until you finish a Long Rest. You can also restore your use of it by expending one use of your Bardic Inspiration (no action required).",
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
                    "description": "You can weave fey magic into a song or dance to fill others with vigor. As a Bonus Action, you can expend a use of Bardic Inspiration, rolling a Bardic Inspiration die. When you do so, choose a number of other creatures within 60 feet of yourself, up to a number equal to your Charisma modifier (minimum of one creature). Each of those creatures gains a number of Temporary Hit Points equal to two times the number rolled on the Bardic Inspiration die, and then each can use its Reaction to move up to its Speed without provoking Opportunity Attacks.",
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
                    "description": "You always have the Command spell prepared. As a Bonus Action, you cast Command without expending a spell slot, and you take on an unearthly appearance for 1 minute or until your Concentration ends. During this time, you can cast Command as a Bonus Action without expending a spell slot. Any creature Charmed by you automatically fails its saving throw against the Command you cast with this feature. Once you use this feature, you can't use it again until you finish a Long Rest. You can also restore your use of it by expending a level 3+ spell slot (no action required).",
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
                    "description": "As a Bonus Action, you can assume a magically majestic presence for 1 minute or until you have the Incapacitated condition. For the duration, whenever any creature hits you with an attack roll for the first time on a turn, the attacker must succeed on a Charisma saving throw against your spell save DC, or the attack misses instead, as the creature recoils from your majesty. Once you assume this majestic presence, you can't do so again until you finish a Short or Long Rest.",
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
                    "description": "You gain proficiency with three skills of your choice.",
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
                    "description": "You learn to use your wit to supernaturally distract, confuse, and otherwise sap the confidence and competence of others. When a creature that you can see within 60 feet of yourself makes a damage roll or succeeds on an ability check or attack roll, you can take a Reaction to expend one use of your Bardic Inspiration; roll your Bardic Inspiration die, and subtract the number rolled from the creature's roll, reducing the damage or potentially turning the success into a failure.",
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
                    "description": "You learn two spells of your choice. These spells can come from the Cleric, Druid, or Wizard spell list or any combination thereof (see a class's section for its spell list). A spell you choose must be a cantrip or a spell for which you have spell slots, as shown in the Bard Features table. You always have the chosen spells prepared, and whenever you gain a Bard level, you can replace one of the spells with another spell that meets these requirements.",
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
                    "description": "When you make an ability check or attack roll and fail, you can expend one use of Bardic Inspiration; roll the Bardic Inspiration die, and add the number rolled to the d20, potentially turning a failure into a success. On a failure, the Bardic Inspiration isn't expended.",
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
                    "description": "You can use your wit to turn the tide of battle. A creature that has a Bardic Inspiration die from you can use it for one of the following effects. \n *Defense*. When the creature is hit by an attack roll, that creature can use its Reaction to roll the Bardic Inspiration die and add the number rolled to its AC against that attack, potentially causing the attack to miss. \n *Offense*. Immediately after the creature hits a target with an attack roll, the creature can roll the Bardic Inspiration die and add the number rolled to the attack's damage against the target.",
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
                    "description": "You gain proficiency with Martial weapons and training with Medium armor and Shields. In addition, you can use a Simple or Martial weapon as a Spellcasting Focus to cast spells from your Bard spell list.",
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
                    "description": "You can attack twice instead of once whenever you take the Attack action on your turn. In addition, you can cast one of your cantrips that has a casting time of an action in place of one of those attacks.",
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
                    "description": "After you cast a spell that has a casting time of an action, you can make one attack with a weapon as a Bonus Action.",
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
