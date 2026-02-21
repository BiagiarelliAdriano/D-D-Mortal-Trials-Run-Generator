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
                    "details": {
                        "first_turn": "Normal Initiative",
                        "second_turn": "Initiative minus 10"
                    }
                }
            ]
        }
    }
}
