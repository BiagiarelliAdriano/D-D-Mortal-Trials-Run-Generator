"""
Subclass definitions for the Sorcerer class.
"""

WILD_MAGIC_SURGE_TABLE = {
    "01-04": "Roll on this table at the start of each of your turns for the next minute, ignoring this result on subsequent rolls.",
    "05-08": "A creature that is Friendly toward you appears in a random unoccupied space within 60ft of you. The creature is under the DM's control and disappears 1 minute later. Roll 1d4 to determine the creature: on a 1, a Modron Duodrone appears; on a 2, a Flumph appears; on a 3, a Modron Monodrone appears; on a 4, a Unicorn appears.",
    "09-12": "For the next minute, you regain 5 Hit Points at the start of each of your turns.",
    "13-16": "Creatures have Disadvantage on saving throws against the next spell you cast in the next minute that involves a saving throw.",
    "17-20": "You are subjected to an effect that lasts for 1 minute unless its description says otherwise. Roll 1d8 to determine the effect: on a 1, you're surrounded by faint, ethereal music only you and creatures within 5ft of you can hear; on a 2, your size increases by one size category; on a 3, you grow a long beard made of feathers that remains until you sneeze, at which point the feathers explode from your face and vanish; on a 4, you must shout when you speak; on a 5, illusory butterflies flutter in the air within 10ft of you; on a 6, an eye appears on your forehead, granting you Advantage on Wisdom (Perception) checks; on a 7, pink bubbles float out of your mouth whenever you speak; on a 8, your skin turns a vibrant shade of blue for 24 hours or until the effect is ended by a Remove Curse spell.",
    "21-24": "For the next minute, all your spells with a casting time of an action have a casting time of a Bonus Action.",
    "25-28": "You are transported to the Astral Plane until the end of your next turn. You then return to the space you previously occupied or the nearest unoccupied space if that space is occupied.",
    "29-32": "The next time you cast a spell that deals damage within the next minute, don't roll the spell's damage dice for the damage. Instead use the highest number possible for each damage die.",
    "33-36": "You have Resistance to all damage for the next minute.",
    "37-40": "You turn into a potted plant until the start of your next turn. While you're a plant, you have the Incapacitated condition and have Vulnerability to all damage. If you drop to 0 Hit Points, your pot breaks, and your form reverts.",
    "41-44": "For the next minute, you can teleport up to 20ft as a Bonus Action on each of your turns.",
    "45-48": "You and up to three creatures you choose within 30ft of you have the Invisibile condition for 1 minute. This invisibility ends on a creature immediately after it makes an attack roll, deals damage or casts a spell.",
    "49-52": "A spectral shield hovers near you for the next minute, granting you a +2 bonus to AC and immunity to Magic Missile.",
    "53-56": "You can take one extra action on this turn.",
    "57-60": "You cast a random spell. If the spell normally requires Concentration, it doesn't require Concentration in this case; the spell lasts for its full duration. Roll 1d10 to determine the spell: on a 1, Confusion; on a 2, Fireball; on a 3, Fog Cloud; on a 4, Fly (cast on a random creature within 60ft of you); on a 5, Grease; on a 6, Levitate (cast on yourself); on a 7, Magic Missile (cast as a level 5 spell); On an 8, Mirror Image; on a 9, Polymorph (cast on yourself), and if you fail the saving throw, you turn into a Goat; on a 10, See Invisibility.",
    "61-64": "For the next minute, any flammable, nonmagical object you touch that isn't being worn or carried by another creature bursts into flame, takes 1d4 Fire damage, and is burning.",
    "65-68": "If you die within the next hour, you immediately revive as if by the Reincarnate spell.",
    "69-72": "You have the Frightened condition until the end of your next turn. The DM determines the source of your fear.",
    "73-76": "You teleport up to 60ft to an unoccupied space you can see.",
    "77-80": "A random creature within 60ft of you has the Poisoned condition for 1d4 hours.",
    "81-84": "You radiate Bright Light in a 30ft radius for the next minute. Any creature that ends its turn within 5ft of you has the Blinded condition until the end of its next turn.",
    "85-88": "Up to three creatures of your choice that you can see within 30ft of you take 1d10 Necrotic damage. You regain Hit Points equal to the sum of the Necrotic damage dealt.",
    "89-92": "Up to three creatures of your choice that you can see within 30ft of you take 4d10 Lightning damage.",
    "93-96": "You and all creatures within 30ft of you have Vulnerability to Piercing damage for the next minute.",
    "97-00": "Roll 1d6: On a 1, you regain 2d10 Hit Points; on a 2, one ally of your choice within 300ft of you regains 2d10 Hit Points; on a 3, you regain your lowest-level expended spell slot; on a 4, one ally of your choice within 300ft of you regains their lowest-level expended spell slot; on a 5, you regain all your expended Sorcery Points; on a 6, all the effects of row 17-20 affect you simultaneously."
}

SORCERER_SUBCLASSES = {
    "aberrant_sorcery": {
        "id": "aberrant_sorcery",
        "name": "Aberrant Sorcery",
        "description": "An alien influence has wrapped its tendrils around your mind, giving you psionic power. You might have been exposed to the Far Realm, or maybe you carry a psychic seed within you. Whatever the source, this power allows you to touch other minds and warp the reality around you with the force of your aberrant will.",
        "features": {
            3: [
                {
                    "id": "aberrant_sorcery_psionic_spells",
                    "name": "Psionic Spells",
                    "summary": "You always have certain psionic spells prepared.",
                    "details": {
                        "spells": {
                            3: ["Arms Of Hadar", "Calm Emotions", "Detect Thoughts", "Dissonant Whispers", "Mind Sliver"],
                            5: ["Hunger Of Hadar", "Sending"],
                            7: ["Evard's Black Tentacles", "Summon Aberration"],
                            9: ["Rary's Telepathic Bond", "Telekinesis"]
                        }
                    }
                },
                {
                    "id": "aberrant_sorcery_telepathic_speech",
                    "name": "Telepathic Speech",
                    "summary": "Bonus Action: Connect telepathically with a creature within 30ft for miles equal to Cha modifier.",
                    "details": {
                        "action": "Bonus Action",
                        "range": "30ft",
                        "duration": "Sorcerer level minutes",
                        "limit": "Charisma modifier miles (min 1)",
                        "requirement": "Must share a language to understand each other"
                    }
                }
            ],
            6: [
                {
                    "id": "aberrant_sorcery_psionic_sorcery",
                    "name": "Psionic Sorcery",
                    "summary": "Cast Psionic Spells using Sorcery Points (no V, S, or standard M components).",
                    "details": {
                        "cost": "Sorcery Points equal to spell level",
                        "benefit": "No Verbal or Somatic components; no Material components unless consumed or costly"
                    }
                },
                {
                    "id": "aberrant_sorcery_psychic_defenses",
                    "name": "Psychic Defenses",
                    "summary": "Get Resistance to Psychic damage and Advantage on saves vs Charmed/Frightened.",
                    "details": {
                        "resistance": "Psychic",
                        "advantages": ["Saving throws to avoid or end Charmed", "Saving throws to avoid or end Frightened"]
                    }
                }
            ],
            14: [
                {
                    "id": "aberrant_sorcery_revelation_in_flesh",
                    "name": "Revelation In Flesh",
                    "summary": "Bonus Action: Spend Sorcery Points to transform for 10 min (Swim, Fly, See Invisible, or Squeeze).",
                    "details": {
                        "action": "Bonus Action",
                        "cost": "1 Sorcery Point per benefit",
                        "duration": "10 minutes",
                        "options": {
                            "aquatic_adaptation": "Swim Speed (2x Speed) and water breathing (gills)",
                            "glistening_flight": "Fly Speed (equal to Speed) and hover",
                            "see_the_invisible": "See Invisible creatures within 60ft (no total cover)",
                            "wormlike_movement": "Squeeze through 1-inch spaces; 5ft movement to escape grapple/restraints"
                        }
                    }
                }
            ],
            18: [
                {
                    "id": "aberrant_sorcery_warping_implosion",
                    "name": "Warping Implosion",
                    "summary": "Magic Action: Teleport up to 120ft; creatures near departure point take 3d10 Force damage and are pulled in.",
                    "details": {
                        "action": "Magic Action",
                        "range": "120ft (teleport)",
                        "effect_area": "30ft radius from origin",
                        "damage": "3d10 Force (half on success)",
                        "save": "Strength vs Spell DC",
                        "recharge": "Long Rest (or 5 Sorcery Points)"
                    }
                }
            ]
        }
    },
    "clockwork_sorcery": {
        "id": "clockwork_sorcery",
        "name": "Clockwork Sorcery",
        "description": "The cosmic force of order has suffused your being. You might be linked to the Plane of Perfect Order, where everything is governed by rigid laws and mechanical precision. Your magic manifests as shimmering gears, ticking echoes, and geometric patterns, allowing you to impose structure on the chaos of the world and shield your allies with the logic of the grand equation.",
        "features": {
            3: [
                {
                    "id": "clockwork_sorcery_spells",
                    "name": "Clockwork Spells",
                    "summary": "You always have certain order-themed spells prepared and manifest visual signs of order.",
                    "details": {
                        "spells": {
                            3: ["Aid", "Alarm", "Lesser Restoration", "Protection From Evil And Good"],
                            5: ["Dispel Magic", "Protection From Energy"],
                            7: ["Freedom Of Movement", "Summon Construct"],
                            9: ["Greater Restoration", "Wall Of Force"]
                        },
                        "manifestations": [
                            "Spectral cogwheels hover behind you",
                            "The hands of a clock spin in your eyes",
                            "Your skin glows with a brassy sheen",
                            "Floating equations and geometric objects overlay your body",
                            "Your Spellcasting Focus takes the form of a Tiny clockwork mechanism",
                            "The ticking of gears or ringing of a clock is audible"
                        ]
                    }
                },
                {
                    "id": "clockwork_sorcery_restore_balance",
                    "name": "Restore Balance",
                    "summary": "Reaction: Prevent Advantage or Disadvantage on a d20 roll within 60ft.",
                    "details": {
                        "action": "Reaction",
                        "range": "60ft",
                        "effect": "Prevent Advantage or Disadvantage from affecting the roll",
                        "recharge": "Long Rest",
                        "uses": "Charisma modifier (min 1)"
                    }
                }
            ],
            6: [
                {
                    "id": "clockwork_sorcery_bastion_of_law",
                    "name": "Bastion Of Law",
                    "summary": "Magic Action: Spend 1-5 Sorcery Points to create a d8-based damage reduction ward.",
                    "details": {
                        "action": "Magic Action",
                        "range": "30ft",
                        "cost": "1 to 5 Sorcery Points",
                        "effect": "Ward has d8s equal to points spent. Use d8s to reduce incoming damage count.",
                        "duration": "Until Long Rest or reused"
                    }
                }
            ],
            14: [
                {
                    "id": "clockwork_sorcery_trance_of_order",
                    "name": "Trance Of Order",
                    "summary": "Bonus Action: For 1 min, attacks against you can't have Advantage, and you treat d20 rolls of 9 or lower as 10.",
                    "details": {
                        "action": "Bonus Action",
                        "duration": "1 minute",
                        "benefits": [
                            "Attack rolls against you cannot benefit from Advantage",
                            "Treat any d20 roll of 9 or lower as a 10"
                        ],
                        "recharge": "Long Rest (or 5 Sorcery Points)"
                    }
                }
            ],
            18: [
                {
                    "id": "clockwork_sorcery_clockwork_cavalcade",
                    "name": "Clockwork Cavalcade",
                    "summary": "Magic Action: Summon spirits in a 30ft Cube to Heal 100 HP, Repair objects, and Dispel level 6- spells.",
                    "details": {
                        "action": "Magic Action",
                        "area": "30ft Cube originating from you",
                        "effects": [
                            "Heal: Restore up to 100 HP, divided as you choose among creatures in the cube",
                            "Repair: Instantly repair damaged objects entirely in the cube",
                            "Dispel: End every level 6 or lower spell on chosen creatures/objects in the cube"
                        ],
                        "recharge": "Long Rest (or 7 Sorcery Points)"
                    }
                }
            ]
        }
    },
    "draconic_sorcery": {
        "id": "draconic_sorcery",
        "name": "Draconic Sorcery",
        "description": "Your innate magic comes from draconic magic that was mingled with your blood or that of your ancestors. Most often, sorcerers with this origin trace their descent back to a mighty sorcerer of ancient times who made a bargain with a dragon or who might even have claimed a dragon parentage. The power of dragons flows through your veins, granting you physical resilience and the ability to channel elemental fury.",
        "features": {
            3: [
                {
                    "id": "draconic_sorcery_resilience",
                    "name": "Draconic Resilience",
                    "summary": "Max HP increases by 3 plus 1 per Sorcerer level; Unarmored AC = 10 + Dex + Cha.",
                    "details": {
                        "hp_bonus": "3 + 1 per Sorcerer level",
                        "ac_calc": "10 + Dexterity modifier + Charisma modifier (when not wearing armor)",
                        "visuals": "Dragon-like scales cover parts of your body"
                    }
                },
                {
                    "id": "draconic_sorcery_spells",
                    "name": "Draconic Spells",
                    "summary": "You always have certain dragon-themed spells prepared.",
                    "details": {
                        "spells": {
                            3: ["Alter Self", "Chromatic Orb", "Command", "Dragon's Breath"],
                            5: ["Fear", "Fly"],
                            7: ["Arcane Eye", "Charm Monster"],
                            9: ["Legend Lore", "Summon Dragon"]
                        }
                    }
                }
            ],
            6: [
                {
                    "id": "draconic_sorcery_elemental_affinity",
                    "name": "Elemental Affinity",
                    "summary": "Gain Resistance to a damage type and add Charisma modifier to its damage rolls.",
                    "details": {
                        "options": ["Acid", "Cold", "Fire", "Lightning", "Poison"],
                        "benefit_1": "Resistance to the chosen damage type",
                        "benefit_2": "Add Charisma modifier to one damage roll of a spell that deals the chosen type"
                    }
                }
            ],
            14: [
                {
                    "id": "draconic_sorcery_dragon_wings",
                    "name": "Dragon Wings",
                    "summary": "Bonus Action: Gain Fly Speed (60ft) for 1 hour.",
                    "details": {
                        "action": "Bonus Action",
                        "speed": "60ft",
                        "duration": "1 hour",
                        "recharge": "Long Rest (or 3 Sorcery Points)"
                    }
                }
            ],
            18: [
                {
                    "id": "draconic_sorcery_dragon_companion",
                    "name": "Dragon Companion",
                    "summary": "Cast Summon Dragon for free once per LR; can cast without Concentration (duration 1 min).",
                    "details": {
                        "free_cast": "One cast without a spell slot per Long Rest",
                        "components": "No Material components required",
                        "concentration_option": "Can modify to not require Concentration; duration becomes 1 minute"
                    }
                }
            ]
        }
    },
    "wild_magic_sorcery": {
        "id": "wild_magic_sorcery",
        "name": "Wild Magic Sorcery",
        "description": "Your innate magic comes from the wild forces of chaos that underlie the order of the creation. You might have been exposed to some form of raw magic, perhaps through a planar portal leading to Limbo, the Elemental Planes, or the mysterious Fey Realm. Or your magic might be a fluke of your birth, with no apparent cause or reason. However it came to be, this magic churns within you, waiting for any outlet to burst free in a surge of untamed power.",
        "features": {
            3: [
                {
                    "id": "wild_magic_surge",
                    "name": "Wild Magic Surge",
                    "summary": "Casting slot-leveled spells can trigger a random magical effect on a d20 roll of 20.",
                    "details": {
                        "trigger": "Cast a Sorcerer spell with a spell slot",
                        "frequency": "Once per turn",
                        "roll": "Roll 1d20; on a 20, roll on the Wild Magic Surge table",
                        "restriction": "Spell effects from the table cannot be modified by Metamagic",
                        "surge_table": WILD_MAGIC_SURGE_TABLE
                    }
                },
                {
                    "id": "wild_magic_tides_of_chaos",
                    "name": "Tides Of Chaos",
                    "summary": "Gain Advantage on one d20 Test. Recharges on Long Rest or by casting a spell (triggers Surge).",
                    "details": {
                        "benefit": "Advantage on one d20 Test",
                        "recharge": {
                            "standard": "Long Rest",
                            "chaos_surge": "Cast a Sorcerer spell with a spell slot to regain use, then automatically roll on the Wild Magic Surge table"
                        }
                    }
                }
            ],
            6: [
                {
                    "id": "wild_magic_bend_luck",
                    "name": "Bend Luck",
                    "summary": "Reaction: Spend 1 Sorcery Point to add or subtract 1d4 from another creature's d20 roll.",
                    "details": {
                        "action": "Reaction",
                        "cost": "1 Sorcery Point",
                        "range": "Visible creature",
                        "effect": "Add or subtract 1d4 bonus/penalty to the target's d20 roll"
                    }
                }
            ],
            14: [
                {
                    "id": "wild_magic_controlled_chaos",
                    "name": "Controlled Chaos",
                    "summary": "Roll twice on the Wild Magic Surge table and choose either result.",
                    "details": {
                        "benefit": "Roll twice when rolling on the Wild Magic Surge table; use either number",
                        "surge_table": WILD_MAGIC_SURGE_TABLE
                    }
                }
            ],
            18: [
                {
                    "id": "wild_magic_tamed_surge",
                    "name": "Tamed Surge",
                    "summary": "Once per LR: Choose any result from the Wild Magic Surge table (except final row) instead of rolling.",
                    "details": {
                        "trigger": "Cast a Sorcerer spell with a spell slot",
                        "effect": "Pick any effect except the final row. If effect involves a roll, you must make it.",
                        "recharge": "Long Rest",
                        "surge_table": WILD_MAGIC_SURGE_TABLE
                    }
                }
            ]
        }
    }
}
