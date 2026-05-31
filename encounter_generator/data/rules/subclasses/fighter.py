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
                    "description": "Your experience on the battlefield has refined your fighting techniques. You learn maneuvers that are fueled by special dice called Superiority Dice. \n Maneuvers. You learn three maneuvers of your choice from the Maneuvers Options. Many maneuvers enhance an attack in some way. You can use only one maneuver per attack. You learn two additional maneuvers of your choice when you reach Fighter levels 7, 10, and 15. Each time you learn new maneuvers, you can also replace one maneuver you know with a different one. \n Superiority Dice. You have four Superiority Dice, which are d8s. A Superiority Die is expended when you use it. You regain all expended Superiority Dice when you finish a Short or Long Rest. You gain an additional Superiority Die when you reach Fighter levels 7 (five dice total) and 15 (six dice total). \n Saving Throws. If a maneuver requires a saving throw, the DC equals 8 plus your Strength or Dexterity modifier (your choice) and Proficiency Bonus.",
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
                    "description": "You gain proficiency with one type of Artisan's Tools of your choice, and you gain proficiency in one skill of your choice from the skills available to Fighters at level 1.",
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
                    "description": "As a Bonus Action, you can discern certain strengths and weaknesses of a creature you can see within 30 feet of yourself; you know whether that creature has any Immunities, Resistances, or Vulnerabilities, and if the creature has any, you know what they are. Once you use this feature, you can't do so again until you finish a Long Rest. You can also restore a use of the feature by expending one Superiority Die (no action required).",
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
                    "summary": "Superiority Die gets bigger.",
                    "description": "Your Superiority Die becomes a d10.",
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
                    "description": "Once per turn, when you use a maneuver, you can roll 1d8 and use the number rolled instead of expending a Superiority Die.",
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
                    "summary": "Your Superiority Die gets bigger.",
                    "description": "Your Superiority Die becomes a d12.",
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
                    "description": "Your attack rolls with weapons and Unarmed Strikes can score a Critical Hit on a roll of 19 or 20 on the d20.",
                    "details": {
                        "critical_range": [19, 20]
                    }
                },
                {
                    "id": "champion_remarkable_athlete",
                    "name": "Remarkable Athlete",
                    "summary": "Gain Advantage on Initiative and Athletics checks; move half speed without opportunity attacks after a crit.",
                    "description": "Thanks to your athleticism, you have Advantage on Initiative rolls and Strength (Athletics) checks. In addition, immediately after you score a Critical Hit, you can move up to half your Speed without provoking Opportunity Attacks.",
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
                    "summary": "Gain another Fighting Style feat.",
                    "description": "You gain another Fighting Style feat of your choice.",
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
                    "description": "The thrill of battle drives you toward victory. During combat, you can give yourself Heroic Inspiration whenever you start your turn without it.",
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
                    "description": "Your attack rolls with weapons and Unarmed Strikes can now score a Critical Hit on a roll of 18–20 on the d20.",
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
                    "description": "You attain the pinnacle of resilience in battle, giving you these benefits. \n Defy Death. You have Advantage on Death Saving Throws. Moreover, when you roll 18–20 on a Death Saving Throw, you gain the benefit of rolling a 20 on it. \n Heroic Rally. At the start of each of your turns, you regain Hit Points equal to 5 plus your Constitution modifier if you are Bloodied and have at least 1 Hit Point.",
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
                    "description": "You have learned to cast spells. \n Cantrips. You know two cantrips of your choice from the Wizard spell list. Whenever you gain a Fighter level, you can replace one of these cantrips with another cantrip of your choice from the Wizard spell list. When you reach Fighter level 10, you learn another Wizard cantrip of your choice. \n Spell Slots. The Spellcasting window that should now be present within your Character Sheet shows how many spell slots you have to cast your level 1+ spells. You regain all expended slots when you finish a Long Rest. \n Prepared Spells of Level 1+. You prepare the list of level 1+ spells that are available for you to cast with this feature. To start, choose three level 1 spells from the Wizard spell list. The number of spells on your list increases as you gain Fighter levels, as shown in the Spellcasting window. Whenever that number increases, choose additional spells from the Wizard spell list. The chosen spells must be of a level for which you have spell slots. \n Changing your Prepared Spells. Whenever you gain a Fighter level, you can replace one spell on your list with another Wizard spell for which you have spell slots. \n Spellcasting Ability. Intelligence is your spellcasting ability for your Wizard spells. \n Spellcasting Focus. You can use an Arcane Focus as a Spellcasting Focus for your Wizard spells.",
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
                    "description": "You learn a ritual that creates a magical bond between yourself and one weapon. You perform the ritual over the course of 1 hour, which can be done during a Short Rest. The weapon must be within your reach throughout the ritual, at the conclusion of which you touch the weapon and forge the bond. The bond fails if another Fighter is bonded to the weapon or if the weapon is a magic item to which someone else is attuned. \n Once you have bonded a weapon to yourself, you can't be disarmed of that weapon unless you have the Incapacitated condition. If it is on the same plane of existence, you can summon that weapon as a Bonus Action, causing it to teleport instantly to your hand. \n You can have up to two bonded weapons, but you can summon only one at a time with a Bonus Action. If you attempt to bond with a third weapon, you must break the bond with one of the other two.",
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
                    "description": "When you take the Attack action on your turn, you can replace one of the attacks with a casting of one of your Wizard cantrips that has a casting time of an action.",
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
                    "description": "You learn how to make your weapon strikes undercut a creature's ability to withstand your spells. When you hit a creature with an attack using a weapon, that creature has Disadvantage on the next saving throw it makes against a spell you cast before the end of your next turn.",
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
                    "description": "When you use your Action Surge, you can teleport up to 30 feet to an unoccupied space you can see. You can teleport before or after the additional action.",
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
                    "description": "When you take the Attack action on your turn, you can replace two of the attacks with a casting of one of your level 1 or level 2 Wizard spells that has a casting time of an action.",
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
                    "description": "You harbor a wellspring of psionic energy within yourself. It is represented by your Psionic Energy Dice, which fuel powers you have from this subclass. \n Lv3: 4D6. \n Lv5: 6D8. \n Lv9: 8D8. \n Lv11: 8D10. \n Lv13: 10D10. \n Lv17: 12D12. Any features in this subclass that use a Psionic Energy Die use only the dice from this subclass. Some of your powers expend the Psionic Energy Die, as specified in a power's description, and you can't use a power if it requires you to use a die when all your Psionic Energy Dice are expended. \n You regain one of your expended Psionic Energy Dice when you finish a Short Rest, and you regain all of them when you finish a Long Rest. \n *-Protective Field-* When you or another creature you can see within 30 feet of you takes damage, you can take a Reaction to expend one Psionic Energy Die, roll the die, and reduce the damage taken by the number rolled plus your Intelligence modifier (minimum reduction of 1), as you create a momentary shield of telekinetic force. \n *-Psionic Strike-* You can propel your weapons with psionic force. Once on each of your turns, immediately after you hit a target within 30 feet of yourself with an attack and deal damage to it with a weapon, you can expend one Psionic Energy Die, rolling it and dealing Force damage to the target equal to the number rolled plus your Intelligence modifier. \n *-Telekinetic Movement-* You can move an object or a creature with your mind. As a Magic action, choose one target you can see within 30 feet of yourself; the target must be a loose object that is Large or smaller or one willing creature other than you. You transport the target up to 30 feet to an unoccupied space you can see. Alternatively, if the target is a Tiny object, you can transport it to or from your hand. \n Once you take this action, you can't do so again until you finish a Short or Long Rest unless you expend a Psionic Energy Die (no action required) to restore your use of it.",
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
                    "description": "You have mastered new ways to use your telekinetic abilities, detailed below. \n *-Psi-Powered Leap-* As a Bonus Action, you gain a Fly Speed equal to twice your Speed until the end of the current turn. Once you take this Bonus Action, you can't do so again until you finish a Short or Long Rest unless you expend a Psionic Energy Die (no action required) to restore your use of it. \n *-Telekinetic Thrust-* When you deal damage to a target with your Psionic Strike, you can force the target to make a Strength saving throw (DC 8 plus your Intelligence modifier and Proficiency Bonus). On a failed save, you can give the target the Prone condition or transport it up to 10 feet horizontally.",
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
                    "description": "You have Resistance to Psychic damage. Moreover, if you start your turn with the Charmed or Frightened condition, you can expend a Psionic Energy Die (no action required) and end every effect on yourself giving you those conditions.",
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
                    "description": "You can shield yourself and others with telekinetic force. As a Bonus Action, you can choose creatures, including yourself, within 30 feet of yourself, up to a number of creatures equal to your Intelligence modifier (minimum of one creature). Each of the chosen creatures has Half Cover for 1 minute or until you have the Incapacitated condition. Once you use this feature, you can't do so again until you finish a Long Rest unless you expend a Psionic Energy Die (no action required) to restore your use of it.",
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
                    "description": "You always have the Telekinesis spell prepared. With this feature, you can cast it without a spell slot or components, and your spellcasting ability for it is Intelligence. On each of your turns while you maintain Concentration on it, including the turn when you cast it, you can make one attack with a weapon as a Bonus Action. Once you cast the spell with this feature, you can't do so in this way again until you finish a Long Rest unless you expend a Psionic Energy Die (no action required) to restore your use of it.",
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
