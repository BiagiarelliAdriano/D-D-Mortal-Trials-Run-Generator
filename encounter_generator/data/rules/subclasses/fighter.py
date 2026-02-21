"""
Subclass definitions for the Fighter class.
"""

from encounter_generator.data.rules.spell_tables import THIRD_CASTER_PREPARED

BATTLE_MASTER_MANEUVERS = {
    "ambush": {
        "name": "Ambush",
        "summary": "Add Superiority Die to Stealth or Initiative.",
        "details": "When you make a Dexterity (Stealth) check or an Initiative roll, you can expend one Superiority Die and add the die to the roll, unless you have the Incapacitated condition."
    },
    "bait_and_switch": {
        "name": "Bait and Switch",
        "summary": "Switch places with a creature and gain an AC bonus.",
        "details": "When you're within 5ft of a creature on your turn, you can expend one Superiority Die and switch places with that creature, provided you spend at least 5ft of movement and the creature is willing and doesn't have the Incapacitated condition. This movement doesn't provoke Opportunity Attacks. Roll the Superiority Die. Until the start of your next turn, you or the other creature (your choice) gains a bonus to AC equal to the number rolled."
    },
    "commander_strike": {
        "name": "Commander's Strike",
        "summary": "Replace an attack to let a companion attack as a Reaction.",
        "details": "When you take the Attack action on your turn, you can replace one of your attacks to direct one of your companions to strike. When you do so, choose a willing creature who can see or hear you and expend one Superiority Die. That creature can immediately use its Reaction to make one attack with a weapon or an Unarmed Strike, adding the Superiority Die to the attack's damage roll on a hit."
    },
    "commanding_presence": {
        "name": "Commanding Presence",
        "summary": "Add Superiority Die to Intimidation, Performance, or Persuasion.",
        "details": "When you make a Charisma (Intimidation, Performance or Persuasion) check, you can expend one Superiority Die and add that die to the roll."
    },
    "disarming_attack": {
        "name": "Disarming Attack",
        "summary": "Attempt to disarm a target on a hit.",
        "details": "When you hit a creature with an attack roll, you can expend one Superiority Die to attempt to disarm the target. Add the Superiority Die roll to the attack's damage roll. The target must succeed on a Strength saving throw or drop one object of your choice that it's holding, with the object landing in its space."
    },
    "distracting_strike": {
        "name": "Distracting Strike",
        "summary": "Grant Advantage to the next ally attacking the target.",
        "details": "When you hit a creature with an attack roll, you can expend one Superiority Die roll to the attack's damage roll. The next attack roll against the target by an attacker other than you has Advantage if the attack is made before the start of your next turn."
    },
    "evasive_footwork": {
        "name": "Evasive Footwork",
        "summary": "Take Disengage action as a Bonus Action and gain AC bonus.",
        "details": "As a Bonus Action, you can expend one Superiority Die and take the Disengage action. You also roll the die and add the number rolled to your AC until the start of your next turn."
    },
    "feinting_attack": {
        "name": "Feinting Attack",
        "summary": "Gain Advantage on next attack against a target within 5ft.",
        "details": "As a Bonus Action, you can expend one Superiority Die to feint, choosing one creature within 5ft of yourself as your target. You have Advantage on your next attack roll against that target this turn. If that attack hits, add the Superiority Die to the attack's damage roll."
    },
    "goading_attack": {
        "name": "Goading Attack",
        "summary": "Attempt to goad a target into attacking you.",
        "details": "When you hit a creature with an attack roll, you can expend one Superiority Die to attempt to goad the target into attacking you. Add the Superiority Die to the attack's damage roll. The target must succeed on a Wisdom saving throw or have Disadvantage on attack rolls against targets other than you until the end of your next turn."
    },
    "lunging_attack": {
        "name": "Lunging Attack",
        "summary": "Take Dash action as a Bonus Action and add damage to a melee hit.",
        "details": "As a Bonus Action, you can expend one Superiority Die and take the Dash action. If you move at least 5ft in a straight line immediately before hitting with a melee attack as part of the Attack action on this turn, you can add the Superiority Die to the attack's damage roll."
    },
    "maneuvering_attack": {
        "name": "Maneuvering Attack",
        "summary": "Maneuver an ally into a new position on a hit.",
        "details": "When you hit a creature with an attack roll, you can expend one Superiority Die to maneuver one of your comrades into another position. Add the Superiority Die roll to the attack's damage roll, and choose a willing creature who can see or hear you. That creature can use its Reaction to move up to half its Speed without provoking an Opportunity Attack from the target of your attack."
    },
    "menacing_attack": {
        "name": "Menacing Attack",
        "summary": "Attempt to frighten a target on a hit.",
        "details": "When you hit a creature with an attack roll, you can expend one Superiority Die to attempt to frighten the target. Add the Superiority Die to the attack's damage roll. The target must succeed on a Wisdom saving throw or have the Frightened condition until the end of your next turn."
    },
    "parry": {
        "name": "Parry",
        "summary": "Reduce incoming melee damage as a Reaction.",
        "details": "When another creature damages you with a melee attack roll, you can take a Reaction and expend one Superiority Die to reduce the damage by the number you roll on your Superiority Die plus your Strength or Dexterity modifier (your choice)."
    },
    "precision_attack": {
        "name": "Precision Attack",
        "summary": "Add Superiority Die to a missed attack roll.",
        "details": "When you miss with an attack roll, you can expend one Superiority Die, roll that die, and add it to the attack roll, potentially causing the attack to hit."
    },
    "pushing_attack": {
        "name": "Pushing Attack",
        "summary": "Attempt to push a target back 15ft on a hit.",
        "details": "When you hit a creature with an attack roll using a weapon or an Unarmed Strike, you can expend one Superiority Die to attempt to drive the target back. Add the Superiority Die to the attack's damage roll. If the target is Large or smaller, it must succeed on a Strength saving throw or be pushed up to 15ft directly away from you."
    },
    "rally": {
        "name": "Rally",
        "summary": "Grant Temporary HP to an ally within 30ft.",
        "details": "As a Bonus Action, you can expend one Superiority Die to bolster the resolve of a companion. Choose an ally of yours within 30ft of yourself who can see or hear you. That creature gains Temporary Hit Points equal to the Superiority Die roll plus half your Fighter level (round down)."
    },
    "riposte": {
        "name": "Riposte",
        "summary": "Make a melee attack as a Reaction when missed.",
        "details": "When a creature misses you with a melee attack roll, you can take a Reaction and expend one Superiority Die to make a melee attack roll with a weapon or an Unarmed Strike against a the creature. If you hit, add the Superiority Die to the attack's damage."
    },
    "sweeping_attack": {
        "name": "Sweeping Attack",
        "summary": "Damage a second creature within 5ft of your target.",
        "details": "When you hit a creature with a melee attack roll using a weapon or an Unarmed Strike, you can expend one Superiority Die to attempt to damage another creature. Choose another creature within 5ft of the original target and within your reach. If the original attack roll would hit the second creature, it takes damage equal to the number you roll on your Superiority Die. The damage is of the same type dealt by the original attack."
    },
    "tactical_assessment": {
        "name": "Tactical Assessment",
        "summary": "Add Superiority Die to History, Investigation, or Insight.",
        "details": "When you make an Intelligence (History or Investigation) check or a Wisdom (Insight) check, you can expend one Superiority Die and add that die to the ability check."
    },
    "trip_attack": {
        "name": "Trip Attack",
        "summary": "Attempt to knock a target Prone on a hit.",
        "details": "When you hit a creature with an attack roll using a weapon or an Unarmed Strike, you can expend one Superiority Die and add the die to the attack's damage roll. If the target is Large or smaller, it must succeed on a Strength saving throw or have the Prone condition."
    }
}

FIGHTER_SUBCLASSES = {
    "battle_master": {
        "id": "battle_master",
        "name": "Battle Master",
        "description": "The Battle Master is a student of the art of war, viewing combat as a discipline to be mastered through study and practice. These fighters use superior field tactics and maneuvers to control the flow of battle and outmaneuver their opponents.",
        "features": {
            3: [
                {
                    "id": "battle_master_combat_superiority",
                    "name": "Combat Superiority",
                    "summary": "Learn maneuvers fueled by Superiority Dice (d8s) to enhance attacks and control the battlefield.",
                    "details": {
                        "superiority_dice": {
                            "count": {3: 4, 7: 5, 15: 6},
                            "size": {3: "d8", 10: "d10", 18: "d12"},
                            "recharge": "Short or Long Rest"
                        },
                        "maneuvers_known": {3: 3, 7: 5, 10: 7, 15: 9},
                        "maneuver_options": BATTLE_MASTER_MANEUVERS,
                        "rules": [
                            "One maneuver per attack",
                            "Replace one maneuver when learning new ones",
                            "Saving Throw DC: 8 + Str/Dex mod + Proficiency Bonus"
                        ]
                    }
                },
                {
                    "id": "battle_master_student_of_war",
                    "name": "Student Of War",
                    "summary": "Gain proficiency with one type of Artisan's Tools and one skill from the Fighter list.",
                    "details": {
                        "tool_proficiency": "Choice of one Artisan's Tools",
                        "skill_proficiency": "Choice of one skill from Fighter class list"
                    }
                }
            ],
            7: [
                {
                    "id": "battle_master_know_your_enemy",
                    "name": "Know Your Enemy",
                    "summary": "Bonus Action: see a creature's Immunities, Resistances, and Vulnerabilities (30ft).",
                    "details": {
                        "action": "Bonus Action",
                        "range": "30ft",
                        "recharge": "Long Rest (can restore by expending one Superiority Die)"
                    }
                }
            ],
            10: [
                {
                    "id": "battle_master_improved_combat_superiority",
                    "name": "Improved Combat Superiority",
                    "summary": "Your Superiority Die becomes a d10.",
                    "details": {
                        "die_upgrade": "d10"
                    }
                }
            ],
            15: [
                {
                    "id": "battle_master_relentless",
                    "name": "Relentless",
                    "summary": "Once per turn, roll 1d8 instead of expending a Superiority Die for a maneuver.",
                    "details": {
                        "effect": "Roll 1d8 to replace Superiority Die expenditure",
                        "limit": "Once per turn"
                    }
                }
            ],
            18: [
                {
                    "id": "battle_master_ultimate_combat_superiority",
                    "name": "Ultimate Combat Superiority",
                    "summary": "Your Superiority Die becomes a d12.",
                    "details": {
                        "die_upgrade": "d12"
                    }
                }
            ]
        }
    },
    "champion": {
        "id": "champion",
        "name": "Champion",
        "description": "The Champion focuses on the development of raw physical power perfected to deadly perfection. Those who model themselves on this archetype combine rigorous training with physical excellence to deal devastating blows and outlast any opponent on the field of honor.",
        "features": {
            3: [
                {
                    "id": "champion_improved_critical",
                    "name": "Improved Critical",
                    "summary": "Your weapon and Unarmed Strike rolls score a Critical Hit on a 19 or 20.",
                    "details": {
                        "critical_range": [19, 20]
                    }
                },
                {
                    "id": "champion_remarkable_athlete",
                    "name": "Remarkable Athlete",
                    "summary": "Gain Advantage on Initiative and Athletics checks; move half speed without opportunity attacks after a crit.",
                    "details": {
                        "advantages": ["Initiative rolls", "Strength (Athletics) checks"],
                        "on_crit": "Move up to half your Speed without provoking Opportunity Attacks"
                    }
                }
            ],
            7: [
                {
                    "id": "champion_additional_fighting_style",
                    "name": "Additional Fighting Style",
                    "summary": "Gain another Fighting Style feat of your choice.",
                    "details": {
                        "benefit": "One additional Fighting Style feat"
                    }
                }
            ],
            10: [
                {
                    "id": "champion_heroic_warrior",
                    "name": "Heroic Warrior",
                    "summary": "Start each turn in combat with Heroic Inspiration if you don't already have it.",
                    "details": {
                        "trigger": "Start of turn in combat",
                        "effect": "Gain Heroic Inspiration"
                    }
                }
            ],
            15: [
                {
                    "id": "champion_superior_critical",
                    "name": "Superior Critical",
                    "summary": "Your weapon and Unarmed Strike rolls score a Critical Hit on a 18-20.",
                    "details": {
                        "critical_range": [18, 19, 20]
                    }
                }
            ],
            18: [
                {
                    "id": "champion_survivor",
                    "name": "Survivor",
                    "summary": "Advantage on Death Saves (18-20 counts as 20); regain 5 + Con mod HP at start of turn if Bloodied.",
                    "details": {
                        "death_saves": {
                            "advantage": True,
                            "critical_success_range": [18, 19, 20]
                        },
                        "regeneration": {
                            "amount": "5 + Constitution modifier",
                            "condition": "Bloodied and at least 1 HP",
                            "trigger": "Start of turn"
                        }
                    }
                }
            ]
        }
    },
    "eldritch_knight": {
        "id": "eldritch_knight",
        "name": "Eldritch Knight",
        "description": "The Eldritch Knight combines the martial mastery common to all fighters with a careful study of magic. They use magical energy to enhance their weapons, armor, and combat tactics, mirroring the techniques of wizards but focusing them through the lens of battlefield expertise.",
        "features": {
            3: [
                {
                    "id": "eldritch_knight_spellcasting",
                    "name": "Spellcasting",
                    "summary": "Cast Wizard spells using Intelligence. Use an Arcane Focus and bond with weapons.",
                    "details": {
                        "ability": "Intelligence",
                        "progression": "third",
                        "cantrips_known": {3: 2, 10: 3},
                        "spells_known_count": THIRD_CASTER_PREPARED,
                        "spell_list": "Wizard",
                        "ritual_casting": False,
                        "focus": "Arcane Focus"
                    }
                },
                {
                    "id": "eldritch_knight_war_bond",
                    "name": "War Bond",
                    "summary": "Bond with up to two weapons; can't be disarmed and can summon them as a Bonus Action.",
                    "details": {
                        "ritual_duration": "1 hour (can be during Short Rest)",
                        "benefits": [
                            "Cannot be disarmed unless Incapacitated",
                            "Bonus Action: teleport weapon to hand (if on same plane)"
                        ],
                        "limit": "Up to 2 bonded weapons"
                    }
                }
            ],
            7: [
                {
                    "id": "eldritch_knight_war_magic",
                    "name": "War Magic",
                    "summary": "When you take the Attack action, replace one attack with a Wizard cantrip (1 action).",
                    "details": {
                        "trigger": "Attack action",
                        "effect": "Replace 1 attack with a cantrip"
                    }
                }
            ],
            10: [
                {
                    "id": "eldritch_knight_eldritch_strike",
                    "name": "Eldritch Strike",
                    "summary": "Hitting a creature with a weapon gives them Disadvantage on their next save against your spells.",
                    "details": {
                        "trigger": "Weapon hit",
                        "effect": "Disadvantage on next save vs your spell (until end of your next turn)"
                    }
                }
            ],
            15: [
                {
                    "id": "eldritch_knight_arcane_charge",
                    "name": "Arcane Charge",
                    "summary": "Teleport up to 30ft when you use Action Surge (before or after the extra action).",
                    "details": {
                        "trigger": "Action Surge",
                        "range": "30ft",
                        "effect": "Teleport"
                    }
                }
            ],
            18: [
                {
                    "id": "eldritch_knight_improved_war_magic",
                    "name": "Improved War Magic",
                    "summary": "When you take the Attack action, replace two attacks with a Level 1 or 2 Wizard spell (1 action).",
                    "details": {
                        "trigger": "Attack action",
                        "effect": "Replace 2 attacks with a Lvl 1-2 spell"
                    }
                }
            ]
        }
    },
    "psi_warrior": {
        "id": "psi_warrior",
        "name": "Psi Warrior",
        "description": "Awake to the psionic power within, the Psi Warrior augments their physical prowess with the power of their mind. They use telekinetic energy to shield themselves and others, to propel their weapon strikes with mental force, and to eventually master the very air around them.",
        "features": {
            3: [
                {
                    "id": "psi_warrior_psionic_power",
                    "name": "Psionic Power",
                    "summary": "Fuel telekinetic abilities using Psionic Energy Dice (scaling count and size).",
                    "details": {
                        "dice_scaling": {
                            3: "4d6",
                            5: "6d8",
                            9: "8d8",
                            11: "8d10",
                            13: "10d10",
                            17: "12d12"
                        },
                        "recharge": "One on Short Rest, all on Long Rest",
                        "powers": {
                            "protective_field": "Reaction: expend die to reduce damage to self or ally (30ft) by roll + Intelligence mod.",
                            "psionic_strike": "Once per turn: expend die to deal extra Force damage (roll + Intelligence mod) on weapon hit (30ft).",
                            "telekinetic_movement": "Magic Action: move loose object (Large or smaller) or willing creature 30ft. Once per Short/Long rest (or expend die)."
                        }
                    }
                }
            ],
            7: [
                {
                    "id": "psi_warrior_telekinetic_adept",
                    "name": "Telekinetic Adept",
                    "summary": "Gain Psi-Powered Leap (flight for 1 turn) and Telekinetic Thrust (prone/push on Psionic Strike).",
                    "details": {
                        "psi_powered_leap": "Bonus Action: gain Fly Speed (2x Speed) until end of turn. Once per Short/Long rest (or expend die).",
                        "telekinetic_thrust": "When using Psionic Strike: target makes Strength save vs DC (8 + Int + Prof) or is Prone or pushed 10ft horizontally."
                    }
                }
            ],
            10: [
                {
                    "id": "psi_warrior_guarded_mind",
                    "name": "Guarded Mind",
                    "summary": "Resistance to Psychic damage; expend die to end Charmed or Frightened conditions.",
                    "details": {
                        "resistance": "Psychic",
                        "cleanse": "Expend die at start of turn (no action) to end every Charmed or Frightened effect."
                    }
                }
            ],
            15: [
                {
                    "id": "psi_warrior_bulwark_of_force",
                    "name": "Bulwark Of Force",
                    "summary": "Bonus Action: grant Half Cover to Intelligence mod allies within 30ft for 1 minute.",
                    "details": {
                        "action": "Bonus Action",
                        "range": "30ft",
                        "targets": "Intelligence modifier creatures (minimum 1)",
                        "effect": "Half Cover (+2 AC/Dex saves)",
                        "duration": "1 minute or until Incapacitated",
                        "recharge": "Long Rest (or expend die)"
                    }
                }
            ],
            18: [
                {
                    "id": "psi_warrior_telekinetic_master",
                    "name": "Telekinetic Master",
                    "summary": "Cast Telekinesis for free (Intelligence). Attack as a Bonus Action while concentrating.",
                    "details": {
                        "spell": "Telekinesis (no slot/components, Intelligence)",
                        "combat_synergy": "Make one weapon attack as a Bonus Action while concentrating on the spell",
                        "recharge": "Long Rest (or expend die)"
                    }
                }
            ]
        }
    }
}
