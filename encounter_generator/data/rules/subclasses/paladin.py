"""
Subclass definitions for the Paladin class.
"""

PALADIN_SUBCLASSES = {
    "devotion": {
        "id": "devotion",
        "name": "Oath of Devotion",
        "description": "The Oath of Devotion binds a paladin to the loftiest ideals of justice, virtue, and order. These paladins, often known as cavaliers, white knights, or holy warriors, share these tenets: Let your word be your promise, protect the weak and never fear to act, let your honorable deeds be an example.",
        "features": {
            3: [
                {
                    "id": "devotion_oath_spells",
                    "name": "Oath Of Devotion Spells",
                    "summary": "You always have certain spells prepared as you gain levels in this class.",
                    "description": "The magic of your oath ensures you always have certain spells ready; when you reach a Paladin level specified in the Oath of Devotion Spells list, you thereafter always have the listed spells prepared. \n Lv3: Protection from Evil and Good, Shield of Faith. \n Lv5: Aid, Zone of Truth. \n Lv9: Beacon of Hope, Dispel Magic. \n Lv13: Freedom of Movement, Guardian of Faith. \n Lv17: Commune, Flame Strike.",
                    "details": {
                        "spells": {
                            3: ["Protection From Evil And Good", "Shield Of Faith"],
                            5: ["Aid", "Zone Of Truth"],
                            9: ["Beacon Of Hope", "Dispel Magic"],
                            13: ["Freedom Of Movement", "Guardian Of Faith"],
                            17: ["Commune", "Flame Strike"]
                        }
                    }
                },
                {
                    "id": "devotion_sacred_weapon",
                    "name": "Sacred Weapon",
                    "summary": "Expend 1 Channel Divinity (Attack action) to add Charisma mod to attacks and deal Radiant damage (10 min).",
                    "description": "When you take the Attack action, you can expend one use of your Channel Divinity to imbue one Melee weapon that you are holding with positive energy. For 10 minutes or until you use this feature again, you add your Charisma modifier to attack rolls you make with that weapon (minimum bonus of +1), and each time you hit with it, you cause it to deal its normal damage type or Radiant damage. The weapon also emits Bright Light in a 20-foot radius and Dim Light 20 feet beyond that. You can end this effect early (no action required). This effect also ends if you aren't carrying the weapon.",
                    "details": {
                        "action": "Attack Action (replacing one attack)",
                        "cost": "1 Channel Divinity",
                        "duration": "10 minutes",
                        "benefits": [
                            "Add Charisma modifier to attack rolls (min +1)",
                            "Can choose to deal Radiant damage",
                            "Emits Bright Light (20ft) and Dim Light (20ft beyond)"
                        ]
                    }
                }
            ],
            7: [
                {
                    "id": "devotion_aura_of_devotion",
                    "name": "Aura Of Devotion",
                    "summary": "You and allies in your Aura of Protection have Immunity to the Charmed condition.",
                    "description": "You and your allies have Immunity to the Charmed condition while in your Aura of Protection. If a Charmed ally enters the aura, that condition has no effect on that ally while there.",
                    "details": {
                        "benefit": "Immunity to Charmed condition",
                        "range": "Aura of Protection"
                    }
                }
            ],
            15: [
                {
                    "id": "devotion_smite_of_protection",
                    "name": "Smite Of Protection",
                    "summary": "Casting Divine Smite grants Half Cover to you and allies in your aura until your next turn.",
                    "description": "Your magical smite now radiates protective energy. Whenever you cast Divine Smite, you and your allies have Half Cover while in your Aura of Protection. The aura has this benefit until the start of your next turn.",
                    "details": {
                        "trigger": "Cast Divine Smite",
                        "effect": "Half Cover (+2 AC/Dex saves) for you and allies in aura",
                        "duration": "Until start of your next turn"
                    }
                }
            ],
            20: [
                {
                    "id": "devotion_holy_nimbus",
                    "name": "Holy Nimbus",
                    "summary": "Bonus Action (10 min): enemies in aura take Radiant damage; advantage vs Fiends/Undead saves.",
                    "description": "As a Bonus Action, you can imbue your Aura of Protection with holy power, granting the benefits below for 10 minutes or until you end them (no action required). Once you use this feature, you can't use it again until you finish a Long Rest. You can also restore your use of it by expending a level 5 spell slot (no action required). *-Holy Ward-* You have Advantage on any saving throw you are forced to make by a Fiend or an Undead. *-Radiant Damage-* Whenever an enemy starts its turn in the aura, that creature takes Radiant damage equal to your Charisma modifier plus your Proficiency Bonus. *-Sunlight-* The aura is filled with Bright Light that is sunlight.",
                    "details": {
                        "action": "Bonus Action",
                        "duration": "10 minutes",
                        "damage": "Charisma modifier + Proficiency Bonus (Radiant)",
                        "save_advantage": "Advantage on saves vs Fiends or Undead",
                        "light": "Bright Light (Sunlight)",
                        "recharge": "Long Rest or expend Level 5 spell slot"
                    }
                }
            ]
        }
    },
    "glory": {
        "id": "glory",
        "name": "Oath of Glory",
        "description": "Paladins who take the Oath of Glory believe they and their companions are destined to achieve glory through magnanimous deeds. They share these tenets: Endeavor to be known by your deeds, face hardships with courage, inspire others to strive for glory.",
        "features": {
            3: [
                {
                    "id": "glory_oath_spells",
                    "name": "Oath Of Glory Spells",
                    "summary": "You always have certain spells prepared as you gain levels in this class.",
                    "description": "The magic of your oath ensures you always have certain spells ready; when you reach a Paladin level specified in the Oath of Glory Spells list, you thereafter always have the listed spells prepared. \n Lv3: Guiding Bolt, Heroism. \n Lv5: Enhance Ability, Magic Weapon. \n Lv9: Haste, Protection from Energy. \n Lv13: Compulsion, Freedom of Movement. \n Lv17: Legend Lore, Yolande's Regal Presence.",
                    "details": {
                        "spells": {
                            3: ["Guiding Bolt", "Heroism"],
                            5: ["Enhance Ability", "Magic Weapon"],
                            9: ["Haste", "Protection From Energy"],
                            13: ["Compulsion", "Freedom Of Movement"],
                            17: ["Legend Lore", "Youlande's Regal Presence"]
                        }
                    }
                },
                {
                    "id": "glory_inspiring_smite",
                    "name": "Inspiring Smite",
                    "summary": "After Divine Smite, expend 1 Channel Divinity to grant 2d8 + Paladin level Temp HP to allies within 30ft.",
                    "description": "Immediately after you cast Divine Smite, you can expend one use of your Channel Divinity and distribute Temporary Hit Points to creatures of your choice within 30 feet of yourself, which can include you. The total number of Temporary Hit Points equals 2d8 plus your Paladin level, divided among the chosen creatures however you like.",
                    "details": {
                        "trigger": "Immediately after Divine Smite",
                        "cost": "1 Channel Divinity",
                        "range": "30ft",
                        "effect": "Distribute 2d8 + Paladin level Temporary Hit Points"
                    }
                },
                {
                    "id": "glory_peerless_athlete",
                    "name": "Peerless Athlete",
                    "summary": "Bonus Action: expend 1 Channel Divinity for 1 hour of Athletics/Acrobatics advantage and +10ft jump distance.",
                    "description": "As a Bonus Action, you can expend one use of your Channel Divinity to augment your athleticism. For 1 hour, you have Advantage on Strength (Athletics) and Dexterity (Acrobatics) checks, and the distance of your Long and High Jumps increases by 10 feet (this extra distance costs movement as normal).",
                    "details": {
                        "action": "Bonus Action",
                        "cost": "1 Channel Divinity",
                        "duration": "1 hour",
                        "benefits": [
                            "Advantage on Strength (Athletics) and Dexterity (Acrobatics) checks",
                            "Long and High Jump distance increases by 10ft"
                        ]
                    }
                }
            ],
            7: [
                {
                    "id": "glory_aura_of_alacrity",
                    "name": "Aura Of Alacrity",
                    "summary": "Your speed increases by 10ft. Allies in your Aura of Protection gain +10ft speed until the end of their next turn.",
                    "description": "Your Speed increases by 10 feet. In addition, whenever an ally enters your Aura of Protection for the first time on a turn or starts their turn there, the ally's Speed increases by 10 feet until the end of their next turn.",
                    "details": {
                        "self_buff": "+10ft Speed",
                        "ally_buff": "+10ft Speed (ends at start/end of next turn)",
                        "range": "Aura of Protection"
                    }
                }
            ],
            15: [
                {
                    "id": "glory_glorious_defense",
                    "name": "Glorious Defense",
                    "summary": "Reaction: grant AC bonus (Charisma mod) to self/ally within 10ft on hit. If attack misses, make a weapon attack.",
                    "description": "You can turn defense into a sudden strike. When you or another creature you can see within 10 feet of you is hit by an attack roll, you can take a Reaction to grant a bonus to the target's AC against that attack, potentially causing it to miss. The bonus equals your Charisma modifier (minimum of +1). If the attack misses, you can make one attack with a weapon against the attacker as part of this Reaction if the attacker is within your weapon's range. You can use this feature a number of times equal to your Charisma modifier (minimum of once), and you regain all expended uses when you finish a Long Rest.",
                    "details": {
                        "action": "Reaction",
                        "trigger": "Target within 10ft hit by attack",
                        "bonus": "Charisma modifier (min +1) to AC",
                        "counter_attack": "Make 1 weapon attack if original attack misses",
                        "uses": "Charisma modifier (minimum 1)",
                        "recharge": "Long Rest"
                    }
                }
            ],
            20: [
                {
                    "id": "glory_living_legend",
                    "name": "Living Legend",
                    "summary": "Bonus Action (10 min): Advantage on Charisma checks, reroll failed saves, and turn one miss per turn into a hit.",
                    "description": "You can empower yourself with the legends—whether true or exaggerated—of your great deeds. As a Bonus Action, you gain the benefits below for 10 minutes. Once you use this feature, you can't use it again until you finish a Long Rest. You can also restore your use of it by expending a level 5 spell slot (no action required). *-Charismatic-* You are blessed with an otherworldly presence and have Advantage on all Charisma checks. *-Saving Throw Reroll-* If you fail a saving throw, you can take a Reaction to reroll it. You must use this new roll. *-Unerring Strike-* Once on each of your turns when you make an attack roll with a weapon and miss, you can cause that attack to hit instead.",
                    "details": {
                        "action": "Bonus Action",
                        "duration": "10 minutes",
                        "benefits": [
                            "Advantage on all Charisma checks",
                            "Reaction: Reroll a failed saving throw (must use new roll)",
                            "Once per turn: turn a missed weapon attack into a hit"
                        ],
                        "recharge": "Long Rest or expend Level 5 spell slot"
                    }
                }
            ]
        }
    },
    "ancients": {
        "id": "ancients",
        "name": "Oath of the Ancients",
        "description": "The Oath of the Ancients is as old as the first elves and the first rituals. Paladins who take this oath love the beautiful and life-giving things of the world. They share these tenets: Kindle the light of hope, shelter life, delight in art and laughter.",
        "features": {
            3: [
                {
                    "id": "ancients_oath_spells",
                    "name": "Oath Of The Ancients Spells",
                    "summary": "You always have certain spells prepared as you gain levels in this class.",
                    "description": "The magic of your oath ensures you always have certain spells ready; when you reach a Paladin level specified in the Oath of the Ancients Spells list, you thereafter always have the listed spells prepared. \n Lv3: Ensnaring Strike, Speak with Animals. \n Lv5: Misty Step, Moonbeam. \n Lv9: Plant Growth, Protection from Energy. \n Lv13: Ice Storm, Stoneskin. \n Lv17: Commune with Nature, Tree Strides.",
                    "details": {
                        "spells": {
                            3: ["Ensnaring Strike", "Speak With Animals"],
                            5: ["Misty Step", "Moonbeam"],
                            9: ["Plant Growth", "Protection From Energy"],
                            13: ["Ice Storm", "Stoneskin"],
                            17: ["Commune With Nature", "Tree Stride"]
                        }
                    }
                },
                {
                    "id": "ancients_natures_wrath",
                    "name": "Nature's Wrath",
                    "summary": "Magic Action: expend 1 Channel Divinity to Restrain creatures within 15ft (Strength save).",
                    "description": "As a Magic action, you can expend one use of your Channel Divinity to conjure spectral vines around nearby creatures. Each creature of your choice that you can see within 15 feet of yourself must succeed on a Strength saving throw or have the Restrained condition for 1 minute. A Restrained creature repeats the save at the end of each of its turns, ending the effect on itself on a success.",
                    "details": {
                        "action": "Magic Action",
                        "cost": "1 Channel Divinity",
                        "range": "15ft",
                        "effect": "Restrained condition for 1 minute (save repeats at end of turns)"
                    }
                }
            ],
            7: [
                {
                    "id": "ancients_aura_of_warding",
                    "name": "Aura Of Warding",
                    "summary": "You and allies in your Aura of Protection have Resistance to Necrotic, Psychic, and Radiant damage.",
                    "description": "Ancient magic lies so heavily upon you that it forms an eldritch ward, blunting energy from before Mortal time; you and your allies have Resistance to Necrotic, Psychic, and Radiant damage while in your Aura of Protection.",
                    "details": {
                        "resistances": ["Necrotic", "Psychic", "Radiant"],
                        "lore": "Ancient magic blunts energy from beyond the Mortal Realm.",
                        "range": "Aura of Protection"
                    }
                }
            ],
            15: [
                {
                    "id": "ancients_undying_sentinel",
                    "name": "Undying Sentinel",
                    "summary": "Drop to 1 HP instead of 0 and heal 3x Paladin level once per Long Rest. Cease visibly aging.",
                    "description": "When you are reduced to 0 Hit Points and not killed outright, you can drop to 1 Hit Point instead, and you regain a number of Hit Points equal to three times your Paladin level. Once you use this feature, you can't do so again until you finish a Long Rest. Additionally, you can't be aged magically, and you cease visibly aging.",
                    "details": {
                        "death_ward": "Drop to 1 HP instead of 0 (unless killed outright)",
                        "healing": "3x Paladin level",
                        "extra": "Cannot be aged magically; cease visibly aging",
                        "recharge": "Long Rest"
                    }
                }
            ],
            20: [
                {
                    "id": "ancients_elder_champion",
                    "name": "Elder Champion",
                    "summary": "Bonus Action (1 min): enemies have save disadvantage vs your magic; heal 10 HP per turn; cast spells as Bonus Actions.",
                    "description": "As a Bonus Action, you can imbue your Aura of Protection with primal power, granting the benefits below for 1 minute or until you end them (no action required). Once you use this feature, you can't use it again until you finish a Long Rest. You can also restore your use of it by expending a level 5 spell slot (no action required). *-Diminish Defiance-* Enemies in the aura have Disadvantage on saving throws against your spells and Channel Divinity options. *-Regeneration-* At the start of each of your turns, you regain 10 Hit Points. *-Swift Spells-* Whenever you cast a spell that has a casting time of an action, you can cast it using a Bonus Action instead.",
                    "details": {
                        "action": "Bonus Action",
                        "duration": "1 minute",
                        "regeneration": "10 Hit Points at start of each turn",
                        "magic_buffs": [
                            "Enemies have Disadvantage on saves vs your spells/Channel Divinity",
                            "Action spells can be cast as a Bonus Action"
                        ],
                        "recharge": "Long Rest or expend Level 5 spell slot"
                    }
                }
            ]
        }
    },
    "vengeance": {
        "id": "vengeance",
        "name": "Oath of Vengeance",
        "description": "The Oath of Vengeance is a solemn commitment to punish those who have committed grievous sins. When evil forces slaughter helpless villagers, when an entire people turns against the will of the gods, when a guild of thieves grows too violent and powerful, or when a dragon rampages through the countryside, at times like these, paladins arise and swear an Oath of Vengeance. These paladins share the following tenets: Show the wicked no mercy, fight injustice and its causes, aid those harmed by injustice.",
        "features": {
            3: [
                {
                    "id": "vengeance_oath_spells",
                    "name": "Oath Of Vengeance Spells",
                    "summary": "You always have certain spells prepared as you gain levels in this class.",
                    "description": "The magic of your oath ensures you always have certain spells ready; when you reach a Paladin level specified in the Oath of Vengeance Spells list, you thereafter always have the listed spells prepared. \n Lv3: Bane, Hunter's Mark. \n Lv5: Hold Person, Misty Step. \n Lv9: Haste, Protection from Energy. \n Lv13: Banishment, Dimension Door. \n Lv17: Hold Monster, Scrying.",
                    "details": {
                        "spells": {
                            3: ["Bane", "Hunter's Mark"],
                            5: ["Hold Person", "Misty Step"],
                            9: ["Haste", "Protection From Energy"],
                            13: ["Banishment", "Dimension Door"],
                            17: ["Hold Monster", "Scrying"]
                        }
                    }
                },
                {
                    "id": "vengeance_vow_of_enmity",
                    "name": "Vow Of Enmity",
                    "summary": "When you take the Attack action, expend 1 Channel Divinity to gain Advantage on attack rolls against a creature within 30ft for 1 min.",
                    "description": "When you take the Attack action, you can expend one use of your Channel Divinity to utter a vow of enmity against a creature you can see within 30 feet of yourself. You have Advantage on attack rolls against the creature for 1 minute or until you use this feature again. If the creature drops to 0 Hit Points before the vow ends, you can transfer the vow to a different creature within 30 feet of yourself (no action required).",
                    "details": {
                        "action": "Attack Action (replacing one attack)",
                        "cost": "1 Channel Divinity",
                        "range": "30ft",
                        "duration": "1 minute",
                        "effect": "Advantage on attack rolls against the target; transfer to new target if original drops to 0 HP"
                    }
                }
            ],
            7: [
                {
                    "id": "vengeance_relentless_avenger",
                    "name": "Relentless Avenger",
                    "summary": "Hit with Opportunity Attack: reduce target Speed to 0 and move up to half your Speed (no Opportunity Attacks).",
                    "description": "Your supernatural focus helps you close off a foe's retreat. When you hit a creature with an Opportunity Attack, you can reduce the creature's Speed to 0 until the end of the current turn. You can then move up to half your Speed as part of the same Reaction. This movement doesn't provoke Opportunity Attacks.",
                    "details": {
                        "trigger": "Hit a creature with an Opportunity Attack",
                        "effect": "Target Speed becomes 0 until end of turn",
                        "movement": "Move up to half your Speed as part of the Reaction"
                    }
                }
            ],
            15: [
                {
                    "id": "vengeance_soul_of_vengeance",
                    "name": "Soul Of Vengeance",
                    "summary": "Reaction: make a melee attack when your Vow of Enmity target hits or misses with an attack.",
                    "description": "Immediately after a creature under the effect of your Vow of Enmity hits or misses with an attack roll, you can take a Reaction to make a melee attack against that creature if it's within range.",
                    "details": {
                        "trigger": "Vow of Enmity target makes an attack roll",
                        "action": "Reaction",
                        "effect": "Make 1 melee attack against the target"
                    }
                }
            ],
            20: [
                {
                    "id": "vengeance_avenging_angel",
                    "name": "Avenging Angel",
                    "summary": "Bonus Action (10 min): gain 60ft Fly Speed; enemies in aura must save or be Frightened (Advantage vs Frightened targets).",
                    "description": "As a Bonus Action, you gain the benefits below for 10 minutes or until you end them (no action required). Once you use this feature, you can't use it again until you finish a Long Rest. You can also restore your use of it by expending a level 5 spell slot (no action required). *-Flight-* You sprout spectral wings on your back, have a Fly Speed of 60 feet, and can hover. *-Frightful Aura-* Whenever an enemy starts its turn in your Aura of Protection, that creature must succeed on a Wisdom saving throw or have the Frightened condition for 1 minute or until it takes any damage. Attack rolls against the Frightened creature have Advantage.",
                    "details": {
                        "action": "Bonus Action",
                        "duration": "10 minutes",
                        "movement": "60ft Fly Speed (can hover)",
                        "aura_effect": "Enemies starting turn in aura must save (Wisdom) or be Frightened; attacks against Frightened targets have Advantage",
                        "recharge": "Long Rest or expend Level 5 spell slot"
                    }
                }
            ]
        }
    }
}
