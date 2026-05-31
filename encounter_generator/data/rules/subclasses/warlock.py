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
                    "description": "The magic of your patron ensures you always have certain spells ready; when you reach a Warlock level specified in the Archfey Spells list, you thereafter always have the listed spells prepared. \n Lv3: Calm Emotions, Faerie Fire, Misty Step, Phantasmal Force, Sleep. \n Lv5: Blink, Plant Growth. \n Lv7: Dominate Beast, Greater Invisibility. \n Lv9: Dominate Person, Seeming.",
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
                    "description": "Your patron grants you the ability to move between the boundaries of the planes. You can cast Misty Step without expending a spell slot a number of times equal to your Charisma modifier (minimum of once), and you regain all expended uses when you finish a Long Rest. In addition, whenever you cast that spell, you can choose one of the following additional effects. \n *-Refreshing Step-* Immediately after you teleport, you or one creature you can see within 10 feet of yourself gains 1d10 Temporary Hit Points. \n *-Taunting Step-* Creatures within 5 feet of the space you left must succeed on a Wisdom saving throw against your spell save DC or have Disadvantage on attack rolls against creatures other than you until the start of your next turn.",
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
                    "description": "You can cast Misty Step as a Reaction in response to taking damage. In addition, the following effects are now among your Steps of the Fey options. \n *-Disappearing Step-* You have the Invisible condition until the start of your next turn or until immediately after you make an attack roll, deal damage, or cast a spell. \n *-Dreadful Step-* Creatures within 5 feet of the space you left or the space you appear in (your choice) must succeed on a Wisdom saving throw against your spell save DC or take 2d10 Psychic damage.",
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
                    "description": "Your patron teaches you how to guard your mind and body. You are immune to the Charmed condition. In addition, immediately after a creature you can see hits you with an attack roll, you can take a Reaction to reduce the damage you take by half (round down), and you can force the attacker to make a Wisdom saving throw against your spell save DC. On a failed save, the attacker takes Psychic damage equal to the damage you take. Once you use this Reaction, you can't use it again until you finish a Long Rest unless you expend a Pact Magic spell slot (no action required) to restore your use of it.",
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
                    "description": "Your patron grants you the ability to weave your magic with teleportation. Immediately after you cast an Enchantment or Illusion spell using an action and a spell slot, you can cast Misty Step as part of the same action and without expending a spell slot.",
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
                    "description": "The magic of your patron ensures you always have certain spells ready; when you reach a Warlock level specified in the Celestial Spells list, you thereafter always have the listed spells prepared. \n Lv3: Aid, Cure Wounds, Guiding Bolt, Lesser Restoration, Light, Sacred Flame. \n Lv5: Daylight, Revivify. \n Lv7: Guardian of Faith, Wall of Fire. \n Lv9: Greater Restoration, Summon Celestial.",
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
                    "description": "You gain the ability to channel celestial energy to heal wounds. You have a pool of d6s to fuel this healing. The number of dice in the pool equals 1 plus your Warlock level. As a Bonus Action, you can heal yourself or one creature you can see within 60 feet of yourself, expending dice from the pool. The maximum number of dice you can expend at once equals your Charisma modifier (minimum of one die). Roll the dice you expend, and restore a number of Hit Points equal to the roll's total. Your pool regains all expended dice when you finish a Long Rest.",
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
                    "description": "Your link to your patron allows you to serve as a conduit for radiant energy. You have Resistance to Radiant damage. Once per turn, when a spell you cast deals Radiant or Fire damage, you can add your Charisma modifier to that spell's damage against one of the spell's targets.",
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
                    "description": "You gain Temporary Hit Points whenever you use your Magical Cunning feature or finish a Short or Long Rest. These Temporary Hit Points equal your Warlock level plus your Charisma modifier. Additionally, choose up to five creatures you can see when you gain the points. Those creatures each gain Temporary Hit Points equal to half your Warlock level plus your Charisma modifier.",
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
                    "description": "When you or an ally within 60 feet of you is about to make a Death Saving Throw, you can unleash radiant energy to save the creature. The creature regains Hit Points equal to half its Hit Point maximum and can end the Prone condition on itself. Each creature of your choice that is within 30 feet of the creature takes Radiant damage equal to 2d8 plus your Charisma modifier, and each has the Blinded condition until the end of the current turn. Once you use this feature, you can't use it again until you finish a Long Rest.",
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
                    "description": "When you reduce an enemy to 0 Hit Points, you gain Temporary Hit Points equal to your Charisma modifier plus your Warlock level (minimum of 1 Temporary Hit Point). You also gain this benefit if someone else reduces an enemy within 10 feet of you to 0 Hit Points.",
                    "details": {
                        "trigger": "Enemy reduced to 0 HP (by you or ally within 10ft)",
                        "temp_hp": "Charisma modifier + Warlock level (min 1)"
                    }
                },
                {
                    "id": "fiend_patron_fiend_spells",
                    "name": "Fiend Spells",
                    "summary": "You always have certain fiend-themed spells prepared.",
                    "description": "The magic of your patron ensures you always have certain spells ready; when you reach a Warlock level specified in the Fiend Spells list, you thereafter always have the listed spells prepared. \n Lv3: Burning Hands, Command, Scorching Ray, Suggestion. \n Lv5: Fireball, Stinking Cloud. \n Lv7: Fire Shield, Wall of Fire. \n 9: Geas, Insect Plague.",
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
                    "description": "You can call on your fiendish patron to alter fate in your favor. When you make an ability check or a saving throw, you can use this feature to add 1d10 to your roll. You can do so after seeing the roll but before any of the roll's effects occur. You can use this feature a number of times equal to your Charisma modifier (minimum of once), but you can use it no more than once per roll. You regain all expended uses when you finish a Long Rest.",
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
                    "description": "Choose one damage type, other than Force, whenever you finish a Short or Long Rest. You have Resistance to that damage type until you choose a different one with this feature.",
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
                    "description": "Once per turn when you hit a creature with an attack roll, you can try to instantly transport the target through the Lower Planes. The target must succeed on a Charisma saving throw against your spell save DC, or the target disappears and hurtles through a nightmare landscape. The target takes 8d10 Psychic damage if it isn't a Fiend, and it has the Incapacitated condition until the end of your next turn, when it returns to the space it previously occupied or the nearest unoccupied space. Once you use this feature, you can't use it again until you finish a Long Rest unless you expend a Pact Magic spell slot (no action required) to restore your use of it.",
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
                    "description": "You can form a telepathic connection between your mind and the mind of another. As a Bonus Action, choose one creature you can see within 30 feet of yourself. You and the chosen creature can communicate telepathically with each other while the two of you are within a number of miles of each other equal to your Charisma modifier (minimum of 1 mile). To understand each other, you each must mentally use a language the other knows. The telepathic connection lasts for a number of minutes equal to your Warlock level. It ends early if you use this feature to connect with a different creature.",
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
                    "description": "The magic of your patron ensures you always have certain spells ready; when you reach a Warlock level specified in the Great Old One Spells list, you thereafter always have the listed spells prepared. \n Lv3: Detect Thoughts, Dissonant Whispers, Phantasmal Force, Tasha's Hideous Laughter. \n Lv5: Clairvoyance, Hunger of Hadar. \n Lv7: Confusion, Summon Aberration. \n Lv9: Modify Memory, Telekinesis.",
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
                    "description": "When you cast a Warlock spell that deals damage, you can change its damage type to Psychic. In addition, when you cast a Warlock spell that is an Enchantment or Illusion, you can do so without Verbal or Somatic components.",
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
                    "description": "When you form a telepathic bond with a creature using your Awakened Mind, you can force that creature to make a Wisdom saving throw against your spell save DC. On a failed save, the creature has Disadvantage on attack rolls against you, and you have Advantage on attack rolls against that creature for the duration of the bond. Once you use this feature, you can't use it again until you finish a Short or Long Rest unless you expend a Pact Magic spell slot (no action required) to restore your use of it.",
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
                    "description": "Your alien patron grants you a powerful curse. You always have the Hex spell prepared. When you cast Hex and choose an ability, the target also has Disadvantage on saving throws of the chosen ability for the duration of the spell.",
                    "details": {
                        "prepared": "Hex spell",
                        "effect": "Target has Disadvantage on saving throws of the ability chosen for Hex"
                    }
                },
                {
                    "id": "great_old_one_patron_thought_shield",
                    "name": "Thought Shield",
                    "summary": "Immune to telepathy (unless allowed), Resistance to Psychic damage, reflect Psychic damage.",
                    "description": "Your thoughts can't be read by telepathy or other means unless you allow it. You also have Resistance to Psychic damage, and whenever a creature deals Psychic damage to you, that creature takes the same amount of damage that you take.",
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
                    "description": "When you cast Summon Aberration, you can modify it so that it doesn't require Concentration. If you do so, the spell's duration becomes 1 minute for that casting, and when summoned, the Aberration has a number of Temporary Hit Points equal to your Warlock level plus your Charisma modifier. In addition, the first time each turn the Aberration hits a creature under the effect of your Hex, the Aberration deals extra Psychic damage to the target equal to the bonus damage of that spell.",
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
