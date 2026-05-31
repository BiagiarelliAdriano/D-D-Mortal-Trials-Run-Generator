"""
Subclass definitions for the Cleric class.
"""

CLERIC_SUBCLASSES = {
    "life": {
        "id": "life",
        "name": "Life Domain",
        "description": "The Life Domain focuses on the vibrant positive energy, one of the fundamental forces of the universe, that sustains all life. Clerics of this domain are masters of healing magic, dedicated to preserving life and restoring the wounded to strength.",
        "features": {
            3: [
                {
                    "id": "life_disciple_of_life",
                    "name": "Disciple Of Life",
                    "summary": "Healing spells restore extra HP equal to 2 + spell slot level.",
                    "description": "When a spell you cast with a spell slot restores Hit Points to a creature, that creature regains additional Hit Points on the turn you cast the spell. The additional Hit Points equal 2 plus the spell slot's level.",
                    "details": {
                        "bonus_healing": "2 + spell slot level",
                        "trigger": "Cast a healing spell using a spell slot"
                    }
                },
                {
                    "id": "life_domain_spells",
                    "name": "Life Domain Spells",
                    "summary": "Always have specific healing and preservation spells prepared.",
                    "description": "Your connection to this divine domain ensures you always have certain spells ready. When you reach a Cleric level specified in the Life Domain Spells table, you thereafter always have the listed spells prepared. \n Lv3: Aid, Bless, Cure Wounds, Lesser Restoration. \n Lv5: Mass Healing Word, Revivify. \n Lv7: Aura of Life, Death Ward. \n Lv9: Greater Restoration, Mass Cure Wounds.",
                    "details": {
                        "spells": {
                            3: ["Aid", "Bless", "Cure Wounds", "Lesser Restoration"],
                            5: ["Mass Healing Word", "Revivify"],
                            7: ["Aura Of Life", "Death Ward"],
                            9: ["Greater Restoration", "Mass Cure Wounds"]
                        }
                    }
                },
                {
                    "id": "life_preserve_life",
                    "name": "Preserve Life",
                    "summary": "Channel Divinity: restore 5x Cleric level HP to Bloodied creatures within 30ft (up to half max HP).",
                    "description": "As a Magic action, you present your Holy Symbol and expend a use of your Channel Divinity to evoke healing energy that can restore a number of Hit Points equal to five times your Cleric level. Choose Bloodied creatures within 30 feet of yourself (which can include you), and divide those Hit Points among them. This feature can restore a creature to no more than half its Hit Point maximum.",
                    "details": {
                        "action": "Magic Action",
                        "cost": "One use of Channel Divinity",
                        "range": "30ft",
                        "healing_pool": "5 * Cleric Level",
                        "target_restriction": "Bloodied creatures (current HP <= half max HP)",
                        "healing_limit": "Cannot restore creature beyond half its max HP"
                    }
                }
            ],
            6: [
                {
                    "id": "life_blessed_healer",
                    "name": "Blessed Healer",
                    "summary": "Healing others also heals you: regain 2 + spell slot level HP.",
                    "description": "The healing spells you cast on others heal you as well. Immediately after you cast a spell with a spell slot that restores Hit Points to one creature other than you, you regain Hit Points equal to 2 plus the spell slot's level.",
                    "details": {
                        "trigger": "Cast a spell with a slot that restores HP to others",
                        "healing": "2 + spell slot level"
                    }
                }
            ],
            17: [
                {
                    "id": "life_supreme_healing",
                    "name": "Supreme Healing",
                    "summary": "Healing spells and Channel Divinity use the highest possible number for each die roll.",
                    "description": "When you would normally roll one or more dice to restore Hit Points to a creature with a spell or Channel Divinity, don't roll those dice for the healing; instead use the highest number possible for each die. For example, instead of restoring 2d6 Hit Points to a creature with a spell, you restore 12.",
                    "details": {
                        "effect": "Use maximum value for healing dice (no rolling required)"
                    }
                }
            ]
        }
    },
    "light": {
        "id": "light",
        "name": "Light Domain",
        "description": "The Light Domain focuses on the divine radiance of the heavens and the searing power of the sun. Clerics of this domain are beacons of hope and justice, using their holy light to blind foes, reveal hidden truths, and immolate the forces of darkness.",
        "features": {
            3: [
                {
                    "id": "light_domain_spells",
                    "name": "Light Domain Spells",
                    "summary": "Always have specific fire and light-based spells prepared.",
                    "description" : "Your connection to this divine domain ensures you always have certain spells ready. When you reach a Cleric level specified in the Light Domain Spells table, you thereafter always have the listed spells prepared. \n Lv3: Burning Hands, Faerie Fire, Scorching Ray, See Invisibility. \n Lv5: Daylight, Fireball. \n Lv7: Arcane Eye, Wall of Fire. \n Lv9: Flame Strike, Scrying.",
                    "details": {
                        "spells": {
                            3: ["Burning Hands", "Faerie Fire", "Scorching Ray", "See Invisibility"],
                            5: ["Daylight", "Fireball"],
                            7: ["Arcane Eye", "Wall Of Fire"],
                            9: ["Flame Strike", "Scrying"]
                        }
                    }
                },
                {
                    "id": "light_radiance_of_the_dawn",
                    "name": "Radiance Of The Dawn",
                    "summary": "Channel Divinity: dispel magical darkness and deal Radiant damage in a 30ft Emanation.",
                    "description": "As a Magic action, you present your Holy Symbol and expend a use of your Channel Divinity to emit a flash of light in a 30-foot Emanation originating from yourself. Any magical Darkness—such as that created by the Darkness spell—in that area is dispelled. Additionally, each creature of your choice in that area must make a Constitution saving throw, taking Radiant damage equal to 2d10 plus your Cleric level on a failed save or half as much damage on a successful one.",
                    "details": {
                        "action": "Magic Action",
                        "cost": "One use of Channel Divinity",
                        "area": "30ft Emanation",
                        "effect": "Dispel magical darkness. Con save or take 2d10 + Cleric level Radiant damage (half on success)."
                    }
                },
                {
                    "id": "light_warding_flare",
                    "name": "Warding Flare",
                    "summary": "Reaction: impose Disadvantage on an attack roll within 30ft; uses equal Wisdom modifier.",
                    "description": "When a creature that you can see within 30 feet of yourself makes an attack roll, you can take a Reaction to impose Disadvantage on the attack roll, causing light to flare before it hits or misses. You can use this feature a number of times equal to your Wisdom modifier (minimum of once). You regain all expended uses when you finish a Long Rest.",
                    "details": {
                        "action": "Reaction",
                        "range": "30ft",
                        "effect": "Impose Disadvantage on the attack roll",
                        "uses": "Wisdom modifier (minimum 1)",
                        "recharge": "Long Rest"
                    }
                }
            ],
            6: [
                {
                    "id": "light_improved_warding_flare",
                    "name": "Improved Warding Flare",
                    "summary": "Warding Flare recharges on Short/Long Rests and grants Temp HP to the attack target.",
                    "description": "You regain all expended uses of your Warding Flare when you finish a Short or Long Rest. In addition, whenever you use Warding Flare, you can give the target of the triggering attack a number of Temporary Hit Points equal to 2d6 plus your Wisdom modifier.",
                    "details": {
                        "recharge_update": "Short or Long Rest",
                        "bonus_effect": "Target of triggering attack receives 2d6 + Wisdom modifier Temporary Hit Points"
                    }
                }
            ],
            17: [
                {
                    "id": "light_corona_of_light",
                    "name": "Corona Of Light",
                    "summary": "Magic Action: emit sunlight aura that imposes Disadvantage on saves versus your Fire/Radiant effects.",
                    "description": "As a Magic action, you cause yourself to emit an aura of sunlight that lasts for 1 minute or until you dismiss it (no action required). You emit Bright Light in a 60-foot radius and Dim Light for an additional 30 feet. Your enemies in the Bright Light have Disadvantage on saving throws against your Radiance of the Dawn and any spell that deals Fire or Radiant damage. You can use this feature a number of times equal to your Wisdom modifier (minimum of once), and you regain all expended uses when you finish a Long Rest.",
                    "details": {
                        "action": "Magic Action",
                        "duration": "1 minute",
                        "light": "60ft Bright, 30ft Dim",
                        "effect": "Enemies in Bright Light have Disadvantage on saves vs Radiance of the Dawn and your Fire/Radiant spells",
                        "uses": "Wisdom modifier (minimum 1)",
                        "recharge": "Long Rest"
                    }
                }
            ]
        }
    },
    "trickery": {
        "id": "trickery",
        "name": "Trickery Domain",
        "description": "The Trickery Domain is the province of gods who are mischief-makers, rebels, and subverters of the status quo. Clerics of this domain are masters of deception, illusion, and stealth, using their divine powers to outwit foes and navigate through shadows.",
        "features": {
            3: [
                {
                    "id": "trickery_blessing_of_the_trickster",
                    "name": "Blessing Of The Trickster",
                    "summary": "Magic Action: grant yourself or a willing creature within 30ft Advantage on Stealth checks until a Long Rest.",
                    "description": "As a Magic action, you can choose yourself or a willing creature within 30 feet of yourself to have Advantage on Dexterity (Stealth) checks. This blessing lasts until you finish a Long Rest or you use this feature again.",
                    "details": {
                        "action": "Magic Action",
                        "range": "30ft",
                        "effect": "Advantage on Dexterity (Stealth) checks",
                        "duration": "Until Long Rest or reused"
                    }
                },
                {
                    "id": "trickery_invoke_duplicity",
                    "name": "Invoke Duplicity",
                    "summary": "Bonus Action: expend Channel Divinity to create a perfect illusory double that you can cast spells from.",
                    "description": "As a Bonus Action, you can expend one use of your Channel Divinity to create a perfect visual illusion of yourself in an unoccupied space you can see within 30 feet of yourself. The illusion is intangible and doesn't occupy its space. It lasts for 1 minute, but it ends early if you dismiss it (no action required) or have the Incapacitated condition. The illusion is animated and mimics your expressions and gestures. While it persists, you gain the following benefits. \n Cast Spells. You can cast spells as though you were in the illusion's space, but you must use your own senses. \n Distract. When both you and your illusion are within 5 feet of a creature that can see the illusion, you have Advantage on attack rolls against that creature, given how distracting the illusion is to the target. \n Move. As a Bonus Action, you can move the illusion up to 30 feet to an unoccupied space you can see that is within 120 feet of yourself.",
                    "details": {
                        "action": "Bonus Action",
                        "cost": "One use of Channel Divinity",
                        "range": "30ft creation, 120ft tether",
                        "duration": "1 minute (Concentration not explicitly required by user prompt, but illusion ends if Incapacitated)",
                        "benefits": [
                            "Cast spells from illusion's space",
                            "Advantage on attacks if both you and illusion are within 5ft of target",
                            "Move illusion 30ft as a Bonus Action"
                        ]
                    }
                },
                {
                    "id": "trickery_domain_spells",
                    "name": "Trickery Domain Spells",
                    "summary": "Always have specific illusion and deception spells prepared.",
                    "description": "Your connection to this divine domain ensures you always have certain spells ready. When you reach a Cleric level specified in the Trickery Domain Spells table, you thereafter always have the listed spells prepared. \n Lv3: Charm Person, Disguise Self, Invisibility, Pass without Trace. \n Lv5: Hypnotic Pattern, Nondetection. \n Lv7: Confusion, Dimension Door. \n Lv9: Dominate Person, Modify Memory.",
                    "details": {
                        "spells": {
                            3: ["Charm Person", "Disguise Self", "Invisibility", "Pass Without Trace"],
                            5: ["Hypnotic Pattern", "Nondetection"],
                            7: ["Confusion", "Dimension Door"],
                            9: ["Dominate Person", "Modify Memory"]
                        }
                    }
                }
            ],
            6: [
                {
                    "id": "trickery_tricksters_transposition",
                    "name": "Trickster's Transposition",
                    "summary": "Teleport and swap places with your duplicate when you create or move it with a Bonus Action.",
                    "description": "Whenever you take the Bonus Action to create or move the illusion of your Invoke Duplicity, you can teleport, swapping places with the illusion.",
                    "details": {
                        "trigger": "Using Bonus Action to create or move Invoke Duplicity illusion",
                        "effect": "Swap places with the illusion"
                    }
                }
            ],
            17: [
                {
                    "id": "trickery_improved_duplicity",
                    "name": "Improved Duplicity",
                    "summary": "Illusion grants Advantage to allies within 5ft; heals a creature for Cleric level HP when it ends.",
                    "description": "The illusion of your Invoke Duplicity has grown more powerful in the following ways. \n Shared Distraction. When you and your allies make attack rolls against a creature within 5 feet of the illusion, the attack rolls have Advantage. \n Healing Illusion. When the illusion ends, you or a creature of your choice within 5 feet of it regains a number of Hit Points equal to your Cleric level.",
                    "details": {
                        "bonus_effect": "Allies within 5ft of illusion have Advantage on attack rolls",
                        "healing": "Regain HP equal to Cleric level when illusion ends (you or 1 creature within 5ft)"
                    }
                }
            ]
        }
    },
    "war": {
        "id": "war",
        "name": "War Domain",
        "description": "The War Domain excels in the heat of battle, honoring gods who reward bravery and martial prowess. Clerics of this domain are divine warriors who bolster their own strikes and those of their allies, ensuring that every blow delivered in the name of their deity hits with the force of divine decree.",
        "features": {
            3: [
                {
                    "id": "war_guided_strike",
                    "name": "Guided Strike",
                    "summary": "Expend Channel Divinity to give a +10 bonus to a missed attack roll (within 30ft; uses Reaction for others).",
                    "description": "When you or a creature within 30 feet of you misses with an attack roll, you can expend one use of your Channel Divinity and give that roll a +10 bonus, potentially causing it to hit. When you use this feature to benefit another creature's attack roll, you must take a Reaction to do so.",
                    "details": {
                        "cost": "One use of Channel Divinity",
                        "range": "30ft",
                        "effect": "+10 bonus to the attack roll",
                        "action": "No action required for self, Reaction for others"
                    }
                },
                {
                    "id": "war_domain_spells",
                    "name": "War Domain Spells",
                    "summary": "Always have specific combat and protection spells prepared.",
                    "description": "Your connection to this divine domain ensures you always have certain spells ready. When you reach a Cleric level specified in the War Domain Spells table, you thereafter always have the listed spells prepared. \n Lv3: Guiding Bolt, Magic Weapon, Shield of Faith, Spiritual Weapon. \n Lv5: Crusader's Mantle, Spirit Guardians. \n Lv7: Fire Shield, Freedom of Movement. \n Lv9: Hold Monster, Steel Wind Strike.",
                    "details": {
                        "spells": {
                            3: ["Guiding Bolt", "Magic Weapon", "Shield Of Faith", "Spiritual Weapon"],
                            5: ["Crusader's Mantle", "Spirit Guardians"],
                            7: ["Fire Shield", "Freedom Of Movement"],
                            9: ["Hold Monster", "Steel Wind Strike"]
                        }
                    }
                },
                {
                    "id": "war_war_priest",
                    "name": "War Priest",
                    "summary": "Bonus Action: make one weapon attack or Unarmed Strike; uses equal Wisdom modifier.",
                    "description": "As a Bonus Action, you can make one attack with a weapon or an Unarmed Strike. You can use this Bonus Action a number of times equal to your Wisdom modifier (minimum of once). You regain all expended uses when you finish a Short or Long Rest.",
                    "details": {
                        "action": "Bonus Action",
                        "effect": "One weapon attack or Unarmed Strike",
                        "uses": "Wisdom modifier (minimum 1)",
                        "recharge": "Short or Long Rest"
                    }
                }
            ],
            6: [
                {
                    "id": "war_war_gods_blessing",
                    "name": "War God's Blessing",
                    "summary": "Expend Channel Divinity to cast Shield of Faith or Spiritual Weapon without a slot or Concentration (1 min).",
                    "description": "You can expend a use of your Channel Divinity to cast Shield of Faith or Spiritual Weapon rather than expending a spell slot. When you cast either spell in this way, the spell doesn't require Concentration. Instead the spell lasts for 1 minute, but it ends early if you cast that spell again, have the Incapacitated condition, or die.",
                    "details": {
                        "cost": "One use of Channel Divinity",
                        "effect": "Cast Shield of Faith or Spiritual Weapon without a spell slot",
                        "special": "Does not require Concentration; lasts 1 minute or until recast/incapacitated"
                    }
                }
            ],
            17: [
                {
                    "id": "war_avatar_of_battle",
                    "name": "Avatar Of Battle",
                    "summary": "Gain Resistance to Bludgeoning, Piercing, and Slashing damage.",
                    "description": "You gain Resistance to Bludgeoning, Piercing, and Slashing damage.",
                    "details": {
                        "effect": "Permanently gain Resistance to non-magical and magical physical damage"
                    }
                }
            ]
        }
    }
}
