"""
Subclass definitions for the Ranger class.
"""

RANGER_SUBCLASSES = {
    "beast_master": {
        "id": "beast_master",
        "name": "Beast Master",
        "description": "Beast Masters represent the ideal of the hunter and their loyal companion. By bonding with a primal beast, these rangers combine their own martial skill with the ferocity of the wild, creating a unified force that can strike from land, sea, or sky.",
        "features": {
            3: [
                {
                    "id": "beast_master_primal_companion",
                    "name": "Primal Companion",
                    "summary": "Summon a primal beast (Land, Sea, or Sky). Command it as a Bonus Action or by forgoing an attack.",
                    "description": "You magically summon a primal beast, which draws strength from your bond with nature. Choose its stat block: Beast of the Land, Beast of the Sea, or Beast of the Sky. You also determine the kind of animal it is, choosing a kind appropriate for the stat block. Whatever beast you choose, it bears primal markings indicating its supernatural origin. \n The beast is Friendly to you and your allies and obeys your commands. It vanishes if you die. \n The Beast in Combat. In combat, the beast acts during your turn. It can move and use its Reaction on its own, but the only action it takes is the Dodge action unless you take a Bonus Action to command it to take an action in its stat block or some other action. You can also sacrifice one of your attacks when you take the Attack action to command the beast to take the Beast's Strike action. If you have the Incapacitated condition, the beast acts on its own and isn't limited to the Dodge action. \n Restoring or Replacing the Beast. If the beast has died within the last hour, you can take a Magic action to touch it and expend a spell slot. The beast returns to life after 1 minute with all its Hit Points restored. \n Whenever you finish a Long Rest, you can summon a different primal beast, which appears in an unoccupied space within 5 feet of you. You choose its stat block and appearance. If you already have a beast from this feature, the old one vanishes when the new one appears.",
                    "details": {
                        "types": ["Beast of the Land", "Beast of the Sea", "Beast of the Sky"],
                        "command": "Bonus Action to command (or forgo 1 attack from Attack action for Beast's Strike)",
                        "combat": "Acts on your turn; Dodges unless commanded",
                        "revival": "Magic Action + Spell Slot (1 min casting time) if died within 1 hour",
                        "summons": "Change beast type/appearance on Long Rest"
                    }
                }
            ],
            7: [
                {
                    "id": "beast_master_exceptional_training",
                    "name": "Exceptional Training",
                    "summary": "Command beast as a BA to Dash, Disengage, Dodge, or Help. Beast can deal Force damage.",
                    "description": "When you take a Bonus Action to command your Primal Companion beast to take an action, you can also command it to take the Dash, Disengage, Dodge, or Help action using its Bonus Action. In addition, whenever it hits with an attack roll and deals damage, it can deal your choice of Force damage or its normal damage type.",
                    "details": {
                        "bonus_action_commands": ["Dash", "Disengage", "Dodge", "Help"],
                        "damage_type_choice": "Force or normal damage type on hit"
                    }
                }
            ],
            11: [
                {
                    "id": "beast_master_bestial_fury",
                    "name": "Bestial Fury",
                    "summary": "Beast's Strike can be used twice. Beast deals extra Force damage to Hunter's Mark targets.",
                    "description": "When you command your Primal Companion beast to take the Beast's Strike action, the beast can use it twice. In addition, the first time each turn it hits a creature under the effect of your Hunter's Mark spell, the beast deals extra Force damage equal to the bonus damage of that spell.",
                    "details": {
                        "beasts_strike_multiattack": "Beast uses Beast's Strike twice when commanded",
                        "hunters_mark_synergy": "Deals extra Force damage (equal to Hunter's Mark bonus) on first hit per turn vs marked target"
                    }
                }
            ],
            15: [
                {
                    "id": "beast_master_share_spell",
                    "name": "Share Spell",
                    "summary": "Spells targeting yourself also affect your companion within 30ft.",
                    "description": "When you cast a spell targeting yourself, you can also affect your Primal Companion beast with the spell if the beast is within 30 feet of you.",
                    "details": {
                        "range": "30ft",
                        "effect": "Any spell you cast targeting yourself affects both you and your beast"
                    }
                }
            ]
        }
    },
    "fey_wanderer": {
        "id": "fey_wanderer",
        "name": "Fey Wanderer",
        "description": "As a Fey Wanderer, you tread with one foot in the Mortal Realm and the other in the Fey Realm. You bring the joy and the terror of the Fey to your enemies and allies alike, wielding the power of your otherworldly charm and the sting of psychic trauma.",
        "features": {
            3: [
                {
                    "id": "fey_wanderer_spells",
                    "name": "Fey Wanderer Spells",
                    "summary": "You always have certain spells prepared as you gain levels in this class.",
                    "description": "When you reach a Ranger level specified in the Fey Wanderer Spells list, you thereafter always have the listed spells prepared. \n Lv3: Charm Person. \n Lv5: Misty Step. \n Lv9: Summon Fey. \n Lv13: Dimension Door. \n Lv17: Mislead. \n You also possess a fey blessing. Choose it from the Feywild Gifts list or determine it randomly. \n 1d6: \n 1 = Illusory butterflies flutter around you while you take a Short or Long Rest. \n 2 = Flowers bloom from your hair each dawn. \n 3 = You faintly smell of cinnamon, lavender, nutmeg, or another comforting herb or spice. \n 4 = Your shadow dances while no one is looking directly at it. \n 5 = Horns or antlers sprout from your head. \n 6 = Your skin and hair change color each dawn.",
                    "details": {
                        "spells": {
                            3: ["Charm Person"],
                            5: ["Misty Step"],
                            9: ["Summon Fey"],
                            13: ["Dimension Door"],
                            17: ["Mislead"]
                        },
                        "fey_gift": "You possess a fey blessing (e.g., illusory butterflies, dancing shadow, or antlers)."
                    }
                },
                {
                    "id": "fey_wanderer_dreadful_strike",
                    "name": "Dreadful Strike",
                    "summary": "Once per turn, deal extra Psychic damage (1d4, increases at lvl 11) on a weapon hit.",
                    "description": "You can augment your weapon strikes with mind-scarring magic drawn from the murky hollows of the Feywild. When you hit a creature with a weapon, you can deal an extra 1d4 Psychic damage to the target, which can take this extra damage only once per turn. The extra damage increases to 1d6 when you reach Ranger level 11.",
                    "details": {
                        "damage": "1d4 Psychic (increases to 1d6 at level 11)",
                        "limit": "Once per turn"
                    }
                },
                {
                    "id": "fey_wanderer_otherworldly_glamour",
                    "name": "Otherworldly Glamour",
                    "summary": "Gain a bonus to Charisma checks equal to Wisdom mod. Gain proficiency in one Charisma skill.",
                    "description": "Whenever you make a Charisma check, you gain a bonus to the check equal to your Wisdom modifier (minimum of +1). You also gain proficiency in one of these skills of your choice: Deception, Performance, or Persuasion.",
                    "details": {
                        "bonus": "Wisdom modifier (min +1) to all Charisma checks",
                        "skill_choice": ["Deception", "Performance", "Persuasion"]
                    }
                }
            ],
            7: [
                {
                    "id": "fey_wanderer_beguiling_twist",
                    "name": "Beguiling Twist",
                    "summary": "Advantage on saves vs Charm/Fear. Reaction: redirect a successful Charm/Fear save to a new target within 120ft.",
                    "description": "The magic of the Fey Realm guards your mind. You have Advantage on saving throws to avoid or end the Charmed or Frightened condition. In addition, whenever you or a creature you can see within 120 feet of you succeeds on a saving throw to avoid or end the Charmed or Frightened condition, you can take a Reaction to force a different creature you can see within 120 feet of yourself to make a Wisdom save against your spell save DC. On a failed save, the target is Charmed or Frightened (your choice) for 1 minute. The target repeats the save at the end of each of its turns, ending the effect on itself on a success.",
                    "details": {
                        "passive": "Advantage on saving throws to avoid or end Charmed or Frightened",
                        "action": "Reaction",
                        "trigger": "Creature within 120ft succeeds on a save vs Charms or Fear",
                        "effect": "Force a different creature (120ft) to make Wisdom save or be Charmed/Frightened for 1 min"
                    }
                }
            ],
            11: [
                {
                    "id": "fey_wanderer_fey_reinforcements",
                    "name": "Fey Reinforcements",
                    "summary": "Cast Summon Fey without components or once per Long Rest for free. Can remove concentration (1 min duration).",
                    "description": "You can cast Summon Fey without a Material component. You can also cast it once without a spell slot, and you regain the ability to cast it in this way when you finish a Long Rest. Whenever you start casting the spell, you can modify it so that it doesn't require Concentration. If you do so, the spell's duration becomes 1 minute for that casting.",
                    "details": {
                        "free_cast": "1/Long Rest without a spell slot",
                        "material_bypass": "No material components required",
                        "concentration_buff": "Can cast without Concentration (duration reduces to 1 minute)"
                    }
                }
            ],
            15: [
                {
                    "id": "fey_wanderer_misty_wanderer",
                    "name": "Misty Wanderer",
                    "summary": "Cast Misty Step for free (Wis mod/Long Rest) and bring a passenger.",
                    "description": "You can cast Misty Step without expending a spell slot. You can do so a number of times equal to your Wisdom modifier (minimum of once), and you regain all expended uses when you finish a Long Rest. In addition, whenever you cast Misty Step, you can bring along one willing creature you can see within 5 feet of yourself. That creature teleports to an unoccupied space of your choice within 5 feet of your destination space.",
                    "details": {
                        "free_casts": "Wisdom modifier (minimum 1)",
                        "recharge": "Long Rest",
                        "passenger": "Bring one willing creature within 5ft to an unoccupied space within 5ft of destination"
                    }
                }
            ]
        }
    },
    "gloom_stalker": {
        "id": "gloom_stalker",
        "name": "Gloom Stalker",
        "description": "Gloom Stalkers are at home in the darkest places: deep under the earth, in gloomy alleyways, and in primeval forests. Most people fear the dark, but a Gloom Stalker ventures into it with confidence, seeking to ambush threats before they can reach the light.",
        "features": {
            3: [
                {
                    "id": "gloom_stalker_spells",
                    "name": "Gloom Stalker Spells",
                    "summary": "You always have certain spells prepared as you gain levels in this class.",
                    "description": "When you reach a Ranger level specified in the Gloom Stalker Spells list, you thereafter always have the listed spells prepared. \n Lv3: Disguise Self. \n Lv5: Rope Trick. \n Lv9: Fear. \n Lv13: Greater Invisibility. \n Lv17: Seeming.",
                    "details": {
                        "spells": {
                            3: ["Disguise Self"],
                            5: ["Rope Trick"],
                            9: ["Fear"],
                            13: ["Greater Invisibility"],
                            17: ["Seeming"]
                        }
                    }
                },
                {
                    "id": "gloom_stalker_dread_ambusher",
                    "name": "Dread Ambusher",
                    "summary": "Combat start: +10ft Speed. Weapons deal +2d6 Psychic damage (once per turn, Wis mod/LR). Add Wis mod to Initiative.",
                    "description": "You have mastered the art of creating fearsome ambushes, granting you the following benefits. *-Ambusher's Leap-* At the start of your first turn of each combat, your Speed increases by 10 feet until the end of that turn. *-Dreadful Strike-* When you attack a creature and hit it with a weapon, you can deal an extra 2d6 Psychic damage. You can use this benefit only once per turn, you can use it a number of times equal to your Wisdom modifier (minimum of once), and you regain all expended uses when you finish a Long Rest. *-Initiative Bonus-* When you roll Initiative, you can add your Wisdom modifier to the roll.",
                    "details": {
                        "speed_boost": "+10ft Speed on first turn of combat",
                        "extra_damage": "2d6 Psychic (once per turn; increases to 2d8 at lvl 11)",
                        "damage_uses": "Wisdom modifier (minimum 1)",
                        "damage_recharge": "Long Rest",
                        "initiative_bonus": "Add Wisdom modifier to Initiative rolls"
                    }
                },
                {
                    "id": "gloom_stalker_umbral_sight",
                    "name": "Umbral Sight",
                    "summary": "Gain or increase Darkvision (60ft). You are Invisible to creatures using Darkvision in total darkness.",
                    "description": "You gain Darkvision with a range of 60 feet. If you already have Darkvision when you gain this feature, its range increases by 60 feet. You are also adept at evading creatures that rely on Darkvision. While entirely in Darkness, you have the Invisible condition to any creature that relies on Darkvision to see you in that Darkness.",
                    "details": {
                        "darkvision": "60ft (or +60ft if already possessed)",
                        "invisibility": "Invisible to any creature that relies on Darkvision to see you while in total darkness"
                    }
                }
            ],
            7: [
                {
                    "id": "gloom_stalker_iron_mind",
                    "name": "Iron Mind",
                    "summary": "Gain proficiency in Wisdom saving throws (or Int/Cha if already proficient).",
                    "description": "You have honed your ability to resist mind-altering powers. You gain proficiency in Wisdom saving throws. If you already have this proficiency, you instead gain proficiency in Intelligence or Charisma saving throws (your choice).",
                    "details": {
                        "proficiency": "Wisdom saving throws",
                        "alternative": "Intelligence or Charisma if already proficient in Wisdom"
                    }
                }
            ],
            11: [
                {
                    "id": "gloom_stalker_stalkers_flurry",
                    "name": "Stalker's Flurry",
                    "summary": "Dread Ambusher damage becomes 2d8. Dealing extra damage allows an extra attack or AoE Fear effect.",
                    "description": "The Psychic damage of your Dreadful Strike becomes 2d8. In addition, when you use the Dreadful Strike effect of your Dread Ambusher feature, you can cause one of the following additional effects. *-Sudden Strike-* You can make another attack with the same weapon against a different creature that is within 5 feet of the original target and that is within the weapon's range. *-Mass Fear-* The target and each creature within 10 feet of it must make a Wisdom saving throw against your spell save DC. On a failed save, a creature has the Frightened condition until the start of your next turn.",
                    "details": {
                        "damage_upgrade": "Dread Ambusher extra damage becomes 2d8",
                        "flurry_options": [
                            "Make an extra attack vs a different creature within 5ft of target",
                            "Wisdom save (120ft) or Frightened for all creatures within 10ft of target"
                        ]
                    }
                }
            ],
            15: [
                {
                    "id": "gloom_stalker_shadowy_dodge",
                    "name": "Shadowy Dodge",
                    "summary": "Reaction: impose Disadvantage on an attack against you and teleport 30ft.",
                    "description": "When a creature makes an attack roll against you, you can take a Reaction to impose Disadvantage on that roll. Whether the attack hits or misses, you can then teleport up to 30 feet to an unoccupied space you can see.",
                    "details": {
                        "action": "Reaction",
                        "trigger": "Creature makes an attack roll against you",
                        "effect": "Impose Disadvantage on the roll; teleport up to 30ft to an unoccupied space"
                    }
                }
            ]
        }
    },
    "hunter": {
        "id": "hunter",
        "name": "Hunter",
        "description": "Emulating the Hunter archetype means accepting your role as the bulwark between civilization and the terrors of the wilderness. As you walk the Hunter's path, you learn specialized techniques for fighting the threats you face, from raging ogres and hordes of orcs to towering giants and terrifying dragons.",
        "features": {
            3: [
                {
                    "id": "hunter_lore",
                    "name": "Hunter's Lore",
                    "summary": "While a creature is marked by your Hunter's Mark, you know its Immunities, Resistances, and Vulnerabilities.",
                    "description": "You can call on the forces of nature to reveal certain strengths and weaknesses of your prey. While a creature is marked by your Hunter's Mark, you know whether that creature has any Immunities, Resistances, or Vulnerabilities, and if the creature has any, you know what they are.",
                    "details": {
                        "condition": "Target must be marked by Hunter's Mark",
                        "information": "Immunities, Resistances, and Vulnerabilities revealed"
                    }
                },
                {
                    "id": "hunter_prey",
                    "name": "Hunter's Prey",
                    "summary": "Choose Colossus Slayer (+1d8 dmg to wounded) or Horde Breaker (extra attack). Replace on Short/Long Rest.",
                    "description": "You gain one of the following feature options of your choice. Whenever you finish a Short or Long Rest, you can replace the chosen option with the other one. *-Colossus Slayer-* Your tenacity can wear down even the most resilient foes. When you hit a creature with a weapon, the weapon deals an extra 1d8 damage to the target if it's missing any of its Hit Points. You can deal this extra damage only once per turn. *-Horde Breaker-* Once on each of your turns when you make an attack with a weapon, you can make another attack with the same weapon against a different creature that is within 5 feet of the original target, that is within the weapon's range, and that you haven't attacked this turn.",
                    "details": {
                        "options": {
                            "colossus_slayer": "Extra 1d8 damage on weapon hit if target is missing HP (once per turn)",
                            "horde_breaker": "Once per turn: make an extra weapon attack against a different creature within 5ft of original target"
                        },
                        "special": "Can swap option on Short or Long Rest"
                    }
                }
            ],
            7: [
                {
                    "id": "hunter_defensive_tactics",
                    "name": "Defensive Tactics",
                    "summary": "Choose Escape the Horde (OAs have Disadvantange) or Multiattack Defense (AC bonus vs same attacker). Replace on Short/Long Rest.",
                    "description": "You gain one of the following feature options of your choice. Whenever you finish a Short or Long Rest, you can replace the chosen option with the other one. *-Escape the Horde-* Opportunity Attacks have Disadvantage against you. *-Multiattack Defense-* When a creature hits you with an attack roll, that creature has Disadvantage on all other attack rolls against you this turn.",
                    "details": {
                        "options": {
                            "escape_the_horde": "Opportunity Attacks have Disadvantage against you",
                            "multiattack_defense": "When hit, the attacker has Disadvantage on all other attacks against you this turn"
                        },
                        "special": "Can swap option on Short or Long Rest"
                    }
                }
            ],
            11: [
                {
                    "id": "hunter_superior_hunters_prey",
                    "name": "Superior Hunter's Prey",
                    "summary": "Once per turn, deal Hunter's Mark extra damage to a second creature within 30ft of the first damaged target.",
                    "description": "Once per turn when you deal damage to a creature marked by your Hunter's Mark, you can also deal that spell's extra damage to a different creature that you can see within 30 feet of the first creature.",
                    "details": {
                        "trigger": "Deal damage to a creature marked by Hunter's Mark",
                        "effect": "Deal that spell's extra damage to a different creature within 30ft"
                    }
                }
            ],
            15: [
                {
                    "id": "hunter_superior_hunters_defense",
                    "name": "Superior Hunter's Defense",
                    "summary": "Reaction: gain Resistance to an incoming damage type until the end of the turn.",
                    "description": "When you take damage, you can take a Reaction to give yourself Resistance to that damage and any other damage of the same type until the end of the current turn.",
                    "details": {
                        "action": "Reaction",
                        "trigger": "Take damage",
                        "effect": "Gain Resistance to that damage type (and all instances of it) until the end of the current turn"
                    }
                }
            ]
        }
    }
}
