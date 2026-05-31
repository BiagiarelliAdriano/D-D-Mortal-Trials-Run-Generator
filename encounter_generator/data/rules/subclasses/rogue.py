"""
Subclass definitions for the Rogue class.
"""

from encounter_generator.data.rules.spell_tables import THIRD_CASTER_PREPARED

ROGUE_SUBCLASSES = {
    "arcane_trickster": {
        "id": "arcane_trickster",
        "name": "Arcane Trickster",
        "description": "Arcane Tricksters combine their fundamental rogue skills with a study of wizardry. They use their magic to enhance their stealth and agility, becoming experts at both mundane and magical deception.",
        "features": {
            3: [
                {
                    "id": "arcane_trickster_spellcasting",
                    "name": "Spellcasting",
                    "summary": "Cast Wizard spells using Intelligence. Use an Arcane Focus and unique Mage Hand abilities.",
                    "description": "You have learned to cast spells. \n *-Cantrips-* You know three cantrips: Mage Hand and two other cantrips of your choice from the Wizard spell list. Whenever you gain a Rogue level, you can replace one of your cantrips, except Mage Hand, with another Wizard cantrip of your choice. When you reach Rogue level 10, you learn another Wizard cantrip of your choice. \n *-Spell Slots-* The Spellcasting window that should now be present within your Character Sheet shows how many spell slots you have to cast your level 1+ spells. You regain all expended spell slots when you finish a Long Rest. \n *-Prepared Spells of 1st+ Level-* You prepare the list of level 1+ spells that are available for you to cast with this feature. To start, choose three level 1 Wizard spells. The number of spells on your list increases as you gain Rogue levels, as shown in the Spellcasting window. Whenever that number increases, choose additional Wizard spells until the number of spells on your list matches the number in the Spellcasting window. The chosen spells must be of a level for which you have spell slots. \n *-Changing Your Prepared Spells-* Whenever you gain a Rogue level, you can replace one spell on your list with another Wizard spell for which you have spell slots. \n *-Spellcasting Ability-* Intelligence is your spellcasting ability for your Wizard spells. \n *-Spellcasting Focus-* You can use an Arcane Focus as a Spellcasting Focus for your Wizard spells.",
                    "details": {
                        "ability": "Intelligence",
                        "progression": "third",
                        "cantrips_known": {3: 3, 10: 4},
                        "mage_hand_requirement": "One cantrip must be Mage Hand",
                        "spells_prepared_scaling": THIRD_CASTER_PREPARED,
                        "spell_list": "Wizard",
                        "focus": "Arcane Focus"
                    }
                },
                {
                    "id": "arcane_trickster_mage_hand_legerdemain",
                    "name": "Mage Hand Legerdemain",
                    "summary": "Mage Hand is Invisible and can be cast/controlled as a Bonus Action. Can perform Sleight of Hand.",
                    "description": "When you cast Mage Hand, you can cast it as a Bonus Action, and you can make the spectral hand Invisible. You can control the hand as a Bonus Action, and through it, you can make Dexterity (Sleight of Hand) checks.",
                    "details": {
                        "cast_action": "Bonus Action",
                        "control_action": "Bonus Action",
                        "special": "Hand is Invisible; can perform Dexterity (Sleight of Hand) checks through the hand"
                    }
                }
            ],
            9: [
                {
                    "id": "arcane_trickster_magical_ambush",
                    "name": "Magical Ambush",
                    "summary": "While Invisible, enemies have Disadvantage on saves against your spells.",
                    "description": "If you have the Invisible condition when you cast a spell on a creature, it has Disadvantage on any saving throw it makes against the spell on the same turn.",
                    "details": {
                        "condition": "You have the Invisible condition",
                        "effect": "Target has Disadvantage on the saving throw against your spell cast this turn"
                    }
                }
            ],
            13: [
                {
                    "id": "arcane_trickster_versatile_trickster",
                    "name": "Versatile Trickster",
                    "summary": "Use Trip option of Cunning Strike on a second creature within 5ft of Mage Hand.",
                    "description": "You gain the ability to distract targets with your Mage Hand. When you use the Trip option of your Cunning Strike on a creature, you can also use that option on another creature within 5 feet of the spectral hand.",
                    "details": {
                        "synergy": "Cunning Strike (Trip)",
                        "effect": "Apply Trip to an additional creature within 5ft of your spectral hand"
                    }
                }
            ],
            17: [
                {
                    "id": "arcane_trickster_spell_thief",
                    "name": "Spell Thief",
                    "summary": "Reaction: negate a spell targeting you and steal it for 8 hours (Wis save).",
                    "description": "You gain the ability to magically steal the knowledge of how to cast a spell from another spellcaster. Immediately after a creature casts a spell that targets you or includes you in its area of effect, you can take a Reaction to force the creature to make an Intelligence saving throw. The DC equals your spell save DC. On a failed save, you negate the spell's effect against you, and you steal the knowledge of the spell if it is at least level 1 and of a level you can cast (it doesn't need to be a Wizard spell). For the next 8 hours, you have the spell prepared. The creature can't cast it until the 8 hours have passed. Once you steal a spell with this feature, you can't use this feature again until you finish a Long Rest.",
                    "details": {
                        "action": "Reaction",
                        "trigger": "Creature casts a spell targeting you or including you in area",
                        "save": "Intelligence vs your spell DC",
                        "effect": "Negate spell effect against you; if Lvl 1+ and castable by you, you prepare it for 8 hours",
                        "recharge": "Long Rest",
                        "restriction": "Original caster cannot cast the stolen spell for 8 hours"
                    }
                }
            ]
        }
    },
    "assassin": {
        "id": "assassin",
        "name": "Assassin",
        "description": "You focus your training on the grim art of death. Those who adhere to this archetype are diverse: hired killers, spies, bounty hunters, and even specially anointed priests trained to exterminate the enemies of their deity. Stealth, poison, and disguise help you eliminate your foes with deadly efficiency.",
        "features": {
            3: [
                {
                    "id": "assassin_assassinate",
                    "name": "Assassinate",
                    "summary": "Advantage on Initiative and first-round attacks vs those who haven't acted. Extra Sneak Attack damage (Rogue level) in round 1.",
                    "description": "You're adept at ambushing a target, granting you the following benefits. \n *-Initiative-* You have Advantage on Initiative rolls. *-Surprising Strikes-* During the first round of each combat, you have Advantage on attack rolls against any creature that hasn't taken a turn. If your Sneak Attack hits any target during that round, the target takes extra damage of the weapon's type equal to your Rogue level.",
                    "details": {
                        "initiative": "Advantage on Initiative rolls",
                        "ambush": "Advantage on attack rolls against any creature that hasn't taken a turn in the first round of combat",
                        "extra_damage": "Sneak Attack in round 1 deals extra damage of weapon type equal to Rogue level"
                    }
                },
                {
                    "id": "assassin_tools",
                    "name": "Assassin's Tools",
                    "summary": "Gain a Disguise Kit and a Poisoner's Kit, and proficiency with them.",
                    "description": "You gain a Disguise Kit and a Poisoner's Kit, and you have proficiency with them.",
                    "details": {
                        "items": ["Disguise Kit", "Poisoner's Kit"],
                        "proficiencies": ["Disguise Kit", "Poisoner's Kit"]
                    }
                }
            ],
            9: [
                {
                    "id": "assassin_infiltration_expertise",
                    "name": "Infiltration Expertise",
                    "summary": "Unerringly mimic speech/handwriting (1 hour study). Speed isn't reduced by Steady Aim.",
                    "description": "You are expert at the following techniques that aid your infiltrations. *-Masterful Mimicry-* You can unerringly mimic another person's speech, handwriting, or both if you have spent at least 1 hour studying them. *-Roving Aim-* Your Speed isn't reduced to 0 by using Steady Aim.",
                    "details": {
                        "mimicry": "Mimic speech, handwriting, or both after 1 hour of study",
                        "mobility": "Steady Aim doesn't reduce Speed to 0"
                    }
                }
            ],
            13: [
                {
                    "id": "assassin_envenom_weapon",
                    "name": "Envenom Weapon",
                    "summary": "Cunning Strike (Poison) deals extra 2d6 Poison damage (ignores Resistance).",
                    "description": "When you use the Poison option of your Cunning Strike, the target also takes 2d6 Poison damage whenever it fails the saving throw. This damage ignores Resistance to Poison damage.",
                    "details": {
                        "synergy": "Cunning Strike (Poison)",
                        "effect": "Target takes 2d6 Poison damage whenever it fails the saving throw",
                        "bypass": "Ignores Resistance to Poison damage"
                    }
                }
            ],
            17: [
                {
                    "id": "assassin_death_strike",
                    "name": "Death Strike",
                    "summary": "Round 1 Sneak Attack: target must save (Con) or damage is doubled.",
                    "description": "When you hit with your Sneak Attack on the first round of a combat, the target must succeed on a Constitution saving throw (DC 8 plus your Dexterity modifier and Proficiency Bonus), or the attack's damage is doubled against the target.",
                    "details": {
                        "condition": "Hit with Sneak Attack during the first round of combat",
                        "save": "Constitution vs DC (8 + Dex + Prof)",
                        "effect": "Your damage is doubled against the target on a failed save"
                    }
                }
            ]
        }
    },
    "soulknife": {
        "id": "soulknife",
        "name": "Soulknife",
        "description": "Most rogues rely on their prowess with blades and traps, but you strike with the power of your mind. You have learned to manifest psychic energy into shimmering blades that cut through flesh and spirit alike. Whether you are using your mental powers to bolster your skills, communicate telepathically, or strike from the shadows, you are a deadly force of psionic will.",
        "features": {
            3: [
                {
                    "id": "soulknife_psionic_power",
                    "name": "Psionic Power",
                    "summary": "Use Psionic Energy Dice to bolster skill checks (Psi-Bolstered Knack) or communicate telepathically (Psychic Whispers).",
                    "description": "You harbor a wellspring of psionic energy within yourself. It is represented by your Psionic Energy Dice, which fuel certain powers you have from this subclass. The Soulknife Energy Dice list shows the number of these dice you have when you reach certain Rogue levels, and the list shows the die size. \n Lv3: 4D6. \n Lv5: 6D8. \n Lv9: 8D8. \n Lv11: 8D10. \n Lv13: 10D10. \n Lv17: 12D12. Any features in this subclass that use a Psionic Energy Die use only the dice from this subclass. Some of your powers expend a Psionic Energy Die, as specified in a power's description, and you can't use a power if it requires you to use a die when your Psionic Energy Dice are all expended. \n You regain one of your expended Psionic Energy Dice when you finish a Short Rest, and you regain all of them when you finish a Long Rest. \n *-Psi-Bolstered Knack-* If you fail an ability check using a skill or tool with which you have proficiency, you can roll one Psionic Energy Die and add the number rolled to the check, potentially turning failure into success. The die is expended only if the roll then succeeds. \n *-Psychic Whispers-* You can establish telepathic communication between yourself and others. As a Magic action, choose one or more creatures you can see, up to a number of creatures equal to your Proficiency Bonus, and then roll one Psionic Energy Die. For a number of hours equal to the number rolled, the chosen creatures can speak telepathically with you, and you can speak telepathically with them. To send or receive a message (no action required), you and the other creature must be within 1 mile of each other. A creature can end the telepathic connection at any time (no action required). \n The first time you use this power after each Long Rest, you don't expend the Psionic Energy Die. All other times you use the power, you expend the die.",
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
                            "psi_bolstered_knack": "Fail a proficient check: roll die and add to total. Die only expended if you then succeed.",
                            "psychic_whispers": "Magic Action: establish telepathic link with creatures (equal to Prof Bonus) within 1 mile for roll hours. First use per LR is free."
                        }
                    }
                },
                {
                    "id": "soulknife_psychic_blades",
                    "name": "Psychic Blades",
                    "summary": "Manifest psychic blades (1d6/1d4) for attacks. Finess, Thrown (60/120), and Vex mastery.",
                    "description": "You can manifest shimmering blades of psychic energy. Whenever you take the Attack action or make an Opportunity Attack, you can manifest a Psychic Blade in your free hand and make the attack with that blade. The magic blade has the following traits: \n *-Psychic Blade-* \n 1d6 Psychic. Finesse, Thrown (60/120ft). Mastery: Vex (You can use this property, and it doesn't count against the number of properties you can use with Weapon Mastery). \n The blade vanishes immediately after it hits or misses its target, and it leaves no mark if it deals damage. \n After you attack with the blade on your turn, you can make a melee or ranged attack with a second psychic blade as a Bonus Action on the same turn if your other hand is free to create it. The damage die of this bonus attack is 1d4 instead of 1d6.",
                    "details": {
                        "attack": "Manifest blade when taking Attack or Opportunity Attack",
                        "traits": {
                            "damage": "1d6 Psychic + mod (1d4 for Bonus Action attack)",
                            "properties": ["Finesse", "Thrown (60/120ft)"],
                            "mastery": "Vex (independent of other masteries)"
                        },
                        "bonus_action": "Make another attack with a second psychic blade if other hand is free"
                    }
                }
            ],
            9: [
                {
                    "id": "soulknife_soul_blades",
                    "name": "Soul Blades",
                    "summary": "Use Psionic Energy Dice to turn missed attacks into hits (Homing Strikes) or teleport (Psychic Teleportation).",
                    "description": "You can now use the following powers with your Psychic Blades. *-Homing Strikes-* If you make an attack roll with your Psychic Blade and miss the target, you can roll one Psionic Energy Die and add the number rolled to the attack roll. If this causes the attack to hit, the die is expended. *-Psychic Teleportation-* As a Bonus Action, you manifest a Psychic Blade, expend one Psionic Energy Die and roll it, and throw the blade at an unoccupied space you can see up to a number of feet away equal to 10 times the number rolled. You then teleport to that space, and the blade vanishes.",
                    "details": {
                        "homing_strikes": "Missed Psychic Blade attack: roll die and add to hit. Die expended only if it hits.",
                        "psychic_teleportation": "Bonus Action: expend die, throw blade, and teleport 10x roll feet away."
                    }
                }
            ],
            13: [
                {
                    "id": "soulknife_psychic_veil",
                    "name": "Psychic Veil",
                    "summary": "Magic Action: become Invisible for 1 hour (ends if you deal damage or force a save).",
                    "description": "You can weave a veil of psychic static to mask yourself. As a Magic action, you gain the Invisible condition for 1 hour or until you dismiss this effect (no action required). This invisibility ends early immediately after you deal damage to a creature or you force a creature to make a saving throw. Once you use this feature, you can't do so again until you finish a Long Rest unless you expend a Psionic Energy Die (no action required) to restore your use of it.",
                    "details": {
                        "action": "Magic Action",
                        "duration": "1 hour",
                        "recharge": "Long Rest (or expend one Psionic Energy Die)"
                    }
                }
            ],
            17: [
                {
                    "id": "soulknife_rend_mind",
                    "name": "Rend Mind",
                    "summary": "Sneak Attack: target must save (Wis) or be Stunned for 1 minute.",
                    "description": "You can sweep your Psychic Blades through a creature's mind. When you use your Psychic Blades to deal Sneak Attack damage to a creature, you can force that target to make a Wisdom saving throw (DC 8 plus your Dexterity modifier and Proficiency Bonus). If the save fails, the target has the Stunned condition for 1 minute. The Stunned target repeats the save at the end of each of its turns, ending the effect on itself on a success. Once you use this feature, you can't do so again until you finish a Long Rest unless you expend three Psionic Energy Dice (no action required) to restore your use of it.",
                    "details": {
                        "condition": "Deal Sneak Attack damage with Psychic Blades",
                        "save": "Wisdom vs DC (8 + Dex + Prof)",
                        "effect": "Stunned for 1 minute (save ends at end of turns)",
                        "recharge": "Long Rest (or expend three Psionic Energy Dice)"
                    }
                }
            ]
        }
    },
    "thief": {
        "id": "thief",
        "name": "Thief",
        "description": "You have honed your skills in the larcenous arts. Burglars, bandits, cutpurses, and other criminals typically follow this archetype, but so do rogues who prefer to think of themselves as professional treasure seekers, explorers, delvers, and investigators. In addition to improving your agility and stealth, you learn skills useful for delving into ancient ruins, reading unfamiliar languages, and using magic items you normally couldn't wield.",
        "features": {
            3: [
                {
                    "id": "thief_fast_hands",
                    "name": "Fast Hands",
                    "summary": "Bonus Action: Sleight of Hand check, Utilize action, or Magic action (item).",
                    "description": "As a Bonus Action, you can do one of the following. \n *-Sleight of Hand-* Make a Dexterity (Sleight of Hand) check to pick a lock or disarm a trap with Thieves' Tools or to pick a pocket. \n *-Use an Object-* Take the Utilize action, or take the Magic action to use a magic item that requires that action.",
                    "details": {
                        "action": "Bonus Action",
                        "options": [
                            "Dexterity (Sleight of Hand) check to pick lock/disarm trap (Thieves' Tools) or pick pocket",
                            "Utilize action",
                            "Magic action to use a magic item"
                        ]
                    }
                },
                {
                    "id": "thief_second_story_work",
                    "name": "Second-Story Work",
                    "summary": "Gain Climb Speed; use Dexterity for jump distance.",
                    "description": "You've trained to get into especially hard-to-reach places, granting you these benefits. \n *-Climber-* You gain a Climb Speed equal to your Speed. \n *-Jumper-* You can determine your jump distance using your Dexterity rather than your Strength.",
                    "details": {
                        "climb_speed": "Equal to normal Speed",
                        "jumping": "Use Dexterity modifier instead of Strength for jump distance"
                    }
                }
            ],
            9: [
                {
                    "id": "thief_supreme_sneak",
                    "name": "Supreme Sneak",
                    "summary": "Cunning Strike: Stealth Attack (1d6). Attack doesn't end Hide invisibility if behind cover.",
                    "description": "You gain the following Cunning Strike option. \n Stealth Attack (Cost: 1d6). If you have the Hide action's Invisible condition, this attack doesn't end that condition on you if you end the turn behind Three-Quarters Cover or Total Cover.",
                    "details": {
                        "synergy": "Cunning Strike (Cost: 1d6)",
                        "effect": "Attack doesn't end the Hide action's Invisible condition if you end the turn behind 3/4 or Total Cover"
                    }
                }
            ],
            13: [
                {
                    "id": "thief_use_magic_device",
                    "name": "Use Magic Device",
                    "summary": "Attune to 4 items; chance to use charges for free; use Spell Scrolls (Arcana check).",
                    "description": "You've learned how to maximize use of magic items, granting you the following benefits. \n *-Attunement-* You can attune to up to four magic items at once. \n *Charges-* Whenever you use a magic item property that expends charges, roll 1d6. On a roll of 6, you use the property without expending the charges. \n *Scrolls-* You can use any Spell Scroll, using Intelligence as your spellcasting ability for the spell. If the spell is a cantrip or a level 1 spell, you can cast it reliably. If the scroll contains a higher-level spell, you must first succeed on an Intelligence (Arcana) check (DC 10 plus the spell's level). On a successful check, you cast the spell from the scroll. On a failed check, the scroll disintegrates.",
                    "details": {
                        "attunement": "Up to 4 magic items",
                        "charge_efficiency": "Roll 1d6 when expending charges; on a 6, no charges are expended",
                        "spell_scrolls": {
                            "ability": "Intelligence",
                            "reliable": "Cantrips and Level 1 spells",
                            "higher_level": "Intelligence (Arcana) check (DC 10 + spell level) or scroll disintegrates"
                        }
                    }
                }
            ],
            17: [
                {
                    "id": "thief_thiefs_reflexes",
                    "name": "Thief's Reflexes",
                    "summary": "Take two turns during the first round of combat.",
                    "description": "You are adept at laying ambushes and quickly escaping danger. You can take two turns during the first round of any combat. You take your first turn at your normal Initiative and your second turn at your Initiative minus 10.",
                    "details": {
                        "first_turn": "Normal Initiative",
                        "second_turn": "Initiative minus 10"
                    }
                }
            ]
        }
    }
}
