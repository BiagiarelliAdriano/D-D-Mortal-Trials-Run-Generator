"""
Subclass definitions for the Fighter class.
"""

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
                        "spells_known_count": {
                            3: 3, 4: 4, 7: 5, 8: 6, 10: 7, 11: 8, 
                            13: 9, 14: 10, 16: 11, 19: 12, 20: 13
                        },
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
