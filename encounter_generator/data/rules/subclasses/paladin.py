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
