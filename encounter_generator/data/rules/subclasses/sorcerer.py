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
                    "description": "When you reach a Sorcerer level specified in the Psionic Spells list, you thereafter always have the listed spells prepared. \n Lv3: Arms of Hadar, Calm Emotions, Detect Thoughts, Dissonant Whispers, Mind Sliver. \n Lv5: Hunger of Hadar, Sending. \n Lv7: Evard's Black Tentacles, Summon Aberration. \n Lv9: Rary's Telepathic Bond, Telekinesis.",
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
                    "description": "You can form a telepathic connection between your mind and the mind of another. As a Bonus Action, choose one creature you can see within 30 feet of yourself. You and the chosen creature can communicate telepathically with each other while the two of you are within a number of miles of each other equal to your Charisma modifier (minimum of 1 mile). To understand each other, you each must mentally use a language the other knows. The telepathic connection lasts for a number of minutes equal to your Sorcerer level. It ends early if you use this ability to form a connection with a different creature.",
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
                    "description": "When you cast any level 1+ spell from your Psionic Spells feature, you can cast it by expending a spell slot as normal or by spending a number of Sorcery Points equal to the spell's level. If you cast the spell using Sorcery Points, it requires no Verbal or Somatic components, and it requires no Material components unless they are consumed by the spell or have a cost specified in it.",
                    "details": {
                        "cost": "Sorcery Points equal to spell level",
                        "benefit": "No Verbal or Somatic components; no Material components unless consumed or costly"
                    }
                },
                {
                    "id": "aberrant_sorcery_psychic_defenses",
                    "name": "Psychic Defenses",
                    "summary": "Get Resistance to Psychic damage and Advantage on saves vs Charmed/Frightened.",
                    "description": "You have Resistance to Psychic damage, and you have Advantage on saving throws to avoid or end the Charmed or Frightened condition.",
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
                    "description": "You can unleash the aberrant truth hidden within yourself. As a Bonus Action, you can spend 1 Sorcery Point or more to magically alter your body for 10 minutes. For each Sorcery Point you spend, you gain one of the following benefits of your choice, the effects of which last until the alteration ends. \n *-Aquatic Adaptation-* You gain a Swim Speed equal to twice your Speed, and you can breathe underwater. Gills grow from your neck or flare behind your ears, and your fingers become webbed or you grow wriggling cilia. *-Glistening Flight-* You gain a Fly Speed equal to your Speed, and you can hover. As you fly, your skin glistens with mucus or otherworldly light. *-See the Invisible-* You can see any Invisible creature within 60 feet of yourself that isn't behind Total Cover. Your eyes also turn black or become writhing sensory tendrils. *-Wormlike Movement-* Your body, along with any equipment you are wearing or carrying, becomes slimy and pliable. You can move through any space as narrow as 1 inch, and you can spend 5 feet of movement to escape from nonmagical restraints or the Grappled condition.",
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
                    "description": "You can unleash a space-warping anomaly. As a Magic action, you teleport to an unoccupied space you can see within 120 feet of yourself. Immediately after you disappear, each creature within 30 feet of the space you left must make a Strength saving throw against your spell save DC. On a failed save, a creature takes 3d10 Force damage and is pulled straight toward the space you left, ending in an unoccupied space as close to your former space as possible. On a successful save, the creature takes half as much damage only. Once you use this feature, you can't do so again until you finish a Long Rest unless you spend 5 Sorcery Points (no action required) to restore your use of it.",
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
                    "description": "When you reach a Sorcerer level specified in the Clockwork Spells list, you thereafter always have the listed spells prepared. \n Lv3: Aid, Alarm, Lesser Restoration, Protection from Evil and Good. \n Lv5: Dispel Magic, Protection from Energy. \n Lv7: Freedom of Movement, Summon Construct. \n Lv9: Greater Restoration, Wall of Force. \n In addition, consult the Manifestations of Order list and choose or randomly determine a way your connection to order manifests while you are casting any of your Sorcerer spells. \n 1d6: \n 1 = Spectral cogwheels hover behind you. \n 2 = The hands of a clock spin in your eyes. \n 3 = Your skin glows with a brassy sheen. \n 4 = Floating equations and geometric objects overlay your body. \n 5 = Your Spellcasting Focus temporarily takes the form of a Tiny clockwork mechanism. \n 6 = The ticking of gears or ringing of a clock can be heard by you and those affected by your magic.",
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
                    "description": "Your connection to the plane of absolute order allows you to equalize chaotic moments. When a creature you can see within 60 feet of yourself is about to roll a d20 with Advantage or Disadvantage, you can take a Reaction to prevent the roll from being affected by Advantage and Disadvantage. You can use this feature a number of times equal to your Charisma modifier (minimum of once), and you regain all expended uses when you finish a Long Rest.",
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
                    "description": "You can tap into the grand equation of existence to imbue a creature with a shimmering shield of order. As a Magic action, you can expend 1 to 5 Sorcery Points to create a magical ward around yourself or another creature you can see within 30 feet of yourself. The ward is represented by a number of d8s equal to the number of Sorcery Points spent to create it. When the warded creature takes damage, it can expend a number of those dice, roll them, and reduce the damage taken by the total rolled on those dice. The ward lasts until you finish a Long Rest or until you use this feature again.",
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
                    "description": "You gain the ability to align your consciousness with the endless calculations of Mechanus. As a Bonus Action, you can enter this state for 1 minute. For the duration, attack rolls against you can't benefit from Advantage, and whenever you make a D20 Test, you can treat a roll of 9 or lower on the d20 as a 10. Once you use this feature, you can't use it again until you finish a Long Rest unless you spend 5 Sorcery Points (no action required) to restore your use of it.",
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
                    "description": "You momentarily summon spirits of order to expunge disorder around you. As a Magic action, you summon the spirits in a 30-foot Cube originating from you. The spirits look like modrons or other Constructs of your choice. The spirits are intangible and invulnerable, and they create the effects below within the Cube before vanishing. Once you use this action, you can't use it again until you finish a Long Rest unless you spend 7 Sorcery Points (no action required) to restore your use of it. \n *-Heal-* The spirits restore up to 100 Hit Points, divided as you choose among any number of creatures of your choice in the Cube. \n *-Repair-* Any damaged objects entirely in the Cube are repaired instantly. \n *.Dispel-* Every spell of level 6 and lower ends on creatures and objects of your choice in the Cube.",
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
                    "description": "The magic in your body manifests physical traits of your draconic gift. Your Hit Point maximum increases by 3, and it increases by 1 whenever you gain another Sorcerer level. \n Parts of you are also covered by dragon-like scales. While you aren't wearing armor, your base Armor Class equals 10 plus your Dexterity and Charisma modifiers.",
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
                    "description": "When you reach a Sorcerer level specified in the Draconic Spells list, you thereafter always have the listed spells prepared. \n Lv3: Alter Self, Chromatic Orb, Command, Dragon's Breath. \n Lv5: Fear, Fly. \n Lv7: Arcane Eye, Charm Monster. \n Lv9: Legend Lore, Summon Dragon.",
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
                    "description": "Your draconic magic has an affinity with a damage type associated with dragons. Choose one of those types: Acid, Cold, Fire, Lightning, or Poison. You have Resistance to that damage type, and when you cast a spell that deals damage of that type, you can add your Charisma modifier to one damage roll of that spell.",
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
                    "description": "As a Bonus Action, you can cause draconic wings to appear on your back. The wings last for 1 hour or until you dismiss them (no action required). For the duration, you have a Fly Speed of 60 feet. Once you use this feature, you can't use it again until you finish a Long Rest unless you spend 3 Sorcery Points (no action required) to restore your use of it.",
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
                    "description": "You can cast Summon Dragon without a Material component. You can also cast it once without a spell slot, and you regain the ability to cast it in this way when you finish a Long Rest. Whenever you start casting the spell, you can modify it so that it doesn't require Concentration. If you do so, the spell's duration becomes 1 minute for that casting.",
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
                    "description": "Your spellcasting can unleash surges of untamed magic. Once per turn, you can roll 1d20 immediately after you cast a Sorcerer spell with a spell slot. If you roll a 20, roll on the Wild Magic Surge table to create a magical effect. If the magical effect is a spell, it is too wild to be affected by your Metamagic.",
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
                    "description": "You can manipulate chaos itself to give yourself Advantage on one D20 Test before you roll the d20. Once you do so, you must cast a Sorcerer spell with a spell slot or finish a Long Rest before you can use this feature again. If you do cast a Sorcerer spell with a spell slot before you finish a Long Rest, you automatically roll on the Wild Magic Surge table.",
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
                    "description": "You have the ability to twist fate using your wild magic. Immediately after another creature you can see rolls the d20 for a D20 Test, you can take a Reaction and spend 1 Sorcery Point to roll 1d4 and apply the number rolled as a bonus or penalty (your choice) to the d20 roll.",
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
                    "description": "You gain a modicum of control over the surges of your wild magic. Whenever you roll on the Wild Magic Surge table, you can roll twice and use either number.",
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
                    "description": "Immediately after you cast a Sorcerer spell with a spell slot, you can create an effect of your choice from the Wild Magic Surge table instead of rolling on that table. You can choose any effect in the table except for the final row, and if the chosen effect involves a roll, you must make it. Once you use this feature, you can't do so again until you finish a Long Rest.",
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
