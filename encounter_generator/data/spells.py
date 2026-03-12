SPELLS = {
    0: [
        {
            "name": "Acid Splash",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Arcana Cleric", "Arcane Trickster Rogue", "Circle of the Land",
                           "Lore Bard", "Eldritch Knight Fighter", "Evoker Wizard"],
            "sources": ["Elf", "Magic Initiate", "Pact Of The Tome"],
            "action": "Action",
            "range": "60ft",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "You create an acidic bubble at a point within range, where it explodes in a 5ft radius Sphere. Each creature in that Sphere must succeed on a Dexterity Saving Throw or take 1d6 Acid damage.",
            "damage": "1d6",
            "damage_type": "Acid",
            "scaling": {
                "5": {"value": "2d6"},
                "11": {"value": "3d6"},
                "17": {"value": "4d6"}
            }
        },
        {
            "name": "Blade Ward",
            "school": "Abjuration",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Abjurer Wizard", "Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"],
            "sources": ["Elf", "Magic Initiate", "Pact Of The Tome"],
            "action": "Action",
            "range": "Self",
            "components": ["V", "S"],
            "duration": "Concentration, up to 1 minute",
            "description": "Whenever a creature makes an Attack Roll against you before the spell ends, the attacker subtracts 1d4 from the Attack Roll.",
            "damage": "1d4",
            "damage_type": "Debuff"
        },
        {
            "name": "Chill Touch",
            "school": "Necromancy",
            "classes": ["Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"],
            "sources": ["Elf", "Tiefling", "Magic Initiate", "Pact Of The Tome"],
            "action": "Action",
            "range": "Touch",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "Channeling the chill of the grave, make a Melee Spell Attack against a target within reach. On a hit, the target takes 1d10 Necrotic damage, and it can't regain Hit Points until the end of your next turn.",
            "damage": "1d10",
            "damage_type": "Necrotic",
            "attack_type": "Melee Spell",
            "scaling": {
                "5": {"value": "2d10"},
                "11": {"value": "3d10"},
                "17": {"value": "4d10"}
            }
        },
        {
            "name": "Eldritch Blast",
            "school": "Evocation",
            "classes": ["Warlock"],
            "sources": ["Magic Initiate", "Pact Of The Tome"],
            "action": "Action",
            "range": "120ft",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "You hurl a beam of crackling energy. Make a Ranged Spell Attack against one creature or object in range. On a hit, the target takes 1d10 Force damage.",
            "damage": "1d10",
            "damage_type": "Force",
            "attack_type": "Ranged Spell",
            "scaling": {
                "5": {
                    "value": "2 beams",
                    "desc_add": "You can direct the beams at the same target or at different ones. Make a separate Attack Roll for each beam."
                },
                "11": {
                    "value": "3 beams",
                    "desc_add": "You can direct the beams at the same target or at different ones. Make a separate Attack Roll for each beam."
                },
                "17": {
                    "value": "4 beams",
                    "desc_add": "You can direct the beams at the same target or at different ones. Make a separate Attack Roll for each beam."
                }
            }
        },
        {
            "name": "Fire Bolt",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Circle of the Land Druid", "Lore Bard",
                           "Eldritch Knight Fighter", "Evoker Wizard"],
            "sources": ["Elf", "Tiefling", "Magic Initiate", "Pact Of The Tome"],
            "action": "Action",
            "range": "120ft",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "You hurl a mote of fire at a creature or an object within range. Make a Ranged Spell Attack against the target. On a hit, the target takes 1d10 Fire damage. A flammable object hit by this spell starts burning if it isn't being worn or carried.",
            "damage": "1d10",
            "damage_type": "Fire",
            "attack_type": "Ranged Spell",
            "scaling": {
                "5": {"value": "2d10"},
                "11": {"value": "3d10"},
                "17": {"value": "4d10"}
            }
        },
        {
            "name": "Guidance",
            "school": "Divination",
            "classes": ["Cleric", "Druid"],
            "subclasses": ["Circle of the Stars Druid", "Lore Bard"],
            "sources": ["Elf", "Blessed Warrior", "Druidic Warrior", "Magic Initiate", "Pact Of The Tome"],
            "action": "Action",
            "range": "Touch",
            "components": ["V", "S"],
            "duration": "Concentration, up to 1 minute",
            "description": "You touch a willing creature and choose a skill. Until the spell ends, the creature adds 1d4 to any ability check using the chosen skill.",
            "damage": "1d4",
            "damage_type": "Buff"
        },
        {
            "name": "Light",
            "school": "Evocation",
            "classes": ["Bard", "Cleric", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Celestial Warlock", "Lore Bard", "Eldritch Knight Fighter", "Evoker Wizard"],
            "sources": ["Aasimar", "Elf", "Blessed Warrior", "Magic Initiate", "Pact Of The Tome"],
            "action": "Action",
            "range": "Touch",
            "components": ["V"],
            "duration": "1 hour",
            "description": "You touch one Large or smaller object that isn't being worn or carried by someone else. Until the spell ends, the object sheds Bright Light in a 20ft radius and Dim Light for an additional 20ft. The light can be colored as you like. Covering the object with something opaque blocks the light. The spell ends if you cast it again."
        },
        {
            "name": "Mage Hand",
            "school": "Conjuration",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"],
            "sources": ["Elf", "Magic Initiate", "Telekinetic", "Pact Of The Tome"],
            "action": "Action",
            "range": "30ft",
            "components": ["V", "S"],
            "duration": "10 Rounds",
            "description": "A spectral, floating hand appears at a point you choose within range. The hand lasts for the duration. The hand vanishes if it is ever more than 30ft away from you or if you cast this spell again. When you cast the spell, you can use the hand to manipulate an object, open an unlocked door or container, stow or retrieve an item from an open container, or pour the contents out of a vial. As a Magic action on your later turns, you can control the hand thus again. As part of that action, you can move the hand up to 30ft. The hand can't attack, activate magic items, or carry more than 10 pounds."
        },
        {
            "name": "Mending",
            "school": "Transmutation",
            "classes": ["Bard", "Cleric", "Druid", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"],
            "sources": ["Elf", "Blessed Warrior", "Druidic Warrior", "Magic Initiate", "Pact Of The Tome"],
            "action": "Short or Long Rest",
            "range": "Touch",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "This spell repairs a single break or tear in an object you touch, such as a broken chain link, two halves of a broken key, a torn cloak, or a leaking wineskin. As long as the break or tear is no larger than 1 foot in any dimension, you mend it, leaving no trace of the former damage. This spell can physically repair a magic item, but it can't restore magic to such an object."
        },
        {
            "name": "Mind Sliver",
            "school": "Enchantment",
            "classes": ["Sorcerer", "Warlock", "Wizard"],
            "action": "Action",
            "range": "60ft",
            "components": ["V"],
            "duration": "Instant",
            "description": "You try to temporarily sliver the mind of one creature you can see within range. The target must succeed on an Intelligence saving throw or take 1d6 Psychic damage and substract 1d4 from the next saving throw it makes before the end of your next turn.",
            "damage": "1d6",
            "damage_type": "Psychic",
            "scaling": {
                "5": {"value": "2d6"},
                "11": {"value": "3d6"},
                "17": {"value": "4d6"}
            }
        },
        {
            "name": "Poison Spray",
            "school": "Necromancy",
            "classes": ["Druid", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "Action",
            "range": "30ft",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "You spray toxic mist at a creature within range. Make a Ranged Spell Attack against the target. On a hit, the target takes 1d12 Poison damage.",
            "damage": "1d12",
            "damage_type": "Poison",
            "attack_type": "Ranged Spell",
            "scaling": {
                "5": {"value": "2d12"},
                "11": {"value": "3d12"},
                "17": {"value": "4d12"}
            }
        },
        {
            "name": "Produce Flame",
            "school": "Conjuration",
            "classes": ["Druid"],
            "subclasses": [],
            "sources": [],
            "action": "Bonus Action",
            "range": "Self",
            "components": ["V", "S"],
            "duration": "Until end of Encounter",
            "description": "A flickering flame appears in your hand and remains there for the duration. While there, the flame emits no heat and ignites nothing, and it sheds Bright Light in a 20ft radius and Dim Light for an additional 20ft. The spell ends if you cast it again. Until the spell ends, you can take a Magic action to hurl fire at a creature or an object within 60ft of you. Make a Ranged Spell Attack. On a hit, the target takes 1d8 Fire damage.",
            "damage": "1d8",
            "damage_type": "Fire",
            "attack_type": "Ranged Spell",
            "scaling": {
                "5": {"value": "2d8"},
                "11": {"value": "3d8"},
                "17": {"value": "4d8"}
            }
        },
        {
            "name": "Ray Of Frost",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"],
            "action": "Action",
            "range": "60ft",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "A frigid beam of blue-white light streaks toward a creature within range. Make a Ranged Spell Attack against the target. On a hit, it takes 1d8 Cold damage, and its Speed is reduced by 10ft until the start of your next turn.",
            "damage": "1d8",
            "damage_type": "Cold",
            "attack_type": "Ranged Spell",
            "scaling": {
                "5": {"value": "2d8"},
                "11": {"value": "3d8"},
                "17": {"value": "4d8"}
            }
        },
        {
            "name": "Resistance",
            "school": "Abjuration",
            "classes": ["Cleric", "Druid"],
            "subclasses": [],
            "sources": [],
            "action": "Action",
            "range": "Touch",
            "components": ["V", "S"],
            "duration": "Concentration, up to 10 Rounds",
            "description": "You touch a willing creature and choose a damage type: Acid, Bludgeoning, Cold, Fire, Lightning, Necrotic, Piercing, Poison, Radiant, Slashing, or Thunder. When the creature takes damage of the chose type before the spell ends, the creature reduces the total damage taken by 1d4. A creature can benefit from this spell only once per turn.",
            "damage": "1d4",
            "damage_type": "Debuff"
        },
        {
            "name": "Sacred Flame",
            "school": "Evocation",
            "classes": ["Cleric"],
            "subclasses": [],
            "sources": [],
            "action": "Action",
            "range": "60ft",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "Flame-like radiance descends on a creature that you can see within range. The target must succeed on a Dexterity saving throw or take 1d8 Radiant damage. The target gains no benefit from Half Cover or Three-Quarters Cover for this save.",
            "damage": "1d8",
            "damage_type": "Radiant",
            "scaling": {
                "5": {"value": "2d8"},
                "11": {"value": "3d8"},
                "17": {"value": "4d8"}
            }
        },
        {
            "name": "Shillelagh",
            "school": "Transmutation",
            "classes": ["Druid"],
            "subclasses": [],
            "sources": [],
            "action": "Bonus Action",
            "range": "Self",
            "components": ["V", "S"],
            "duration": "10 Rounds",
            "description": "A Club or Quarterstaff you are holding is imbued with nature's power. For the duration, you can use your spellcasting ability instead of Strength for the attack and damage rolls of melee attacks using that weapon, and the weapon's damage die becomes a d8. If the attack deals damage, it can be Force damage or the weapon's normal damage type (your choice). The spell ends early if you cast it again or if you let go of the weapon.",
            "damage": "1d8",
            "damage_type": "Force/Weapon",
            "scaling": {
                "5": {"value": "d10"},
                "11": {"value": "d12"},
                "17": {"value": "2d6"}
            }
        },
        {
            "name": "Shocking Grasp",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"],
            "action": "Action",
            "range": "Touch",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "Lightning springs from you to a creature that you try to touch. Make a Melee Spell Attack against the target. On a hit, the target takes 1d8 Lightning damage, and it can't make Opportunity Attacks until the start of its next turn.",
            "damage": "1d8",
            "damage_type": "Lightning",
            "attack_type": "Melee Spell",
            "scaling": {
                "5": {"value": "2d8"},
                "11": {"value": "3d8"},
                "17": {"value": "4d8"}
            }
        },
        {
            "name": "Sorcerous Burst",
            "school": "Evocation",
            "classes": ["Sorcerer"],
            "action": "Action",
            "range": "120ft",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "You cast sorcerous energy at one creature or object within range. Make a Ranged Attack roll against the target. On a hit, the target takes 1d8 damage of a type you choose: Acid, Cold, Fire, Lightning, Poison, Psychic, or Thunder. If you roll an 8 on a d8 for this spell, you can roll another d8, and add it to the damage. When you cast this spell, the maximum number of these d8s you can add to the spell's damage equals to your spellcasting ability modifier.",
            "damage": "1d8",
            "damage_type": "Choice",
            "attack_type": "Ranged Attack",
            "scaling": {
                "5": {"value": "2d8"},
                "11": {"value": "3d8"},
                "17": {"value": "4d8"}
            }
        },
        {
            "name": "Spare The Dying",
            "school": "Necromancy",
            "classes": ["Cleric", "Druid"],
            "subclasses": [],
            "sources": [],
            "action": "Action",
            "range": "15ft",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "Choose a creature within range that has 0 Hit Points and isn't dead. The creature becomes Stable.",
            "scaling": {
                "5": {"value": "30ft"},
                "11": {"value": "60ft"},
                "17": {"value": "120ft"}
            }
        },
        {
            "name": "Starry Wisp",
            "school": "Evocation",
            "classes": ["Bard", "Druid"],
            "subclasses": [],
            "sources": [],
            "action": "Action",
            "range": "60ft",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "You launch a mote of light at one creature or object within range. Make a Ranged Spell Attack against the target. On a hit, the target takes 1d8 Radiant damage, and until the end of your next turn, it emits Dim Light in a 10ft radius and can't benefit from the Invisible condition.",
            "damage": "1d8",
            "damage_type": "Radiant",
            "attack_type": "Ranged Spell",
            "scaling": {
                "5": {"value": "2d8"},
                "11": {"value": "3d8"},
                "17": {"value": "4d8"}
            }
        },
        {
            "name": "Thorn Whip",
            "school": "Transmutation",
            "classes": ["Druid"],
            "subclasses": [],
            "sources": [],
            "action": "Action",
            "range": "30ft",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "You create a vine-like whip covered in thorns that lashes out at your command toward a creature within range. Make a Melee Spell Attack against the target. On a hit, the target takes 1d6 Piercing damage, and if it is Large or smaller, you can pull it up to 10ft closer to you.",
            "damage": "1d6",
            "damage_type": "Piercing",
            "attack_type": "Melee Spell",
            "scaling": {
                "5": {"value": "2d6"},
                "11": {"value": "3d6"},
                "17": {"value": "4d6"}
            }
        },
        {
            "name": "Thunderclap",
            "school": "Evocation",
            "classes": ["Bard", "Druid", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "Action",
            "range": "Self",
            "components": ["S"],
            "duration": "Instant",
            "description": "Each creature in a 5ft Emanation originating from you must succeed on a Constitution saving throw or take 1d6 Thunder damage. The spell's thunderous sound can be heard up to 100ft away.",
            "damage": "1d6",
            "damage_type": "Thunder",
            "scaling": {
                "5": {"value": "2d6"},
                "11": {"value": "3d6"},
                "17": {"value": "4d6"}
            }
        },
        {
            "name": "Toll The Dead",
            "school": "Necromancy",
            "classes": ["Cleric", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "Action",
            "range": "60ft",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "You point at one creature you can see within range, and the single chime of a dolorous bell is audible within 10ft of the target. The target must succeed on a Wisdom saving throw or take 1d8 Necrotic damage. If the target is missing any of its Hit Points, it instead takes 1d12 Necrotic damage.",
            "damage": "1d8 or 1d12",
            "damage_type": "Necrotic",
            "scaling": {
                "5": {"value": "2d8 or 2d12"},
                "11": {"value": "3d8 or 3d12"},
                "17": {"value": "4d8 or 4d12"}
            }
        },
        {
            "name": "True Strike",
            "school": "Divination",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "Action",
            "range": "Self",
            "components": ["S", "M (a weapon with which you have proficiency and that is worth 1+ CP)"],
            "duration": "Instant",
            "description": "Guided by a flash of magical insight, you make one attack with the weapon used in the spell's casting. The attack uses your spellcasting ability for the attack and damage rolls instead of using Strength or Dexterity. If the attack deals damage, it can be Radiant damage or the weapon's normal damage type (your choice).",
            "damage": "Weapon",
            "damage_type": "Radiant/Weapon",
            "scaling": {
                "5": {"value": "1d6 extra Radiant"},
                "11": {"value": "2d6 extra Radiant"},
                "17": {"value": "3d6 extra Radiant"}
            }
        },
        {
            "name": "Vicious Mockery",
            "school": "Enchantment",
            "classes": ["Bard"],
            "subclasses": [],
            "sources": [],
            "action": "Action",
            "range": "60ft",
            "components": ["V"],
            "duration": "Instant",
            "description": "You unleash a string of insults laced with subtle enchantments at one creature you can see or hear within range. The target must succeed on a Wisdom saving throw or take 1d6 Psychic damage and have Disadvantage on the next Attack Roll it makes before the end of its next turn.",
            "damage": "1d6",
            "damage_type": "Psychic",
            "scaling": {
                "5": {"value": "2d6"},
                "11": {"value": "3d6"},
                "17": {"value": "4d6"}
            }
        },
        {
            "name": "Word Of Radiance",
            "school": "Evocation",
            "classes": ["Cleric"],
            "subclasses": [],
            "sources": [],
            "action": "Action",
            "range": "Self",
            "components": ["V"],
            "duration": "Instant",
            "description": "Burning radiance erupts from you in a 5ft Emanation. Each creature of your choice that you can see in it must succeed on a Constitution saving throw or take 1d6 Radiant damage.",
            "damage": "1d6",
            "damage_type": "Radiant",
            "scaling": {
                "5": {"value": "2d6"},
                "11": {"value": "3d6"},
                "17": {"value": "4d6"}
            }
        },
    ],
    1: [
        {
            "name": "Armor Of Agathys",
            "school": "Abjuration",
            "classes": ["Warlock"],
            "action": "Bonus Action",
            "range": "Self",
            "components": ["V", "S"],
            "duration": "Until Rest taken",
            "description": "Protective magical frost surrounds you. You gain 5 Temporary Hit Points. If a creature hits you with a Melee Attack Roll before the spell ends, the creature takes 5 Cold damage. The spell ends early if you have no Temporary Hit Points.",
            "damage": "5",
            "damage_type": "Cold",
            "level_upgrade": "The Temporary Hit Points and the Cold damage both increase by 5 for each spell slot level above 1."
        },
        {
            "name": "Arms Of Hadar",
            "school": "Conjuration",
            "classes": ["Warlock"],
            "subclasses": ["Aberrant Sorcerer"],
            "action": "Action",
            "range": "Self",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "Invoking Hadar, you cause tendrils to erupt from yourself. Each creature in a 10ft Emanation originating from you makes a Strength saving throw. On a failed save, a target takes 2d6 Necrotic damage and can't take Reactions until the start of its next turn. On a successful save, a target takes half as much damage only.",
            "damage": "2d6",
            "damage_type": "Necrotic",
            "level_upgrade": "The damage increases by 1d6 for each spell slot level above 1."
        },
        {
            "name": "Bane",
            "school": "Enchantment",
            "classes": ["Bard", "Cleric", "Warlock"],
            "subclasses": ["Lore Bard", "Vengeance Paladin"],
            "action": "Action",
            "range": "30ft",
            "components": ["V", "S"],
            "duration": "Concentration, up to 10 Rounds",
            "description": "Up to three creatures of your choice that you can see within range must each make a Charisma saving throw. Whenever a target that fails this save makes an attack roll or a saving throw before the spell ends, the target must substract 1d4 from the attack roll or save.",
            "damage": "1d4",
            "damage_type": "Debuff",
            "level_upgrade": "You can target one additional creature for each spell slot level above 1."
        },
        {
            "name": "Bless",
            "school": "Enchantment",
            "classes": ["Cleric", "Paladin"],
            "subclasses": ["Lore Bard", "Life Cleric"],
            "action": "Action",
            "range": "30ft",
            "components": ["V", "S", "M (a Holy Symbol worth 5+ GP)"],
            "duration": "Concentration, up to 10 Rounds",
            "description": "You bless up to three creatures within range. Whenever a target makes an Attack Roll or a saving throw before the spell ends, the target adds 1d4 to the Attack Roll or save.",
            "damage": "1d4",
            "damage_type": "Buff",
            "level_upgrade": "You can target one additional creature for each spell slot level above 1."
        },
        {
            "name": "Burning Hands",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Circle of the Land Druid", "Lore Bard",
                           "Eldritch Knight Fighter", "Evoker Wizard", "Fiend Warlock", "Light Cleric"],
            "action": "Action",
            "range": "Self",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "A thin sheet of flames shoots forth from you. Each creature in a 15ft Cone makes a Dexterity saving throw, taking 3d6 Fire damage on a failed save or half as much damage on a successful one. Flammable objects in the Cone that aren't being worn or carried start burning.",
            "damage": "3d6",
            "damage_type": "Fire",
            "level_upgrade": "The damage increases by 1d6 for each spell slot level above 1."
        },
        {
            "name": "Charm Person",
            "school": "Enchantment",
            "classes": ["Bard", "Druid", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Glamour Bard", "Lore Bard", "Eldritch Knight Fighter",
                           "Fey Wanderer Ranger", "Trickery Cleric"],
            "action": "Action",
            "range": "30ft",
            "components": ["V", "S"],
            "duration": "Until Rest taken",
            "description": "One Humanoid you can see within range makes a Wisdom saving throw. On a failed save, the target has the Charmed condition until the spell ends or until you or your allies damage it. The Charmed creature is Friendly to you. When the spell ends, the target knows it was Charmed by you.",
            "level_upgrade": "You can target one additional creature for each spell slot level above 1."
        },
        {
            "name": "Chromatic Orb",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Draconic Sorcerer", "Eldritch Knight Fighter",
                           "Evoker Wizard"],
            "action": "Action",
            "range": "90ft",
            "components": ["V", "S", "M (a diamond worth 50+ GP)"],
            "duration": "Instant",
            "description": "You hurl an orb of energy at a target within range. Choose Acid, Cold, Fire, Lightning, Poison, or Thunder for the type of orb you create, and then make a Ranged Spell Attack against the target. On a hit, the target takes 3d8 damage of the chosen type. If you roll the same number on two or more of the d8s, the orb leaps to a different target of your choice within 30ft of the target. Make an Attack Roll against the new target, and make a new damage roll. The orb can't leap again unless you cast the spell with a level 2+ spell slot.",
            "damage": "3d8",
            "damage_type": "Choice",
            "attack_type": "Ranged Spell",
            "level_upgrade": "The damage increases by 1d8 for each spell slot level above 1. The orb can leap a maximum number of times equal to the level of the slot expended, and a creature can be targeted only once by each casting of this spell."
        },
        {
            "name": "Color Spray",
            "school": "Illusion",
            "classes": ["Bard", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter", "Illusionist Wizard"],
            "action": "Action",
            "range": "Self",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "You launch a dazzling array of flashing, colorful light. Each creature in a 15ft Cone originating from you must succeed on a Constitution saving throw or have the Blinded condition until the end of the your next turn."
        },
        {
            "name": "Command",
            "school": "Enchantment",
            "classes": ["Bard", "Cleric", "Paladin"],
            "subclasses": ["Glamour Bard", "Lore Bard", "Draconic Sorcerer", "Fiend Warlock"],
            "action": "Action",
            "range": "60ft",
            "components": ["V"],
            "duration": "Instant",
            "description": "You speak a one-word command to a creature you can see within range. The target must succeed on a Wisdom saving throw or follow the command on its next turn. Choose the command from these options: Approach, Drop, Flee, Grovel, Halt.",
            "level_upgrade": "You can affect one additional creature for each spell slot level above 1."
        },
        {
            "name": "Compelled Duel",
            "school": "Enchantment",
            "classes": ["Paladin"],
            "action": "Bonus Action",
            "range": "30ft",
            "components": ["V"],
            "duration": "Concentration, up to 10 Rounds",
            "description": "You try to compel a creature into a duel. One creature that you can see within range makes a Wisdom saving throw. On a failed save, the target has Disadvantage on Attack Rolls against creatures other than you, and it can't willingly move to a space that is more than 30ft away from you. The spell ends if you make an Attack Roll against a creature other than the target, if you cast a spell on an enemy other than the target, if an ally of yourse damages the target, or if you end your turn more than 30ft away from the target."
        },
        {
            "name": "Cure Wounds",
            "school": "Abjuration",
            "classes": ["Bard", "Cleric", "Druid", "Paladin", "Ranger"],
            "subclasses": ["Celestial Warlock", "Circle of the Moon Druid", "Lore Bard", "Life Cleric"],
            "action": "Action",
            "range": "Touch",
            "components": ["V", "S"],
            "duration": "Instant",
            "description": "A creature you touch regains a number of Hit Points equal to 2d8 plus your spellcasting ability modifier.",
            "damage": "2d8",
            "damage_type": "Healing",
            "level_upgrade": "The healing increases by 2d8 for each spell slot level above 1."
        },
        {
            "name": "Detect Evil And Good",
            "school": "Divination",
            "classes": ["Cleric", "Paladin"],
            "subclasses": ["Lore Bard"],
            "action": "Action",
            "range": "Self",
            "components": ["V", "S"],
            "duration": "Concentration, until end of current Encounter",
            "description": "For the duration, you sense the location of any Aberration, Celestial, Elemental, Fey, Fiend, or Undead within 30ft of yourself. You also sense whether the Hallow spell is active there and, if so, where."
        },
        {
            "name": "Detect Magic",
            "school": "Divination",
            "classes": ["Bard", "Cleric", "Druid", "Paladin", "Ranger", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Diviner Wizard", "Eldritch Knight Fighter"],
            "action": "Action",
            "range": "Self",
            "components": ["V", "S"],
            "duration": "Concentration, until end of current Encounter",
            "description": "For the duration, you sense the presence of magical effects within 30ft of yourself. If you sense such effects, you can take the Magic action to see a faint aura around any visible creature or object in the area that bears the magic, and if an effect was creature by a spell, you learn the spell's school of magic."
        },
        {
            "name": "Dissonant Whispers",
            "school": "Enchantment",
            "classes": ["Bard"],
            "subclasses": ["Aberrant Sorcerer", "Great Old One Warlock"],
            "action": "Action",
            "range": "60ft",
            "components": ["V"],
            "duration": "Instant",
            "description": "One creature of your choice that you can see within range hears a discordant melody in its mind. The target makes a Wisdom saving throw. On a failed save, it takes 3d6 Psychic damage and must immediately use its Reaction, if available, to move as far away from you as it can, using the safest route. On a successful save, the target takes half as much damage only.",
            "damage": "3d6",
            "damage_type": "Psychic",
            "level_upgrade": "The damage increases by 1d6 for each spell slot level above 1."
        },
        {
            "name": "Divine Favor",
            "school": "Transmutation",
            "classes": ["Paladin"],
            "action": "Bonus Action",
            "range": "Self",
            "components": ["V", "S"],
            "duration": "10 Rounds",
            "description": "Until the spell ends, your attacks with weapons deal an extra 1d4 Radiant damage on a hit.",
            "damage": "1d4",
            "damage_type": "Radiant"
        },
        {
            "name": "Divine Smite",
            "school": "Evocation",
            "classes": ["Paladin"],
            "action": "Bonus Action, which you take immediately after hitting a target with a Melee weapon or an Unarmed Strike",
            "range": "Self",
            "components": ["V"],
            "duration": "Instant",
            "description": "The target takes an extra 2d8 Radiant damage from the attack. The damage increases by 1d8 if the target is a Fiend or an Undead.",
            "damage": "2d8",
            "damage_type": "Radiant",
            "level_upgrade": "The damage increases by 1d8 for each spell slot level above 1."
        },
        {
            "name": "Ensnaring Strike",
            "school": "Conjuration",
            "classes": ["Ranger"],
            "subclasses": ["Ancients Paladin"],
            "action": "Bonus Action, which you take immediately after hitting a creature with a weapon",
            "range": "Self",
            "components": ["V"],
            "duration": "Concentration, up to 10 Rounds",
            "description": "As you hit the target, grasping vines appear on it, and it makes a Strength saving throw. A Large or larger creature has Advantage on this save. On a failed save, the target has the Restrained condition until the spell ends. On a successful save, the vines shrivel away, and the spell ends. While Restrained, the target takes 1d6 Piercing damage at the start of each of its turns. The target or a creature within reach of it can take an action to make a Strength (Athletics) check against you spell save DC. On a success, the spell ends.",
            "damage": "1d6",
            "damage_type": "Piercing",
            "level_upgrade": "The damage increases by 1d6 for each spell slot level above 1."
        },
        {
            "name": "Entangle",
            "school": "Conjuration",
            "classes": ["Druid", "Ranger"],
            "subclasses": ["Lore Bard"],
            "action": "Action",
            "range": "90ft",
            "components": ["V", "S"],
            "duration": "Concentration, up to 10 Rounds",
            "description": "Grasping plants sprout from the ground in a 20ft square within range. For the duration, these plants turn the ground in the area into Difficutl Terrain. They disappear when the spell ends. Each creature (other than you) in the area when you cast the spell must succeed on a Strength saving throw or have the Restrained condition until the spell ends."
        },
        {
            "name": "Expeditious Retreat",
            "school": "Transmutation",
            "classes": ["Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"],
            "action": "Bonus Action",
            "range": "Self",
            "components": ["V", "S"],
            "duration": "Concentration, until end of current Encounter",
            "description": "You take the Dash Action, and until the spell ends, you can take that Action again as a Bonus Action."
        },
        {
            "name": "Faerie Fire",
            "school": "Evocation",
            "classes": ["Bard", "Druid"],
            "subclasses": ["Archfey Warlock", "Lore Bard", "Light Cleric"],
            "action": "Action",
            "range": "60ft",
            "components": ["V"],
            "duration": "Concentration, up to 10 Rounds",
            "description": "Objects in a 20ft Cube within range are outlined in blue, green, or violet light (your choice). Each creature in the Cube is also outlined if it fails a Dexterity saving throw. For the duration, objects and affected creatures she Dim Light in a 10ft radius and can't benefit from the Invisible condition. Attack rolls against an effected creature or object have Advantage if the attacker can see it."
        },
        {
            "name": "False Life",
            "school": "Necromancy",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"],
            "action": "Action",
            "range": "Self",
            "components": ["V", "S"],
            "duration": "Instantaneous",
            "description": "You gain 2d4 + 4 Temporary Hit Points.",
            "damage": "2d4+4",
            "damage_type": "Healing",
            "level_upgrade": "You gain 5 additional Temporary Hit Points for each spell slot level above 1."
        },
        {
            "name": "Feather Fall",
            "school": "Transmutation",
            "classes": ["Bard", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"],
            "action": "Reaction",
            "range": "60ft",
            "components": ["V"],
            "duration": "10 Rounds",
            "description": "Choose up to five falling creatures within range. A falling creature's rate of descent slows to 60ft per Round until the spell ends. If a creature lands before the spell ends, the creature takes no damage from the fall, and the spell ends for that creature."
        },
        {
            "name": "Find Familiar",
            "school": "Conjuration",
            "classes": ["Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"],
            "action": "Before or after an Encounter",
            "range": "10ft",
            "components": ["V", "S", "M (10+GP)"],
            "duration": "Instantaneous",
            "description": "You gain the service of a familiar, a spirit that takes an animal form you choose. The familiar has the statistics of the chosen form, though it is a Celestial, Fey, or Fiend (your choice) instead of a Beast. While your familiar is within 100ft of you, you can communicate with it telepathically. As a Bonus Action, you can see through its eyes and hear what it hears until the start of your next turn. When you cast a spell with a range of touch, your familiar can deliver the touch using its Reaction. It rolls its own Initiative and acts on its own turn. It can't attack. If it drops to 0 Hit Points, it disappears. Reappears after casting this spell again."
        },
        {
            "name": "Fog Cloud",
            "school": "Conjuration",
            "classes": ["Druid", "Ranger", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Circle of the Land Druid", "Sea Druid", "Lore Bard",
                           "Eldritch Knight Fighter"],
            "action": "Action",
            "range": "120ft",
            "components": ["V", "S"],
            "duration": "Concentration, up until the end of the current Encounter",
            "description": "You create a 20ft radius Sphere of fog centered on a point within range. The Sphere is Heavily Obscured. It lasts for the duration or until a strong wind disperses it.",
            "level_upgrade": "The fog's radius increases by 20ft for each spell slot level above 1."
        },
        {
            "name": "Goodberry",
            "school": "Conjuration",
            "classes": ["Druid", "Ranger"],
            "subclasses": ["Lore Bard"],
            "action": "Action",
            "range": "Touch",
            "components": ["V", "S"],
            "duration": "Until taking a Long Rest",
            "description": "Ten berries appear in your hand and are infused with magic for the duration. A creature can take a Bonus Action to eat one berry. Eating a berry restores 1 Hit Point. Uneaten berries disappear when the spell ends.",
            "damage": "1",
            "damage_type": "Healing"
        },
        {
            "name": "Grease",
            "school": "Conjuration",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"],
            "action": "Action",
            "range": "60ft",
            "components": ["V", "S"],
            "duration": "10 Rounds",
            "description": "Nonflammable grease covers the ground in a 10ft square centered on a point within range and turns it into Difficult Terrain for the duration. When the grease appears, each creature standing in its area must succeed on a Dexterity saving throw or have the Prone condition. A creature that enters the area or ends its turn there must also succeed on that save or fall Prone."
        },
        {
            "name": "Guiding Bolt",
            "school": "Evocation",
            "classes": ["Cleric"],
            "subclasses": ["Celestial Warlock", "Circle of the Stars Druid", "Lore Bard", "Glory Paladin",
                           "War Cleric"],
            "action": "Action",
            "range": "120ft",
            "components": ["V", "S"],
            "duration": "1 Rounds",
            "description": "You hurl a bolt of light toward a creature within range. Make a Ranged Spell Attack against the target. On a hit, it takes 4d6 Radiant damage, and the next Attack Roll made against it before the end of your next turn has Advantage.",
            "damage": "4d6",
            "damage_type": "Radiant",
            "attack_type": "Ranged Spell",
            "level_upgrade": "The damage increases by 1d6 for each spell slot level above 1."
        },
        {
            "name": "Hail Of Thorns",
            "school": "Conjuration",
            "classes": ["Ranger"],
            "action": "Bonus Action, which you take immediately after hitting a creature with a Ranged weapon",
            "range": "Self",
            "components": ["V"],
            "duration": "Instantaneous",
            "description": "As you hit the creature, this spell creates a rain of thorns that sprouts from your Ranged weapon or ammunition. The target of the attack and each creature within 5ft of it make a Dexterity saving throw, taking 1d10 Piercing damage on a failed save or half as much damage on a successful one.",
            "damage": "1d10",
            "damage_type": "Piercing",
            "level_upgrade": "The damage increases by 1d10 for each spell slot level above 1."
        },
        {
            "name": "Healing Word",
            "school": "Abjuration",
            "classes": ["Bard", "Cleric", "Druid"],
            "subclasses": ["Lore Bard"],
            "action": "Bonus Action",
            "range": "60ft",
            "components": ["V"],
            "duration": "Instantaneous",
            "description": "A creature of your choice that you can see within range regains Hit Points equal to 2d4 plus your spellcasting ability modifier.",
            "damage": "2d4",
            "damage_type": "Healing",
            "level_upgrade": "The healing increases by 2d4 for each spell slot level above 1."
        },
        {
            "name": "Hellish Rebuke",
            "school": "Evocation",
            "classes": ["Warlock"],
            "action": "Reaction, which you take in response to taking damage from a creature that you can see within 60ft of yourself",
            "range": "60ft",
            "components": ["V", "S"],
            "duration": "Instantaneous",
            "description": "The creature that damaged you is momentarily surrounded by green flames. It makes a Dexterity saving throw, taking 2d10 Fire damage on a failed save or half as much damage on a successful one.",
            "damage": "2d10",
            "damage_type": "Fire",
            "level_upgrade": "The damage increases by 1d10 for each spell slot level above 1."
        },
        {
            "name": "Heroism",
            "school": "Enchantment",
            "classes": ["Bard", "Paladin"],
            "subclasses": ["Glory Paladin"],
            "action": "Action",
            "range": "Touch",
            "components": ["V", "S"],
            "duration": "Concentration, up to 10 Rounds",
            "description": "A willing creature you touch is imbued with bravery. Until the spell ends, the creature is immune to the Frightened condition and gains Temporary Hit Points equal to your spellcasting ability modifier at the start of each of its turns.",
            "damage_type": "Healing",
            "level_upgrade": "You can target one additional creature for each spell slot level above 1."
        },
        {
            "name": "Hex",
            "school": "Enchantment",
            "classes": ["Warlock"],
            "subclasses": ["Great Old One Warlock"],
            "action": "Bonus Action",
            "range": "90ft",
            "components": ["V", "S"],
            "duration": "Concentration, until the end of the current Encounter",
            "description": "You place a curse on a creature that you can see within range. Until the spell ends, you deal an extra 1d6 Necrotic damage to the target whenever you hit it with an attack roll. Also, choose one ability when you cast the spell. The target has Disadvantage on ability checks made with the chosen ability. If the target drops to 0 Hit Points before this spell ends, you can take a Bonus Action on a later turn to curse a new creature.",
            "damage": "1d6",
            "damage_type": "Necrotic"
        },
        {
            "name": "Hunter's Mark",
            "school": "Divination",
            "classes": ["Ranger"],
            "subclasses": ["Vengeance Paladin"],
            "action": "Bonus Action",
            "range": "90ft",
            "components": ["V"],
            "duration": "Concentration, until the end of the current Encounter",
            "description": "You magically mark one creature you can see within range as your quarry. Until the spell ends, you deal an extra 1d6 Force damage to the target whenever you hit it with an attack roll. You also have Advantage on any Wisdom checks you make to find it. If the target drops to 0 Hit Points before this spell ends, you can take a Bonus Action to move the mark to a new creature you can see within range.",
            "damage": "1d6",
            "damage_type": "Force"
        },
        {
            "name": "Ice Knife",
            "school": "Conjuration",
            "classes": ["Druid", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"],
            "action": "Action",
            "range": "60ft",
            "components": ["S"],
            "duration": "Instantaneous",
            "description": "You create a shard of ice and fling it at one creature within range. Make a Ranged Spell Attack against the target. On a hit, the target takes 1d10 Piercing damage. Hit or miss, the shard then explodes. The target and each creature within 5ft of it must succeed on a Dexterity saving throw or take 2d6 Cold damage.",
            "damage": "1d10 / 2d6",
            "damage_type": "Piercing / Cold",
            "attack_type": "Ranged Spell",
            "level_upgrade": "The Cold damage increases by 1d6 for each spell slot level above 1."
        },
        {
            "name": "Identify",
            "school": "Divination",
            "classes": ["Bard", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "Before or after an Encounter",
            "range": "Touch",
            "components": ["V", "S", "M (a pearl worth 100+GP)"],
            "duration": "Instantaneous",
            "description": "You touch an object throughout the spell's casting. If the object is a magic item or some other magical object, you learn its properties and how to use them, whether it requires Attunement, and how many charges it has, if any. You learn whether any ongoing spells are affecting the item and what they are. If the item was created by a spell, you learn that spell's name. If you instead touch a creature throughout the casting, you learn which ongoing spells, if any, are currently affecting it."
        },
        {
            "name": "Inflict Wounds",
            "school": "Necromancy",
            "classes": ["Cleric"],
            "subclasses": ["Lore Bard"],
            "action": "Action",
            "range": "Touch",
            "components": ["V", "S"],
            "duration": "Instantaneous",
            "description": "A creature you touch makes a Constitution saving throw, taking 2d10 Necrotic damage on a failed save or half as much damage on a successful one.",
            "damage": "2d10",
            "damage_type": "Necrotic",
            "level_upgrade": "The damage increases by 1d10 for each spell slot level above 1."
        },
        {
            "name": "Jump",
            "school": "Transmutation",
            "classes": ["Druid", "Ranger", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"],
            "action": "Bonus Action",
            "range": "Touch",
            "components": ["V", "S"],
            "duration": "10 Rounds",
            "description": "You touch a willing creature. Once on each of its turns until the spell ends, that creature can jump up to 30ft by spending 10ft of movement.",
            "level_upgrade": "You can target one additional creature for each spell slot level above 1."
        },
        {
            "name": "Longstrider",
            "school": "Transmutation",
            "classes": ["Bard", "Druid", "Ranger", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "Action",
            "range": "Touch",
            "components": ["V", "S"],
            "duration": "Until end of current Encounter",
            "description": "You touch a creature. The target's Speed increases by 10ft until the spell ends.",
            "level_upgrade": "You can target one additional creature for each spell slot level above 1."
        },
        {
            "name": "Mage Armor",
            "school": "Abjuration",
            "classes": ["Sorcerer", "Wizard"],
            "action": "Action",
            "range": "Touch",
            "components": ["V", "S"],
            "duration": "Until Rest is taken",
            "description": "You touch a willing creature who isn't wearing armor. Until the spell ends, the target's base AC becomes 13 plus its Dexterity modifier. The spell ends early if the target dons armor."
        },
        {
            "name": "Magic Missile",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"],
            "action": "Action",
            "range": "120ft",
            "components": ["V", "S"],
            "duration": "Instantaneous",
            "description": "You create three glowing darts of magical force. Each dart strikes a creature of your choice that you can see within range. A dart deals 1d4 + 1 Force damage to its target. The darts all strike simultaneously, and you can direct them to hit one creature or several.",
            "damage": "1d4+1",
            "damage_type": "Force",
            "level_upgrade": "The spell creates one more dart for each spell slot level above 1."
        },
        {
            "name": "Protection From Evil And Good",
            "school": "Abjuration",
            "classes": ["Cleric", "Druid", "Paladin", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "Action",
            "range": "Touch",
            "components": ["V", "S", "M (a flask of Holy Water worth 25+GP, which the spell consumes)"],
            "duration": "Concentration, until end of current Encounter",
            "description": "Until the spell ends, one willing creature you touch is protected against creatures that are Aberrations, Celestials, Elementals, Fey, Fiends, or Undead. Creatures of those types have Disadvantage on Attack Rolls against the target. The target also can't be possessed by or gain the Charmed or Frightened conditions from them."
        },
        {
            "name": "Ray Of Sickness",
            "school": "Necromancy",
            "classes": ["Sorcerer", "Wizard"],
            "action": "Action",
            "range": "60ft",
            "components": ["V", "S"],
            "duration": "Instantaneous",
            "description": "You shoot a greenish ray at a creature within range. Make a Ranged Spell Attack against the target. On a hit, the target takes 2d8 Poison damage and has the Poisoned condition until the end of your next turn.",
            "damage": "2d8",
            "damage_type": "Poison",
            "attack_type": "Ranged Spell",
            "level_upgrade": "The damage increases by 1d8 for each spell slot level above 1."
        },
        {
            "name": "Sanctuary",
            "school": "Abjuration",
            "classes": ["Cleric"],
            "subclasses": [],
            "sources": [],
            "action": "Bonus Action",
            "range": "30ft",
            "components": ["V", "S"],
            "duration": "10 Rounds",
            "description": "You ward a creature within range. Until the spell ends, any creature who targets the warded creature with an Attack Roll or a damaging spell must succeed on a Wisdom saving throw or either choose a new target or lose the attack or spell. The spell ends if the warded creature makes an Attack Roll, casts a spell, or deals damage."
        },
        {
            "name": "Searing Smite",
            "school": "Evocation",
            "classes": ["Paladin"],
            "action": "Bonus Action, which you take immediately after hitting a target with a Melee weapon or an Unarmed Strike",
            "range": "Self",
            "components": ["V"],
            "duration": "10 Rounds",
            "description": "As you hit the target, it takes an extra 1d6 Fire damage from the attack. At the start of each of its turns until the spell ends, the target takes 1d6 Fire damage and then makes a Constitution saving throw. On a failed save, the spell continues. On a successful save, the spell ends.",
            "damage": "1d6",
            "damage_type": "Fire",
            "level_upgrade": "All the damage increases by 1d6 for each spell slot level above 1."
        },
        {
            "name": "Shield",
            "school": "Abjuration",
            "classes": ["Sorcerer", "Wizard"],
            "action": "Reaction, which you take when you are hit by an Attack Roll or targeted by the Magic Missile spell",
            "range": "Self",
            "components": ["V", "S"],
            "duration": "1 Round",
            "description": "An imperceptible barrier of magical force protects you. Until the start of your next turn, you have a +5 bonus to AC, including against the triggering attack, and you take no damage from Magic Missile.",
            "damage_type": "Buff"
        },
        {
            "name": "Shield Of Faith",
            "school": "Abjuration",
            "classes": ["Cleric", "Paladin"],
            "subclasses": [],
            "sources": [],
            "action": "Bonus Action",
            "range": "60ft",
            "components": ["V", "S"],
            "duration": "Concentration, until end of current Encounter",
            "description": "A shimmering field surrounds a creature of your choice within range, granting it a +2 bonus to AC for the duration."
        },
        {
            "name": "Sleep",
            "school": "Enchantment",
            "classes": ["Bard", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Tasha's Hideous Laughter",
            "school": "Enchantment",
            "classes": ["Bard", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Thunderous Smite",
            "school": "Evocation",
            "classes": ["Paladin"]
        },
        {
            "name": "Thunderwave",
            "school": "Evocation",
            "classes": ["Bard", "Druid", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "With Bolt",
            "school": "Evocation"
        },
        {
            "name": "Wrathful Smite",
            "school": "Necromancy",
            "classes": ["Paladin"]
        },
    ],
    2: [
        {
            "name": "Aid",
            "school": "Abjuration",
            "classes": ["Bard", "Cleric", "Druid", "Paladin", "Ranger"],
            "subclasses": ["Celestial Warlock", "Clockwork Sorcerer", "Lore Bard",
                           "Life Cleric", "Devotion Paladin"],
        },
        {
            "name": "Arcane Lock",
            "school": "Abjuration",
            "classes": ["Wizard"]
        },
        {
            "name": "Arcane Vigor",
            "school": "Abjuration",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Abjurer Wizard", "Arcane Trickster Rogue", "Lore Bard",
                           "Eldritch Knight Fighter"]
        },
        {
            "name": "Barkskin",
            "school": "Transmutation",
            "classes": ["Druid", "Ranger"],
            "subclasses": ["Lore Bard"]
        },
        {
            "name": "Blindness/Deafness",
            "school": "Transmutation",
            "classes": ["Bard", "Cleric", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"]
        },
        {
            "name": "Blur",
            "school": "Illusion",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Circle of the Land Druid", "Lore Bard",
                           "Eldritch Knight Fighter", "Illusionist Wizard"]
        },
        {
            "name": "Cloud Of Daggers",
            "school": "Conjuration",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"]
        },
        {
            "name": "Continual Flame",
            "school": "Evocation",
            "classes": ["Cleric", "Druid", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter", "Evoker Wizard"]
        },
        {
            "name": "Cordon Of Arrows",
            "school": "Transmutation",
            "classes": ["Ranger"]
        },
        {
            "name": "Crown Of Madness",
            "school": "Enchantment",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"]
        },
        {
            "name": "Darkness",
            "school": "Evocation",
            "classes": ["Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter", "Evoker Wizard",
                           "Shadow Monk"]
        },
        {
            "name": "Dragon's Breath",
            "school": "Transmutation",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Draconic Sorcerer",
                           "Eldritch Knight Fighter"]
        },
        {
            "name": "Enhance Ability",
            "school": "Transmutation",
            "classes": ["Bard", "Cleric", "Druid", "Ranger", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Enlarge/Reduce",
            "school": "Transmutation",
            "classes": ["Bard", "Druid", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"]
        },
        {
            "name": "Find Steed",
            "school": "Conjuration",
            "classes": ["Paladin"]
        },
        {
            "name": "Flame Blade",
            "school": "Evocation",
            "classes": ["Druid", "Sorcerer"],
            "subclasses": ["Lore Bard"]
        },
        {
            "name": "Flaming Sphere",
            "school": "Conjuration",
            "classes": ["Druid", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"]
        },
        {
            "name": "Gust Of Wind",
            "school": "Evocation",
            "classes": ["Druid", "Ranger", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Circle of the Sea Druid", "Lore Bard", "Eldritch Knight Fighter",
                           "Evoker Wizard"]
        },
        {
            "name": "Heat Metal",
            "school": "Transmutation",
            "classes": ["Bard", "Druid"],
            "subclasses": ["Lore Bard"]
        },
        {
            "name": "Hold Person",
            "school": "Enchantment",
            "classes": ["Bard", "Cleric", "Druid", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Circle of the Land Druid", "Lore Bard",
                           "Eldritch Knight Fighter", "Vengeance Paladin"]
        },
        {
            "name": "Invisibility",
            "school": "Illusion",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter", "Illusionist Wizard",
                           "Trickery Cleric"]
        },
        {
            "name": "Lesser Restoration",
            "school": "Abjuration",
            "classes": ["Bard", "Cleric", "Druid", "Paladin", "Ranger"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Magic Weapon",
            "school": "Transmutation",
            "classes": ["Paladin", "Ranger", "Sorcerer", "Wizard"]
        },
        {
            "name": "Melf's Acid Arrow",
            "school": "Evocation",
            "classes": ["Wizard"]
        },
        {
            "name": "Mind Spike",
            "school": "Divination",
            "classes": ["Warlock", "Wizard"]
        },
        {
            "name": "Mirror Image",
            "school": "Illusion",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Misty Step",
            "school": "Conjuration",
            "classes": ["Sorcerer", "Warlock", "Wizard"]
        },
        {
            "name": "Moonbeam",
            "school": "Evocation",
            "classes": ["Druid"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Nystul's Magic Aura",
            "school": "Illusion",
            "classes": ["Wizard"]
        },
        {
            "name": "Phantasmal Force",
            "school": "Illusion",
            "classes": ["Bard", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Prayer Of Healing",
            "school": "Abjuration",
            "classes": ["Cleric", "Paladin"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Protection From Poison",
            "school": "Abjuration",
            "classes": ["Cleric", "Druid", "Paladin", "Ranger"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Ray Of Enfeeblement",
            "school": "Necromancy",
            "classes": ["Warlock", "Wizard"]
        },
        {
            "name": "Scorching Ray",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"]
        },
        {
            "name": "See Invisibility",
            "school": "Divination",
            "classes": ["Bard", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Shatter",
            "school": "Evocation",
            "classes": ["Bard", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Shining Smite",
            "school": "Transmutation",
            "classes": ["Paladin"]
        },
        {
            "name": "Silence",
            "school": "Illusion",
            "classes": ["Bard", "Cleric", "Ranger"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Spider Climb",
            "school": "Transmutation",
            "classes": ["Sorcerer", "Warlock", "Wizard"]
        },
        {
            "name": "Spike Growth",
            "school": "Transmutation",
            "classes": ["Druid", "Ranger"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Spiritual Weapon",
            "school": "Evocation",
            "classes": ["Cleric"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Summon Beast",
            "school": "Conjuration",
            "classes": ["Druid", "Ranger"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Warding Bond",
            "school": "Abjuration",
            "classes": ["Cleric", "Paladin"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Web",
            "school": "Conjuration",
            "classes": ["Sorcerer", "Wizard"]
        },
    ],
    3: [
        {
            "name": "Animate Dead",
            "school": "Necromancy",
            "classes": ["Cleric", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"]
        },
        {
            "name": "Aura Of Vitality",
            "school": "Abjuration",
            "classes": ["Cleric", "Druid", "Paladin"],
            "subclasses": ["Lore Bard"],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Beacon Of Hope",
            "school": "Abjuration",
            "classes": ["Cleric"],
            "subclasses": ["Lore Bard", "Devotion Paladin"]
        },
        {
            "name": "Bestow Curse",
            "school": "Necromancy",
            "classes": ["Bard", "Cleric", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"]
        },
        {
            "name": "Blinding Smite",
            "school": "Evocation",
            "classes": ["Paladin"]
        },
        {
            "name": "Blink",
            "school": "Transmutation",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster", "Archfey Warlock", "Lore Bard", "Eldritch Knight Fighter"]
        },
        {
            "name": "Call Lightning",
            "school": "Conjuration",
            "classes": ["Druid"],
            "subclasses": ["Lore Bard"],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Conjure Animals",
            "school": "Conjuration",
            "classes": ["Druid", "Ranger"],
            "subclasses": ["Circle of the Moon Druid", "Lore Bard"],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Conjure Barrage",
            "school": "Conjuration",
            "classes": ["Ranger"]
        },
        {
            "name": "Counterspell",
            "school": "Abjuration",
            "classes": ["Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Abjurer Wizard", "Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"]
        },
        {
            "name": "Crusader's Mantle",
            "school": "Evocation",
            "classes": ["Paladin"],
            "subclasses": ["War Cleric"]
        },
        {
            "name": "Daylight",
            "school": "Evocation",
            "classes": ["Cleric", "Druid", "Paladin", "Ranger", "Sorcerer"],
            "subclasses": ["Celestial Warlock", "Lore Bard", "Light Cleric"]
        },
        {
            "name": "Dispel Magic",
            "school": "Abjuration",
            "classes": ["Bard", "Cleric", "Druid", "Paladin", "Ranger", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Abjurer Wizard", "Arcane Trickster Rogue", "Clockwork Sorcerer",
                           "Lore Bard", "Eldritch Knight Fighter", "Fey Wanderer Ranger", "Devotion Paladin"]
        },
        {
            "name": "Elemental Weapon",
            "school": "Transmutation",
            "classes": ["Druid", "Paladin", "Ranger"],
            "subclasses": ["Lore Bard"]
        },
        {
            "name": "Fear",
            "school": "Illusion",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Draconic Sorcerer", "Eldritch Knight Fighter",
                           "Gloom Stalker Ranger", "Illusionist Wizard"]
        },
        {
            "name": "Feign Death",
            "school": "Necromancy",
            "classes": ["Bard", "Cleric", "Druid", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"]
        },
        {
            "name": "Fireball",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Circle of the Land Druid", "Lore Bard",
                           "Eldritch Knight Fighter", "Evoker Wizard", "Fiend Warlock", "Light Cleric"]
        },
        {
            "name": "Fly",
            "school": "Transmutation",
            "classes": ["Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Draconic Sorcerer", "Eldritch Knight Fighter"]
        },
        {
            "name": "Gaseous Form",
            "school": "Transmutation",
            "classes": ["Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter"]
        },
        {
            "name": "Haste",
            "school": "Transmutation",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter", "Glory Paladin",
                           "Vengeance Paladin"]
        },
        {
            "name": "Hunger Of Hadar",
            "school": "Conjuration",
            "classes": ["Warlock"],
            "subclasses": ["Aberrant Sorcerer", "Great Old One Warlock"]
        },
        {
            "name": "Hypnotic Pattern",
            "school": "Illusion",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Lore Bard", "Eldritch Knight Fighter", "Illusionist Wizard",
                           "Trickery Cleric"]
        },
        {
            "name": "Lightning Arrow",
            "school": "Transmutation",
            "classes": ["Ranger"]
        },
        {
            "name": "Lightning Bolt",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"]
        },
        {
            "name": "Magic Circle",
            "school": "Abjuration",
            "classes": ["Cleric", "Paladin", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Mass Healing Word",
            "school": "Abjuration",
            "classes": ["Bard", "Cleric"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Phantom Steed",
            "school": "Illusion",
            "classes": ["Wizard"]
        },
        {
            "name": "Plant Growth",
            "school": "Transmutation",
            "classes": ["Bard", "Druid", "Ranger"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Protection From Energy",
            "school": "Abjuration",
            "classes": ["Cleric", "Druid", "Ranger", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Remove Curse",
            "school": "Abjuration",
            "classes": ["Cleric", "Paladin", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Revivify",
            "school": "Necromancy",
            "classes": ["Cleric", "Druid", "Paladin", "Ranger"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Sleet Storm",
            "school": "Conjuration",
            "classes": ["Druid", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Slow",
            "school": "Transmutation",
            "classes": ["Bard", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Spirit Guardians",
            "school": "Conjuration",
            "classes": ["Cleric"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Stinking Cloud",
            "school": "Conjuration",
            "classes": ["Bard", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Summon Fey",
            "school": "Conjuration",
            "classes": ["Druid", "Ranger", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Summon Undead",
            "school": "Necromancy",
            "classes": ["Warlock", "Wizard"]
        },
        {
            "name": "Vampiric Touch",
            "school": "Necromancy",
            "classes": ["Sorcerer", "Warlock", "Wizard"]
        },
        {
            "name": "Wind Wall",
            "school": "Evocation",
            "classes": ["Druid", "Ranger"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
    ],
    4: [
        {
            "name": "Aura Of Life",
            "school": "Abjuration",
            "classes": ["Cleric", "Paladin"],
            "subclasses": ["Life Cleric"]
        },
        {
            "name": "Aura Of Purity",
            "school": "Abjuration",
            "classes": ["Cleric", "Paladin"]
        },
        {
            "name": "Banishment",
            "school": "Abjuration",
            "classes": ["Cleric", "Paladin", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Abjurer Wizard", "Arcane Trickster Rogue", "Eldritch Knight Fighter",
                           "Vengeance Paladin"]
        },
        {
            "name": "Blight",
            "school": "Necromancy",
            "classes": ["Druid", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Circle of the Land Druid", "Eldritch Knight Fighter"]
        },
        {
            "name": "Charm Monster",
            "school": "Enchantment",
            "classes": ["Bard", "Druid", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Draconic Sorcerer", "Eldritch Knight Fighter"]
        },
        {
            "name": "Compulsion",
            "school": "Enchantment",
            "classes": ["Bard"],
            "subclasses": ["Glory Paladin"]
        },
        {
            "name": "Confusion",
            "school": "Enchantment",
            "classes": ["Bard", "Druid", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Eldritch Knight Fighter", "Great Old One Warlock",
                           "Trickery Cleric"]
        },
        {
            "name": "Conjure Minor Elementals",
            "school": "Conjuration",
            "classes": ["Druid", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Eldritch Knight Fighter"]
        },
        {
            "name": "Conjure Woodlands Beings",
            "school": "Conjuration",
            "classes": ["Druid", "Ranger"]
        },
        {
            "name": "Death Ward",
            "school": "Abjuration",
            "classes": ["Cleric", "Paladin"],
            "subclasses": ["Life Cleric"]
        },
        {
            "name": "Dimension Door",
            "school": "Conjuration",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Eldritch Knight Fighter", "Fey Wanderer Ranger",
                           "Vengeance Paladin", "Trickery Cleric"]
        },
        {
            "name": "Dominate Beast",
            "school": "Enchantment",
            "classes": ["Druid", "Ranger", "Sorcerer"],
            "subclasses": ["Archfey Warlock"]
        },
        {
            "name": "Evard's Black Tentacles",
            "school": "Conjuration",
            "classes": ["Wizard"],
            "subclasses": ["Aberrant Sorcerer", "Arcane Trickster Rogue", "Eldritch Knight Fighter"]
        },
        {
            "name": "Fabricate",
            "school": "Transmutation",
            "classes": ["Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Eldritch Knight Fighter"]
        },
        {
            "name": "Fire Shield",
            "school": "Evocation",
            "classes": ["Druid", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Eldritch Knight Fighter", "Evoker Wizard",
                           "Fiend Warlock", "War Cleric"]
        },
        {
            "name": "Fount Of Moonlight",
            "school": "Evocation",
            "classes": ["Bard", "Druid"],
            "subclasses": ["Circle of the Moon Druid"]
        },
        {
            "name": "Freedom Of Movement",
            "school": "Abjuration",
            "classes": ["Bard", "Cleric", "Druid", "Ranger"],
            "subclasses": ["Circle of the Land Druid", "Clockwork Sorcerer", "Devotion Paladin",
                           "Glory Paladin", "War Cleric"]
        },
        {
            "name": "Giant Insect",
            "school": "Conjuration",
            "classes": ["Druid"]
        },
        {
            "name": "Grasping Vine",
            "school": "Conjuration",
            "classes": ["Druid", "Ranger"]
        },
        {
            "name": "Greater Invisibility",
            "school": "Illusion",
            "classes": ["Bard", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Archfey Warlock", "Eldritch Knight Fighter",
                           "Gloom Stalker Ranger", "Illusionist Wizard"]
        },
        {
            "name": "Guardian Of Faith",
            "school": "Conjuration",
            "classes": ["Cleric"],
            "subclasses": ["Celestial Warlock", "Devotion Paladin"]
        },
        {
            "name": "Ice Storm",
            "school": "Evocation",
            "classes": ["Druid", "Sorcerer", "Wizard"],
            "subclasses": ["Arcane Trickster Rogue", "Circle of the Land Druid", "Circle of the Sea Druid",
                           "Eldritch Knight Fighter", "Evoker Wizard", "Ancients Paladin"]
        },
        {
            "name": "Locate Creature",
            "school": "Divination",
            "classes": ["Bard", "Cleric", "Druid", "Paladin", "Ranger", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Mordenkainen's Faithful Hound",
            "school": "Conjuration",
            "classes": ["Wizard"]
        },
        {
            "name": "Otiluke's Resilient Sphere",
            "school": "Abjuration",
            "classes": ["Wizard"]
        },
        {
            "name": "Phantasmal Killer",
            "school": "Illusion",
            "classes": ["Bard", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Polymorph",
            "school": "Transmutation",
            "classes": ["Bard", "Druid", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Staggering Smite",
            "school": "Enchantment",
            "classes": ["Paladin"]
        },
        {
            "name": "Stone Shape",
            "school": "Transmutation",
            "classes": ["Cleric", "Druid", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Stoneskin",
            "school": "Transmutation",
            "classes": ["Druid", "Ranger", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Summon Aberration",
            "school": "Conjuration",
            "classes": ["Warlock", "Wizard"]
        },
        {
            "name": "Summon Construct",
            "school": "Conjuration",
            "classes": ["Wizard"]
        },
        {
            "name": "Summon Elemental",
            "school": "Conjuration",
            "classes": ["Druid", "Ranger", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Vitriolic Sphere",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"]
        },
        {
            "name": "Wall Of Fire",
            "school": "Evocation",
            "classes": ["Druid", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
    ],
    5: [
        {
            "name": "Animate Objects",
            "school": "Transmutation",
            "classes": ["Bard", "Sorcerer", "Wizard"]
        },
        {
            "name": "Antilife Shell",
            "school": "Abjuration",
            "classes": ["Druid"]
        },
        {
            "name": "Awaken",
            "school": "Transmutation",
            "classes": ["Bard", "Druid"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Banishing Smite",
            "school": "Conjuration",
            "classes": ["Paladin"]
        },
        {
            "name": "Bigby's Hand",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Evoker Wizard"]
        },
        {
            "name": "Circle Of Power",
            "school": "Abjuration",
            "classes": ["Cleric", "Paladin", "Wizard"],
            "subclasses": ["Abjurer Wizard"]
        },
        {
            "name": "Cloudkill",
            "school": "Conjuration",
            "classes": ["Sorcerer", "Wizard"]
        },
        {
            "name": "Cone Of Cold",
            "school": "Evocation",
            "classes": ["Druid", "Sorcerer", "Wizard"],
            "subclasses": ["Circle of the Land Druid", "Evoker Wizard"]
        },
        {
            "name": "Conjure Elemental",
            "school": "Conjuration",
            "classes": ["Druid", "Wizard"],
            "subclasses": ["Circle of the Sea Druid"]
        },
        {
            "name": "Conjure Volley",
            "school": "Conjuration",
            "classes": ["Ranger"]
        },
        {
            "name": "Contagion",
            "school": "Necromancy",
            "classes": ["Cleric", "Druid"]
        },
        {
            "name": "Creation",
            "school": "Illusion",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Illusionist Wizard"]
        },
        {
            "name": "Destructive Wave",
            "school": "Evocation",
            "classes": ["Paladin"]
        },
        {
            "name": "Dispel Evil And Good",
            "school": "Abjuration",
            "classes": ["Cleric", "Paladin"]
        },
        {
            "name": "Dominate Person",
            "school": "Enchantment",
            "classes": ["Bard", "Sorcerer", "Wizard"],
            "subclasses": ["Archfey Warlock", "Trickery Cleric"]
        },
        {
            "name": "Flame Strike",
            "school": "Evocation",
            "classes": ["Cleric"],
            "subclasses": ["Light Cleric", "Devotion Paladin"]
        },
        {
            "name": "Geas",
            "school": "Enchantment",
            "classes": ["Bard", "Cleric", "Druid", "Paladin", "Wizard"],
            "subclasses": ["Fiend Warlock"]
        },
        {
            "name": "Greater Restoration",
            "school": "Abjuration",
            "classes": ["Bard", "Cleric", "Druid", "Paladin", "Ranger"],
            "subclasses": ["Celestial Warlock", "Clockwork Sorcerer", "Life Cleric"]
        },
        {
            "name": "Hallow",
            "school": "Abjuration",
            "classes": ["Cleric"]
        },
        {
            "name": "Hold Monster",
            "school": "Enchantment",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": ["Circle of the Sea Druid", "Vengeance Paladin", "War Cleric"]
        },
        {
            "name": "Insect Plague",
            "school": "Conjuration",
            "classes": ["Cleric", "Druid", "Sorcerer"],
            "subclasses": ["Circle of the Land Druid", "Fiend Warlock"]
        },
        {
            "name": "Jallarzi's Storm Of Radiance",
            "school": "Evocation",
            "classes": ["Warlock", "Wizard"],
            "subclasses": ["Evoker Wizard"]
        },
        {
            "name": "Mass Cure Wounds",
            "school": "Abjuration",
            "classes": ["Bard", "Cleric", "Druid"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Mislead",
            "school": "Illusion",
            "classes": ["Bard", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Passwall",
            "school": "Transmutation",
            "classes": ["Wizard"]
        },
        {
            "name": "Raise Dead",
            "school": "Necromancy",
            "classes": ["Bard", "Cleric", "Paladin"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Reincarnate",
            "school": "Necromancy",
            "classes": ["Druid"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Steel Wind Strike",
            "school": "Conjuration",
            "classes": ["Ranger", "Wizard"]
        },
        {
            "name": "Summon Celestial",
            "school": "Conjuration",
            "classes": ["Cleric", "Paladin"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Summon Dragon",
            "school": "Conjuration",
            "classes": ["Wizard"]
        },
        {
            "name": "Swift Quiver",
            "school": "Transmutation",
            "classes": ["Ranger"]
        },
        {
            "name": "Synaptic Static",
            "school": "Enchantment",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Telekinesis",
            "school": "Transmutation",
            "classes": ["Sorcerer", "Wizard"]
        },
        {
            "name": "Tree Stride",
            "school": "Conjuration",
            "classes": ["Druid", "Ranger"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Wall Of Force",
            "school": "Evocation",
            "classes": ["Wizard"]
        },
        {
            "name": "Wall Of Stone",
            "school": "Evocation",
            "classes": ["Druid", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Yolande's Regal Presence",
            "school": "Enchantment",
            "classes": ["Bard", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
    ],
    6: [
        {
            "name": "Arcane Gate",
            "school": "Conjuration",
            "classes": ["Sorcerer", "Warlock", "Wizard"]
        },
        {
            "name": "Blade Barrier", 
            "school": "Evocation",
            "classes": ["Cleric"]
        },
        {
            "name": "Chain Lightning",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Evoker Wizard"]
        },
        {
            "name": "Circle Of Death",
            "school": "Necromancy",
            "classes": ["Sorcerer", "Warlock", "Wizard"]
        },
        {
            "name": "Conjure Fey",
            "school": "Conjuration",
            "classes": ["Druid"]
        },
        {
            "name": "Contingency",
            "school": "Abjuration",
            "classes": ["Wizard"],
            "subclasses": ["Abjurer Wizard"]
        },
        {
            "name": "Create Undead",
            "school": "Necromancy",
            "classes": ["Cleric", "Warlock", "Wizard"]
        },
        {
            "name": "Disintegrate",
            "school": "Transmutation",
            "classes": ["Sorcerer", "Wizard"]
        },
        {
            "name": "Eyebite",
            "school": "Necromancy",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"]
        },
        {
            "name": "Flesh To Stone",
            "school": "Transmutation",
            "classes": ["Druid", "Sorcerer", "Wizard"]
        },
        {
            "name": "Globe Of Invulnerability",
            "school": "Abjuration",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Abjurer Wizard"]
        },
        {
            "name": "Harm",
            "school": "Necromancy",
            "classes": ["Cleric"]
        },
        {
            "name": "Heal",
            "school": "Abjuration",
            "classes": ["Cleric", "Druid"]
        },
        {
            "name": "Heroe's Feast",
            "school": "Conjuration",
            "classes": ["Bard", "Cleric", "Druid"]
        },
        {
            "name": "Move Earth",
            "school": "Transmutation",
            "classes": ["Druid", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Otiluke's Freezing Sphere",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"]
        },
        {
            "name": "Otto's Irresistible Dance",
            "school": "Enchantment",
            "classes": ["Bard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Planar Ally",
            "school": "Conjuration",
            "classes": ["Cleric"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Summon Fiend",
            "school": "Conjuration",
            "classes": ["Warlock", "Wizard"]
        },
        {
            "name": "Sunbeam",
            "school": "Evocation",
            "classes": ["Cleric", "Druid", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "True Seeing",
            "school": "Divination",
            "classes": ["Bard", "Cleric", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Wall Of Ice",
            "school": "Evocation",
            "classes": ["Wizard"]
        },
        {
            "name": "Wall Of Thorns",
            "school": "Conjuration",
            "classes": ["Druid"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Wind Walk",
            "school": "Transmutation",
            "classes": ["Druid"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
    ],
    7: [
        {
            "name": "Conjure Celestial",
            "school": "Conjuration",
            "classes": ["Cleric"]
        },
        {
            "name": "Delayed Blast Fireball",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"],
            "subclasses": ["Evoker Wizard"]
        },
        {
            "name": "Divine Word",
            "school": "Evocation",
            "classes": ["Cleric"]
        },
        {
            "name": "Etherealness",
            "school": "Conjuration",
            "classes": ["Bard", "Cleric", "Sorcerer", "Warlock", "Wizard"]
        },
        {
            "name": "Finger Of Death",
            "school": "Necromancy",
            "classes": ["Sorcerer", "Warlock", "Wizard"]
        },
        {
            "name": "Fire Storm",
            "school": "Evocation",
            "classes": ["Cleric", "Druid", "Sorcerer"]
        },
        {
            "name": "Forcecage",
            "school": "Evocation",
            "classes": ["Bard", "Warlock", "Wizard"],
            "subclasses": ["Evoker Wizard"]
        },
        {
            "name": "Mordenkainen's Sword",
            "school": "Evocation",
            "classes": ["Bard", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Power Word Fortify",
            "school": "Enchantment",
            "classes": ["Bard", "Cleric"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Prismatic Spray",
            "school": "Evocation",
            "classes": ["Bard", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Regenerate",
            "school": "Transmutation",
            "classes": ["Bard", "Cleric", "Druid"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Resurrection",
            "school": "Necromancy",
            "classes": ["Bard", "Cleric"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Reverse Gravity",
            "school": "Transmutation",
            "classes": ["Druid", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Sequester",
            "school": "Transmutation",
            "classes": ["Wizard"]
        },
        {
            "name": "Simulacrum",
            "school": "Illusion",
            "classes": ["Wizard"]
        },
        {
            "name": "Teleport",
            "school": "Conjuration",
            "classes": ["Bard", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
    ],
    8: [
        {
            "name": "Animal Shapes",
            "school": "Transmutation",
            "classes": ["Druid"],
        },
        {
            "name": "Antimagic Field",
            "school": "Abjuration",
            "classes": ["Cleric", "Wizard"],
            "subclasses": ["Abjurer Wizard"]
        },
        {
            "name": "Befuddlement",
            "school": "Enchantment",
            "classes": ["Bard", "Druid", "Warlock", "Wizard"]
        },
        {
            "name": "Clone",
            "school": "Necromancy",
            "classes": ["Wizard"]
        },
        {
            "name": "Dominate Monster",
            "school": "Enchantment",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"]
        },
        {
            "name": "Earthquake",
            "school": "Transmutation",
            "classes": ["Cleric", "Druid", "Sorcerer"]
        },
        {
            "name": "Holy Aura",
            "school": "Abjuration",
            "classes": ["Cleric"]
        },
        {
            "name": "Incendiary Cloud",
            "school": "Conjuration",
            "classes": ["Druid", "Sorcerer", "Wizard"]
        },
        {
            "name": "Maze",
            "school": "Conjuration",
            "classes": ["Wizard"]
        },
        {
            "name": "Mind Blank",
            "school": "Abjuration",
            "classes": ["Bard", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Power Word Stun",
            "school": "Enchantment",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Sunburst",
            "school": "Evocation",
            "classes": ["Cleric", "Druid", "Sorcerer", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Tsunami",
            "school": "Conjuration",
            "classes": ["Druid"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
    ],
    9: [
        {
            "name": "Foresight",
            "school": "Divination",
            "classes": ["Bard", "Druid", "Warlock", "Wizard"],
            "subclasses": ["Diviner Wizard"]
        },
        {
            "name": "Gate",
            "school": "Conjuration",
            "classes": ["Cleric", "Sorcerer", "Warlock", "Wizard"]
        },
        {
            "name": "Imprisonment",
            "school": "Abjuration",
            "classes": ["Warlock", "Wizard"],
            "subclasses": ["Abjurer Wizard"]
        },
        {
            "name": "Mass Heal",
            "school": "Abjuration",
            "classes": ["Cleric"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Meteor Swarm",
            "school": "Evocation",
            "classes": ["Sorcerer", "Wizard"]
        },
        {
            "name": "Power Word Heal",
            "school": "Enchantment",
            "classes": ["Bard", "Cleric"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Power Word Kill",
            "school": "Enchantment",
            "classes": ["Bard", "Sorcerer", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Prismatic Wall",
            "school": "Abjuration",
            "classes": ["Bard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Shapechange",
            "school": "Transmutation",
            "classes": ["Druid", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Storm Of Vengeance",
            "school": "Conjuration",
            "classes": ["Druid"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Time Stop",
            "school": "Transmutation",
            "classes": ["Sorcerer", "Wizard"]
        },
        {
            "name": "True Polymorph",
            "school": "Transmutation",
            "classes": ["Bard", "Warlock", "Wizard"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "True Resurrection",
            "school": "Necromancy",
            "classes": ["Cleric", "Druid"],
            "subclasses": [],
            "sources": [],
            "action": "",
            "range": "",
            "components": [],
            "duration": "",
            "description": "",
            "damage": "",
            "damage_type": "",
            "attack_type": "",
            "scaling": {}
        },
        {
            "name": "Weird",
            "school": "Illusion",
            "classes": ["Warlock", "Wizard"]
        },
    ],
}