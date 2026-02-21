"""
Subclass definitions for the Warlock class.
"""

WARLOCK_SUBCLASSES = {
    "archfey_patron": {
        "id": "archfey_patron",
        "name": "Archfey Patron",
        "description": "Your patron is a lord or lady of the Fey Realm, a creature of legend who holds secrets and powers that predate human history. Such beings' motivations are often inscrutable, and they range from the capriciously benevolent to the malevolently cruel. Your pact with this being allows you to weave illusions and enchantments, and to move between the boundaries of the realms with grace and speed.",
        "features": {
            3: [
                {
                    "id": "archfey_patron_archfey_spells",
                    "name": "Archfey Spells",
                    "summary": "You always have certain fey-themed spells prepared.",
                    "details": {
                        "spells": {
                            3: ["Calm Emotions", "Faerie Fire", "Misty Step", "Phantasmal Force", "Sleep"],
                            5: ["Blink", "Plant Growth"],
                            7: ["Dominate Beast", "Greater Invisibility"],
                            9: ["Dominate Person", "Seeming"]
                        }
                    }
                },
                {
                    "id": "archfey_patron_steps_of_the_fey",
                    "name": "Steps Of The Fey",
                    "summary": "Cast Misty Step for free (Cha mod times). Apply bonus effects like Temp HP or Taunting.",
                    "details": {
                        "free_casts": "Charisma modifier (min 1) per Long Rest",
                        "extra_effects": {
                            "refreshing_step": "You or an ally within 10ft gains 1d10 Temporary Hit Points after teleporting",
                            "taunting_step": "Creatures within 5ft of departure point make Wis save or have Disadvantage on attacks against others until your next turn"
                        }
                    }
                }
            ],
            6: [
                {
                    "id": "archfey_patron_misty_escape",
                    "name": "Misty Escape",
                    "summary": "Reaction: Cast Misty Step when taking damage. Gain Disappearing and Dreadful step options.",
                    "details": {
                        "action": "Reaction (to taking damage)",
                        "new_options": {
                            "disappearing_step": "Invisible until your next turn or until you attack/deal damage/cast",
                            "dreadful_step": "Creatures within 5ft of origin or destination make Wis save or take 2d10 Psychic damage"
                        }
                    }
                }
            ],
            10: [
                {
                    "id": "archfey_patron_beguiling_defenses",
                    "name": "Beguiling Defenses",
                    "summary": "Immune to Charmed. Reaction: reduce damage by half and reflect Psychic damage.",
                    "details": {
                        "immunity": "Charmed condition",
                        "action": "Reaction (when hit by an attack)",
                        "effect": "Reduce damage by half (round down). Attacker makes Wis save or takes Psychic damage equal to your final damage taken",
                        "recharge": "Long Rest (or expend Pact Magic slot)"
                    }
                }
            ],
            14: [
                {
                    "id": "archfey_patron_bewitching_magic",
                    "name": "Bewitching Magic",
                    "summary": "Cast Misty Step for free immediately after casting an Enchantment or Illusion spell.",
                    "details": {
                        "trigger": "Cast an Enchantment or Illusion spell (Action and spell slot)",
                        "benefit": "Cast Misty Step as part of the same action without a spell slot"
                    }
                }
            ]
        }
    },
    "celestial_patron": {
        "id": "celestial_patron",
        "name": "Celestial Patron",
        "description": "Your patron is a powerful being of the Upper Planes, such as an empyrean, a solar, or a unicorn. Your pact with that being allows you to experience the barest touch of the holy light that illuminates the multiverse. You are bound to a being of divine power, and your magic allows you to heal wounds and channel radiant energy to purge the darkness.",
        "features": {
            3: [
                {
                    "id": "celestial_patron_celestial_spells",
                    "name": "Celestial Spells",
                    "summary": "You always have certain celestial-themed spells prepared.",
                    "details": {
                        "spells": {
                            3: ["Aid", "Cure Wounds", "Guiding Bolt", "Lesser Restoration", "Light", "Sacred Flame"],
                            5: ["Daylight", "Revivify"],
                            7: ["Guardian Of Faith", "Wall Of Fire"],
                            9: ["Greater Restoration", "Summon Celestial"]
                        }
                    }
                },
                {
                    "id": "celestial_patron_healing_light",
                    "name": "Healing Light",
                    "summary": "Bonus Action: Heal a creature within 60ft using a pool of d6s (1 + Warlock level).",
                    "details": {
                        "action": "Bonus Action",
                        "range": "60ft",
                        "pool_size": "1 + Warlock level (d6s)",
                        "max_per_use": "Charisma modifier (min 1)",
                        "recharge": "Long Rest"
                    }
                }
            ],
            6: [
                {
                    "id": "celestial_patron_radiant_soul",
                    "name": "Radiant Soul",
                    "summary": "Get Resistance to Radiant damage; add Charisma modifier once per turn to Radiant or Fire damage rolls.",
                    "details": {
                        "resistance": "Radiant damage",
                        "damage_bonus": "Once per turn, add Charisma modifier to Radiant or Fire damage of a spell against one target"
                    }
                }
            ],
            10: [
                {
                    "id": "celestial_patron_celestial_resilience",
                    "name": "Celestial Resilience",
                    "summary": "Gain Temp HP for yourself and up to 5 allies after Short/Long Rest or Magical Cunning.",
                    "details": {
                        "trigger": ["Short Rest", "Long Rest", "Magical Cunning feature"],
                        "self_temp_hp": "Warlock level + Charisma modifier",
                        "ally_temp_hp": "Half Warlock level + Charisma modifier (up to 5 allies)"
                    }
                }
            ],
            14: [
                {
                    "id": "celestial_patron_searing_vengeance",
                    "name": "Searing Vengeance",
                    "summary": "Reaction to Death Save: Regain 50% HP, deal Radiant damage, and Blind nearby enemies.",
                    "details": {
                        "action": "Reaction (when you or an ally within 60ft makes a Death Saving Throw)",
                        "benefit": "Target regains 50% Max HP and can end Prone condition",
                        "damage": "2d8 + Charisma modifier Radiant damage to chosen creatures within 30ft",
                        "effect": "Blinded condition until end of current turn",
                        "recharge": "Long Rest"
                    }
                }
            ]
        }
    },
    "fiend_patron": {
        "id": "fiend_patron",
        "name": "Fiend Patron",
        "description": "You have made a pact with a fiend from the lower planes of existence, a being whose aims are evil, even if you strive against those aims. Such beings desire the corruption or destruction of all things, ultimately including you.",
        "features": {
            3: [
                {
                    "id": "fiend_patron_dark_ones_blessing",
                    "name": "Dark One's Blessing",
                    "summary": "Gain Temp HP when you or an ally within 10ft reduces an enemy to 0 HP.",
                    "details": {
                        "trigger": "Enemy reduced to 0 HP (by you or ally within 10ft)",
                        "temp_hp": "Charisma modifier + Warlock level (min 1)"
                    }
                },
                {
                    "id": "fiend_patron_fiend_spells",
                    "name": "Fiend Spells",
                    "summary": "You always have certain fiend-themed spells prepared.",
                    "details": {
                        "spells": {
                            3: ["Burning Hands", "Command", "Scorching Ray", "Suggestion"],
                            5: ["Fireball", "Stinking Cloud"],
                            7: ["Fire Shield", "Wall Of Fire"],
                            9: ["Geas", "Insect Plague"]
                        }
                    }
                }
            ],
            6: [
                {
                    "id": "fiend_patron_dark_ones_own_luck",
                    "name": "Dark One's Own Luck",
                    "summary": "Add 1d10 to an ability check or saving throw (Cha mod times per LR).",
                    "details": {
                        "trigger": "Ability check or saving throw",
                        "effect": "Add 1d10 to the roll (can use after seeing the roll)",
                        "uses": "Charisma modifier (min 1) per Long Rest",
                        "limit": "Once per roll"
                    }
                }
            ],
            10: [
                {
                    "id": "fiend_patron_fiendish_resilience",
                    "name": "Fiendish Resilience",
                    "summary": "Resistance to one damage type (other than Force), chosen after each rest.",
                    "details": {
                        "benefit": "Resistance to one damage type of your choice",
                        "restriction": "Cannot choose Force",
                        "recharge": "Choose new damage type after any Short or Long Rest"
                    }
                }
            ],
            14: [
                {
                    "id": "fiend_patron_hurl_through_hell",
                    "name": "Hurl Through Hell",
                    "summary": "On hit: Transport target through hell for 8d10 Psychic damage and Incapacitated until your next turn.",
                    "details": {
                        "trigger": "Hit a creature with an attack roll",
                        "frequency": "Once per turn",
                        "save": "Charisma vs Spell DC",
                        "effect": "Target disappears until end of your next turn; takes 8d10 Psychic damage (if not a Fiend) and is Incapacitated",
                        "recharge": "Long Rest (or expend Pact Magic slot)"
                    }
                }
            ]
        }
    },
    "great_old_one_patron": {
        "id": "great_old_one_patron",
        "name": "Great Old One Patron",
        "description": "Your patron is a mysterious entity whose nature is utterly foreign to the fabric of reality. It might come from an elder god pronounced dead yet still dreaming. Its motives are incomprehensible, and its knowledge so immense and ancient that even the greatest libraries of mortal realms are but specks of dust. Your pact allows you to touch the minds of others and channel the maddening truth of the cosmos.",
        "features": {
            3: [
                {
                    "id": "great_old_one_patron_awakened_mind",
                    "name": "Awakened Mind",
                    "summary": "Bonus Action: Create a telepathic link with a creature (miles = Cha mod).",
                    "details": {
                        "action": "Bonus Action",
                        "range": "30ft",
                        "duration": "Warlock level minutes",
                        "limit": "Charisma modifier miles (min 1)",
                        "requirement": "Must share a language"
                    }
                },
                {
                    "id": "great_old_one_patron_spells",
                    "name": "Great Old One Spells",
                    "summary": "You always have certain alien-themed spells prepared.",
                    "details": {
                        "spells": {
                            3: ["Detect Thoughts", "Dissonant Whispers", "Phantasmal Force", "Tasha's Hideous Laughter"],
                            5: ["Clairvoyance", "Hunger Of Hadar"],
                            7: ["Confusion", "Summon Aberration"],
                            9: ["Modify Memory", "Telekinesis"]
                        }
                    }
                },
                {
                    "id": "great_old_one_patron_psychic_spells",
                    "name": "Psychic Spells",
                    "summary": "Can change Warlock spell damage to Psychic; cast Enchantment/Illusion without V or S components.",
                    "details": {
                        "damage_change": "Change Warlock spell damage to Psychic",
                        "component_reduction": "No Verbal or Somatic components for Enchantment or Illusion spells"
                    }
                }
            ],
            6: [
                {
                    "id": "great_old_one_patron_clairvoyant_combatant",
                    "name": "Clairvoyant Combatant",
                    "summary": "Force a telepathic target to make a Wis save or have Disadvantage on attacks against you.",
                    "details": {
                        "trigger": "Form a telepathic bond with Awakened Mind",
                        "save": "Wisdom vs Spell DC",
                        "effect": "Target has Disadvantage on attack rolls against you for the duration of the bond",
                        "recharge": "Short/Long Rest (or expend Pact Magic slot)"
                    }
                }
            ],
            10: [
                {
                    "id": "great_old_one_patron_eldritch_hex",
                    "name": "Eldritch Hex",
                    "summary": "Hex is always prepared. Hexed targets have Disadvantage on saving throws for the chosen ability.",
                    "details": {
                        "prepared": "Hex spell",
                        "effect": "Target has Disadvantage on saving throws of the ability chosen for Hex"
                    }
                },
                {
                    "id": "great_old_one_patron_thought_shield",
                    "name": "Thought Shield",
                    "summary": "Immune to telepathy (unless allowed), Resistance to Psychic damage, reflect Psychic damage.",
                    "details": {
                        "telepathy": "Thoughts cannot be read unless permitted",
                        "resistance": "Psychic damage",
                        "reflect": "Deal the same Psychic damage you take back to the attacker"
                    }
                }
            ],
            14: [
                {
                    "id": "great_old_one_patron_create_thrall",
                    "name": "Create Thrall",
                    "summary": "Cast Summon Aberration without Concentration (1 min). Summons get Temp HP and deal extra psychic damage to Hexed targets.",
                    "details": {
                        "benefit_1": "Summon Aberration duration 1 min without Concentration",
                        "benefit_2": "Aberration gains Temp HP (Warlock lvl + Cha mod) when summoned",
                        "benefit_3": "Aberration deals extra Psychic damage (Hex bonus) to creatures under your Hex once per turn"
                    }
                }
            ]
        }
    }
}
