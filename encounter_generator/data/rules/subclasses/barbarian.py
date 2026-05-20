"""
Subclass definitions for the Barbarian class.
"""

BARBARIAN_SUBCLASSES = {
    "berserker": {
        "id": "berserker",
        "name": "Path Of The Berserker",
        "description": "For some barbarians, rage is a means to an end—that end being violence. The Path of the Berserker is a path of untamed fury, slick with blood. As you enter the berserker's rage, you thrill in the chaos of battle, heedless of your own health or well-being.",
        "features": {
            3: [
                {
                    "id": "berserker_frenzy",
                    "name": "Frenzy",
                    "summary": "Deal extra d6s of damage (equal to Rage Bonus) on your first Reckless Attack hit each turn.",
                    "description": "If you use Reckless Attack while your Rage is active, you deal extra damage to the first target you hit on your turn with a Strength-based attack. To determine the extra damage, roll a number of d6s equal to your Rage Damage bonus, and add them together. The damage has the same type as the weapon or Unarmed Strike used for the attack.",
                    "details": {
                        "damage_die": "d6",
                        "die_count": "Rage Bonus",
                        "restriction": "First hit on turn, must use Reckless Attack while Raging"
                    }
                }
            ],
            6: [
                {
                    "id": "berserker_mindless_rage",
                    "name": "Mindless Rage",
                    "summary": "Immunity to Charmed and Frightened conditions while Raging; ends existing effects upon entering Rage.",
                    "description": "You have Immunity to the Charmed and Frightened conditions while your Rage is active. If you're Charmed or Frightened when you enter your Rage, the condition ends on you.",
                }
            ],
            10: [
                {
                    "id": "berserker_retaliation",
                    "name": "Retaliation",
                    "summary": "Use a Reaction to make a melee attack against a creature within 5ft that deals damage to you.",
                    "description": "When you take damage from a creature that is within 5 feet of you, you can take a Reaction to make one melee attack against that creature, using a weapon or an Unarmed Strike.",
                }
            ],
            14: [
                {
                    "id": "berserker_intimidating_presence",
                    "name": "Intimidating Presence",
                    "summary": "Bonus Action to Frighten creatures in a 30ft Emanation (WIS save); can recharge by expending a Rage use.",
                    "description": "As a Bonus Action, you can strike terror into others with your menacing presence and primal power. When you do so, each creature of your choice in a 30-foot Emanation originating from you must make a Wisdom saving throw (DC 8 plus your Strength modifier and Proficiency Bonus). On a failed save, a creature has the Frightened condition for 1 minute. At the end of each of the Frightened creature's turns, the creature repeats the save, ending the effect on itself on a success. Once you use this feature, you can't use it again until you finish a Long Rest unless you expend a use of your Rage (no action required) to restore your use of it.",
                    "details": {
                        "action": "Bonus Action",
                        "area": "30ft Emanation",
                        "save_dc": "8 + STR mod + Proficiency Bonus",
                        "recharge": "Long Rest or expend one Rage use"
                    }
                }
            ]
        }
    },
    "wild_heart": {
        "id": "wild_heart",
        "name": "Path Of The Wild Heart",
        "description": "The Path of the Wild Heart is a journey that brings a barbarian into spiritual kinship with the natural world. Your rage is not just fury; it is a primal connection to the animal spirits that guide and protect you.",
        "features": {
            3: [
                {
                    "id": "wild_heart_animal_speaker",
                    "name": "Animal Speaker",
                    "summary": "Cast Beast Sense and Speak with Animals as Rituals using Wisdom.",
                    "description": "You can cast the Beast Sense and Speak with Animals spells but only as Rituals. Wisdom is your spellcasting ability for them.",
                    "details": {
                        "spells": ["Beast Sense", "Speak with Animals"],
                        "casting_mode": "Ritual only",
                        "ability": "Wisdom"
                    }
                },
                {
                    "id": "wild_heart_rage_of_the_wilds",
                    "name": "Rage of the Wilds",
                    "summary": "Choose an animal spirit benefit whenever you activate your Rage.",
                    "description": "Your Rage taps into the primal power of animals. Whenever you activate your Rage, you gain one of the following options of your choice. \n *Bear*. While your Rage is active, you have Resistance to every damage type except Force, Necrotic, Psychic, and Radiant. \n *Eagle*. When you activate your Rage, you can take the Disengage and Dash actions as part of that Bonus Action. While your Rage is active, you can take a Bonus Action to take both of those actions. \n *Wolf*. While your Rage is active, your allies have Advantage on attack rolls against any enemy of yours within 5 feet of you.",
                    "details": {
                        "options": {
                            "Bear": "Resistance to all damage types except Force, Necrotic, Psychic, and Radiant.",
                            "Eagle": "Dash and Disengage as part of the Bonus Action used to Rage; can take both as a Bonus Action while Raging.",
                            "Wolf": "Allies have Advantage on attack rolls against enemies within 5ft of you."
                        }
                    }
                }
            ],
            6: [
                {
                    "id": "wild_heart_aspect_of_the_wilds",
                    "name": "Aspect of the Wilds",
                    "summary": "Gain a permanent animal aspect, swappable on a Long Rest.",
                    "description": "You gain one of the following options of your choice. Whenever you finish a Long Rest, you can change your choice. \n *Owl*. You have Darkvision with a range of 60 feet. If you already have Darkvision, its range increases by 60 feet. \n *Panther*. You have a Climb Speed equal to your Speed. \n *Salmon*. You have a Swim Speed equal to your Speed.",
                    "details": {
                        "options": {
                            "Owl": "Gain 60ft Darkvision (or +60ft if you already have it).",
                            "Panther": "Gain a Climb Speed equal to your Speed.",
                            "Salmon": "Gain a Swim Speed equal to your Speed."
                        },
                        "recharge": "Long Rest (to swap)"
                    }
                }
            ],
            10: [
                {
                    "id": "wild_heart_nature_speaker",
                    "name": "Nature Speaker",
                    "summary": "Cast Commune with Nature as a Ritual using Wisdom.",
                    "description": "You can cast the Commune with Nature spell but only as a Ritual. Wisdom is your spellcasting ability for it.",
                    "details": {
                        "spells": ["Commune with Nature"],
                        "casting_mode": "Ritual only",
                        "ability": "Wisdom"
                    }
                }
            ],
            14: [
                {
                    "id": "wild_heart_power_of_the_wilds",
                    "name": "Power of the Wilds",
                    "summary": "Gain an advanced animal spirit benefit whenever you activate your Rage.",
                    "description": "Whenever you activate your Rage, you gain one of the following options of your choice. \n *Falcon*. While your Rage is active, you have a Fly Speed equal to your Speed if you aren't wearing any armor. \n *Lion*. While your Rage is active, any of your enemies within 5 feet of you have Disadvantage on attack rolls against targets other than you or another Barbarian who has this option active. \n *Ram*. While your Rage is active, you can cause a Large or smaller creature to have the Prone condition when you hit it with a melee attack.",
                    "details": {
                        "options": {
                            "Falcon": "Gain a Fly Speed equal to your Speed while unarmored.",
                            "Lion": "Enemies within 5ft have Disadvantage vs targets other than you or another Wild Heart Barbarian.",
                            "Ram": "Melee hits can knock Large or smaller creatures Prone."
                        }
                    }
                }
            ]
        }
    },
    "world_tree": {
        "id": "world_tree",
        "name": "Path Of The World Tree",
        "description": "Barbarians who follow the Path of the World Tree draw their power from the cosmic ash that connects the planes. Your rage is a manifesting of the tree's eternal vitality, allowing you to shield allies with spectral roots and traverse the multiverse through its ethereal branches.",
        "features": {
            3: [
                {
                    "id": "world_tree_vitality",
                    "name": "Vitality Of The Tree",
                    "summary": "Gain Temp HP on Rage; grant Temp HP to allies within 10ft at the start of each turn.",
                    "description": "Your Rage taps into the life force of the World Tree. You gain the following benefits. \n *Vitality Surge*. When you activate your Rage, you gain a number of Temporary Hit Points equal to your Barbarian level. \n *Life-Giving Force*. At the start of each of your turns while your Rage is active, you can choose another creature within 10 feet of yourself to gain Temporary Hit Points. To determine the number of Temporary Hit Points, roll a number of d6s equal to your Rage Damage bonus, and add them together. If any of these Temporary Hit Points remain when your Rage ends, they vanish.",
                    "details": {
                        "on_rage": "Gain Temp HP equal to Barbarian level",
                        "turn_start": {
                            "target": "Another creature within 10ft",
                            "amount": "Rage Damage bonus in d6s"
                        },
                        "restriction": "Temp HP vanishes when Rage ends"
                    }
                }
            ],
            6: [
                {
                    "id": "world_tree_branches",
                    "name": "Branches Of The Tree",
                    "summary": "Reaction to teleport a creature starting its turn within 30ft to a space within 5ft of you (STR save).",
                    "description": "Whenever a creature you can see starts its turn within 30 feet of you while your Rage is active, you can take a Reaction to summon spectral branches of the World Tree around it. The target must succeed on a Strength saving throw (DC 8 plus your Strength modifier and Proficiency Bonus) or be teleported to an unoccupied space you can see within 5 feet of yourself or in the nearest unoccupied space you can see. After the target teleports, you can reduce its Speed to 0 until the end of the current turn.",
                    "details": {
                        "action": "Reaction",
                        "range": "30ft",
                        "save_dc": "8 + STR mod + Proficiency Bonus",
                        "effect": "Teleport to unoccupied space within 5ft of you; can reduce speed to 0"
                    }
                }
            ],
            10: [
                {
                    "id": "world_tree_battering_roots",
                    "name": "Battering Roots",
                    "summary": "+10ft reach with Heavy/Versatile weapons; can use Push/Topple mastery in addition to another.",
                    "description": "During your turn, your reach is 10 feet greater with any Melee weapon that has the Heavy or Versatile property, as tendrils of the World Tree extend from you. When you hit with such a weapon on your turn, you can activate the Push or Topple mastery property in addition to a different mastery property you're using with that weapon.",
                    "details": {
                        "reach_bonus": "+10ft (Heavy/Versatile weapons)",
                        "mastery_bonus": "Activate Push or Topple in addition to another property"
                    }
                }
            ],
            14: [
                {
                    "id": "world_tree_travel",
                    "name": "Travel Along The Tree",
                    "summary": "Teleport up to 60ft as a Bonus Action while Raging; once per Rage, teleport 150ft with up to 6 allies.",
                    "description": "When you activate your Rage and as a Bonus Action while your Rage is active, you can teleport up to 60 feet to an unoccupied space you can see. In addition, once per Rage, you can increase the range of that teleport to 150 feet. When you do so, you can also bring up to six willing creatures who are within 10 feet of you. Each creature teleports to an unoccupied space of your choice within 10 feet of your destination space.",
                    "details": {
                        "action": "Bonus Action",
                        "standard_range": "60ft",
                        "extended_range": {
                            "uses": "Once per Rage",
                            "distance": "150ft",
                            "allies": "Up to 6 willing creatures within 10ft"
                        }
                    }
                }
            ]
        }
    },
    "zealot": {
        "id": "zealot",
        "name": "Path Of The Zealot",
        "description": "Some barbarians are chosen by gods to serve as divine instruments of destruction. The Path of the Zealot is a burning flame of faith that fuels your rage, granting you divine power to strike down foes and the resilience to transcend death itself.",
        "features": {
            3: [
                {
                    "id": "zealot_divine_fury",
                    "name": "Divine Fury",
                    "summary": "First hit while Raging deals extra 1d6 + half level damage (Radiant/Necrotic).",
                    "description": "You can channel divine power into your strikes. On each of your turns while your Rage is active, the first creature you hit with a weapon or an Unarmed Strike takes extra damage equal to 1d6 plus half your Barbarian level (round down). The extra damage is Necrotic or Radiant; you choose the type each time you deal the damage.",
                    "details": {
                        "damage_die": "1d6",
                        "modifier": "Barbarian Level / 2 (round down)",
                        "damage_types": ["Radiant", "Necrotic"],
                        "restriction": "Once per turn, while Raging"
                    }
                },
                {
                    "id": "zealot_warrior_of_the_gods",
                    "name": "Warrior Of The Gods",
                    "summary": "Pool of d12s to heal yourself as a Bonus Action.",
                    "description": "A divine entity helps ensure you can continue the fight. You have a pool of four d12s that you can spend to heal yourself. As a Bonus Action, you can expend dice from the pool, roll them, and regain a number of Hit Points equal to the roll's total. Your pool regains all expended dice when you finish a Long Rest. The pool's maximum number of dice increases by one when you reach Barbarian levels 6 (5 dice), 12 (6 dice), and 17 (7 dice).",
                    "details": {
                        "heal_die": "d12",
                        "pool_size": {
                            "type": "level-based",
                            "scaling": {
                                "3-5": 4,
                                "6-11": 5,
                                "12-16": 6,
                                "17-20": 7
                            }
                        },
                        "recharge": "Long Rest"
                    }
                }
            ],
            6: [
                {
                    "id": "zealot_fanatical_focus",
                    "name": "Fanatical Focus",
                    "summary": "Once per Rage, reroll a failed save with a bonus equal to your Rage Bonus.",
                    "description": "Once per active Rage, if you fail a saving throw, you can reroll it with a bonus equal to your Rage Damage bonus, and you must use the new roll.",
                    "details": {
                        "uses": "Once per active Rage",
                        "bonus": "Rage Damage bonus"
                    }
                }
            ],
            10: [
                {
                    "id": "zealot_zealous_presence",
                    "name": "Zealous Presence",
                    "summary": "Bonus Action to grant Advantage on attacks/saves to 10 allies within 60ft until next turn.",
                    "description": "As a Bonus Action, you unleash a battle cry infused with divine energy. Up to ten other creatures of your choice within 60 feet of you gain Advantage on attack rolls and saving throws until the start of your next turn. Once you use this feature, you can't use it again until you finish a Long Rest unless you expend a use of your Rage (no action required) to restore your use of it.",
                    "details": {
                        "action": "Bonus Action",
                        "range": "60ft",
                        "targets": "Up to 10 other creatures",
                        "recharge": "Long Rest or expend one Rage use"
                    }
                }
            ],
            14: [
                {
                    "id": "zealot_rage_of_the_gods",
                    "name": "Rage Of The Gods",
                    "summary": "Assume a divine warrior form (Fly/Hover, resistances); expend Rage as Reaction to prevent 0 HP.",
                    "description": "When you activate your Rage, you can assume the form of a divine warrior. This form lasts for 1 minute or until you drop to 0 Hit Points. Once you use this feature, you can't do so again until you finish a Long Rest. While in this form, you gain the benefits below. \n *Flight*. You have a Fly Speed equal to your Speed and can hover. \n *Resistance*. You have Resistance to Necrotic, Psychic, and Radiant damage. \n *Revivification*. When a creature within 30 feet of you would drop to 0 Hit Points, you can take a Reaction to expend a use of your Rage to instead change the target's Hit Points to a number equal to your Barbarian level.",
                    "details": {
                        "form_benefits": {
                            "speed": "Fly Speed (equal to Speed), can Hover",
                            "resistance": ["Necrotic", "Psychic", "Radiant"],
                            "duration": "1 minute or until 0 HP"
                        },
                        "death_prevention": {
                            "action": "Reaction",
                            "range": "30ft",
                            "cost": "Expend one Rage use",
                            "effect": "Target HP becomes equal to your Barbarian level instead of 0"
                        },
                        "recharge": "Long Rest"
                    }
                }
            ]
        }
    }
}
