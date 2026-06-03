from encounter_generator.data.rules.spell_tables import FULL_CASTER_SLOTS
from encounter_generator.data.rules.subclasses.barbarian import BARBARIAN_SUBCLASSES
from encounter_generator.data.rules.subclasses.bard import BARD_SUBCLASSES
from encounter_generator.data.rules.subclasses.cleric import CLERIC_SUBCLASSES
from encounter_generator.data.rules.subclasses.druid import DRUID_SUBCLASSES
from encounter_generator.data.rules.subclasses.fighter import FIGHTER_SUBCLASSES
from encounter_generator.data.rules.subclasses.monk import MONK_SUBCLASSES
from encounter_generator.data.rules.subclasses.paladin import PALADIN_SUBCLASSES
from encounter_generator.data.rules.subclasses.ranger import RANGER_SUBCLASSES
from encounter_generator.data.rules.subclasses.rogue import ROGUE_SUBCLASSES
from encounter_generator.data.rules.subclasses.sorcerer import SORCERER_SUBCLASSES
from encounter_generator.data.rules.subclasses.warlock import WARLOCK_SUBCLASSES
from encounter_generator.data.rules.subclasses.wizard import WIZARD_SUBCLASSES
from encounter_generator.data.rules.feature_tables import SORCERER_METAMAGIC, WARLOCK_ELDRITCH_INVOCATIONS
from encounter_generator.data.rules.game_rules import BRUTAL_STRIKE_OPTIONS

BARBARIAN = {
    "id": "barbarian",
    "name": "Barbarian",
    "subclasses": BARBARIAN_SUBCLASSES,
    "description": """Barbarians are relentless warriors empowered by primal forces surging from within. Their fury is not
        just rage, it's a physical manifestation of raw survival instinct, ancient spirit guidance, or the wrath
        of a world out of balance.""",
    "primary_ability": "Strength",
    "hit_die": "d12",
    "proficiencies": {
        "saving_throws": ["Strength", "Constitution"],
        "armor": ["Light", "Medium", "Shields"],
        "weapons": ["Simple", "Martial"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Animal Handling", "Athletics", "Intimidation", "Nature", "Perception", "Survival"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Greataxe", "4 Handaxes", "Explorer's Pack"],
            "gold": 15
        },
        "option_b": {
            "gold": 75
        }
    },
    "features": {
        1: [
            {
                "id": "barbarian_rage",
                "name": "Rage",
                "summary": "Enter a state of primal fury, granting bonuses to damage, resistances, and Strength-based rolls.",
                "description": "Your battle fury is a primal force that surges from within, granting you preternatural strength and resilience. On your turn, you can enter a Rage as a Bonus Action. \n\nWhile Raging, you gain the following benefits: \n- **Strength Advantage**: You have Advantage on Strength checks and Strength saving throws. \n- **Rage Damage**: When you make a melee attack using Strength and hit, you gain a bonus to the damage roll. \n- **Resilience**: You have resistance to Bludgeoning, Piercing, and Slashing damage. \n\nYour Rage lasts for 10 minutes. It ends early if you are knocked unconscious or if your turn ends and you haven't attacked a creature, taken damage, or used a Bonus Action to extend it since your last turn.",
                "details": {
                    "Action": "Bonus Action",
                    "uses": {
                        "1-2": 2,
                        "3-5": 3,
                        "6-11": 4,
                        "12-16": 5,
                        "17-20": 6
                    },
                    "recharge": "Short Rest (regain 1), Long Rest (regain all)",
                    "Rage Damage": {
                        "1-8": "+2",
                        "9-15": "+3",
                        "16-20": "+4"
                    },
                    "Resistances": "Bludgeoning, Piercing, Slashing",
                    "Advantages": "Strength Checks & Saves"
                }
            },
            {
                "id": "barbarian_unarmored_defense",
                "name": "Unarmored Defense",
                "summary": "Your AC equals 10 + Dex mod + Con mod while not wearing armor.",
                "description": "Your body is as tough as any suit of mail. While you are not wearing any armor, your Armor Class equals 10 + your Dexterity modifier + your Constitution modifier. You can use a Shield and still gain this benefit.",
                "details": {
                    "Action": "Passive",
                    "Calculation": "10 + DEX + CON",
                    "Requirement": "No Armor"
                }
            },
            {
                "id": "barbarian_weapon_mastery",
                "name": "Weapon Mastery",
                "summary": "Gain mastery of two melee weapons; increases at higher levels. On a Long Rest, you may swap one mastered weapon for another.",
                "description": "Your training with weapons allows you to push them beyond their normal limits. You gain mastery of two melee weapons of your choice. When you hit a creature with a weapon you have mastered, you can use the weapon's mastery property if you meet the requirements. At higher levels, the number of weapons you can master increases.\n\nWhen you finish a Long Rest, you may replace one of your mastered weapons with a different melee weapon.",
                "details": {
                    "Action": "Passive",
                    "weapons_mastered": {
                        "type": "level-based",
                        "scaling": {
                            "1-3": 2,
                            "4-9": 3,
                            "10-20": 4
                        }
                    },
                    "recharge": "Long Rest",
                    "recharge_effect": "swap_weapon_mastery"
                }
            }
        ],
        2: [
            {
                "id": "barbarian_danger_sense",
                "name": "Danger Sense",
                "summary": "Advantage on Dexterity saves while not Incapacitated.",
                "description": "You gain an uncanny sense of when things nearby aren't as they should be, giving you an edge when you dodge away from danger. You have Advantage on Dexterity saving throws against effects that you can see, such as traps and spells. This benefit is suspended if you are Incapacitated.",
                "details": {
                    "Action": "Passive",
                }
            },
            {
                "id": "barbarian_reckless_attack",
                "name": "Reckless Attack",
                "summary": "Gain Advantage on Strength attacks for the turn; attackers gain Advantage against you.",
                "description": "You can throw aside all concern for defense to attack with fierce desperation. When you make your first attack on your turn, you can decide to attack recklessly. Doing so gives you Advantage on melee weapon attack rolls using Strength during this turn, but attack rolls against you have Advantage until your next turn.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        3: [
            {
                "id": "barbarian_subclass",
                "name": "Barbarian Subclass",
                "type": "subclass_choice",
                "summary": "Choose a subclass: Path of the Berserker, Path of the Wild Heart, Path of the World Tree, or Path of the Zealot.",
                "description": "You choose a path that shapes the nature of your rage. Your choice grants you features at 3rd level and again at 6th, 10th, and 14th levels.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": ["berserker", "wild_heart", "world_tree", "zealot"]
                    },
                    "note": "Grants features at various levels."
                }
            },
            {
                "id": "barbarian_primal_knowledge",
                "name": "Primal Knowledge",
                "summary": "Gain 1 Barbarian skill; can use Strength for select ability checks while raging.",
                "description": "Your connection to your primal heritage allows you to draw on your physical might to bolster your skills. You gain proficiency in another skill from the Barbarian skill list. Additionally, while your Rage is active, you can use Strength instead of another ability for checks in certain skills, such as Acrobatics, Intimidation, Perception, Stealth, or Survival.",
                "details": {
                    "Action": "Passive",
                    "skills_affected": ["Acrobatics", "Intimidation", "Perception", "Stealth", "Survival"]
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "description": "You can further specialize your character's talents. You can either increase two ability scores by 1, increase one ability score by 2, or choose a powerful Feat to gain new capabilities.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        5: [
            {
                "id": "barbarian_extra_attack",
                "name": "Extra Attack",
                "summary": "Attack twice when taking the Attack action.",
                "description": "You can attack twice, instead of once, whenever you take the Attack action on your turn.",
                "details": {
                    "Action": "Passive",
                }
            },
            {
                "id": "barbarian_fast_movement",
                "name": "Fast Movement",
                "summary": "+10 ft movement while not wearing Heavy armor.",
                "description": "Your speed increases by 10 feet while you aren't wearing Heavy armor.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        6: [
            {
                "id": "barbarian_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Barbarian subclass.",
                "description": "You gain a new ability based on the Path you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        7: [
            {
                "id": "barbarian_feral_instinct",
                "name": "Feral Instinct",
                "summary": "Advantage on Initiative.",
                "description": "Your instincts are so whetted that you have Advantage on Initiative rolls, helping you act quickly when combat begins.",
                "details": {
                    "Action": "Passive",
                }
            },
            {
                "id": "barbarian_instinctive_pounce",
                "name": "Instinctive Pounce",
                "summary": "Move up to half speed when you Rage.",
                "description": "As part of the Bonus Action you take to enter your Rage, you can move up to half your Speed.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        9: [
            {
                "id": "barbarian_brutal_strike",
                "name": "Brutal Strike",
                "summary": "Add 1d10 damage and choose an extra effect when attacking recklessly.",
                "description": "You have learned to trade accuracy for pure, destructive power. If you use Reckless Attack, you can choose to make a particularly brutal strike. You forgo Advantage on the attack roll to deal an extra 1d10 damage of the weapon's type and apply one of the tactical effects listed below. You can apply only one such effect per turn.\n\n- **Forceful Blow**: Push the target 15 feet away.\n- **Hamstring Blow**: Reduce the target's speed by 15 feet.",
                "details": {
                    "Action": "Passive",
                    "damage": "1d10",
                    "options": {
                        "forceful_blow": BRUTAL_STRIKE_OPTIONS["forceful_blow"],
                        "hamstring_blow": BRUTAL_STRIKE_OPTIONS["hamstring_blow"]
                    }
                }
            }
        ],
        10: [
            {
                "id": "barbarian_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Barbarian subclass.",
                "description": "You gain a new ability based on the Path you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        11: [
            {
                "id": "barbarian_relentless_rage",
                "name": "Relentless Rage",
                "summary": "Make Con save to avoid dropping to 0 HP; unlimited uses but DC starts at 10 and increases by 5 each use, resetting on Short or Long Rest.",
                "description": "Your rage can keep you fighting through even the most grievous wounds. If you drop to 0 hit points while you're raging and don't die outright, you can make a Constitution saving throw. If you succeed, you drop to 1 hit point instead. The DC starts at 10 and increases by 5 each time you use this feature, resetting back to 10 after you finish a Short or Long Rest.",
                "details": {
                    "Action": "Passive",
                    "save": "Constitution",
                    "dc_base": 10,
                    "dc_increment": 5,
                    "recharge": "Short or Long Rest",
                    "recharge_effect": "reset_dc",
                    "uses": "Unlimited",
                    "note": "DC resets to 10 after each Short or Long Rest."
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        13: [
            {
                "id": "barbarian_improved_brutal_strike",
                "name": "Improved Brutal Strike",
                "summary": "Add new options to Brutal Strike: Staggering Blow, Sundering Blow.",
                "description": "Your mastery of brutal combat grows, allowing you to use more advanced tactical strikes that can stagger your foes or leave them vulnerable to your allies. You gain the following additional options for your Brutal Strike:\n\n- **Staggering Blow**: Disadvantage on the next save and no Opportunity Attacks.\n- **Sundering Blow**: Gives allies a +5 bonus to hit the target.",
                "details": {
                    "Action": "Passive",
                    "added_options": {
                        "staggering_blow": BRUTAL_STRIKE_OPTIONS["staggering_blow"],
                        "sundering_blow": BRUTAL_STRIKE_OPTIONS["sundering_blow"]
                    }
                }
            }
        ],
        14: [
            {
                "id": "barbarian_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Barbarian subclass.",
                "description": "You gain a final, powerful ability based on the Path you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        15: [
            {
                "id": "barbarian_persistent_rage",
                "name": "Persistent Rage",
                "summary": "Rage lasts 10 minutes without needing extensions; regains all Rage uses on Initiative (once per Long Rest).",
                "description": "Your rage is so fierce that it now lasts for the full 10 minutes regardless of whether you attack or take damage. Additionally, once per Long Rest, if you roll Initiative and have no Rage uses left, you regain all your Rage uses immediately.",
                "details": {
                    "Action": "Passive",
                    "uses": 1,
                    "recharge": "Long Rest",
                    "recharge_effect": "restore_feature",
                    "restore_target": "barbarian_rage",
                    "trigger": "Initiative",
                    "note": "When triggered on Initiative: restores all Rage uses. The trigger itself recharges on Long Rest."
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        17: [
            {
                "id": "barbarian_brutal_strike_upgrade",
                "name": "Brutal Strike Upgrade",
                "summary": "Damage increases to 2d10; apply two effects at once.",
                "description": "Your Brutal Strikes become devastating. The extra damage increases to 2d10, and you can now apply two different tactical effects from your Brutal Strike options to the same target simultaneously.",
                "details": {
                    "Action": "Passive",
                    "damage": "2d10",
                    "effects_count": 2
                }
            }
        ],
        18: [
            {
                "id": "barbarian_indomitable_might",
                "name": "Indomitable Might",
                "summary": "Use Strength score instead of total if you roll lower on Strength checks/saves.",
                "description": "Your physical strength is so great that you can't be easily overpowered. If your total for a Strength check or Strength saving throw is less than your Strength score, you can use your score in place of the total.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat.",
                "description": "You reach the pinnacle of mortality. You can choose a legendary Epic Boon or another powerful Feat to cement your legacy.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        20: [
            {
                "id": "barbarian_primal_champion",
                "name": "Primal Champion",
                "summary": "Str and Con scores increase by 4, to a max of 25.",
                "description": "You embody the raw power of the wild. Your Strength and Constitution scores increase by 4, and your maximum for those scores is now 25.",
                "details": {
                    "Action": "Passive",
                }
            }
        ]
    }
}

BARD = {
    "id": "bard",
    "name": "Bard",
    "subclasses": BARD_SUBCLASSES,
    "description": """Bards weave magic through performance, turning memory, rhythm, and spoken word into tools of power.
        Driven by curiosity and the spark of creation, they collect fragments of history and myth, transforming
        them into magic and influence.""",
    "primary_ability": "Charisma",
    "hit_die": "d8",
    "proficiencies": {
        "saving_throws": ["Dexterity", "Charisma"],
        "armor": ["Light"],
        "weapons": ["Simple"],
        "tools": {
            "granted": [],
            "choose": 3,
            "options": ["Bagpipes", "Drum", "Dulcimer", "Flute", "Horn", "Lute", "Lyre", "Pan Flute", "Shawm", "Viol"]
        },
        "skills": {
            "granted": [],
            "choose": 3,
            "options": [
                "Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight", "Intimidation",
                "Investigation", "Medicine", "Nature", "Perception", "Performance", "Persuasion", "Religion",
                "Sleight of Hand", "Stealth", "Survival"
            ]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Leather Armor", "2 Daggers", "Musical Instrument (choice)", "Entertainer's Pack"],
            "gold": 19
        },
        "option_b": {
            "gold": 90
        }
    },
    "spellcasting": {
        "ability": "Charisma",
        "progression": "full",
        "preparation_mode": "learned",
        "focus": ["Musical Instrument"],
        "recharge": "Long Rest",
        "cantrips_known": {1: 2, 4: 3, 10: 4},
        "spells_prepared": {
            1: 4, 2: 5, 3: 6, 4: 7, 5: 9, 6: 10, 7: 11, 8: 12, 9: 14, 10: 15,
            11: 16, 12: 16, 13: 17, 14: 17, 15: 18, 16: 18, 17: 19, 18: 20, 19: 21, 20: 22
        }
    },
    "features": {
        1: [
            {
                "id": "bard_bardic_inspiration",
                "name": "Bardic Inspiration",
                "summary": "Supernaturally inspire others with a d6; add to failed D20 tests.",
                "description": "You can supernaturally inspire others through words, music, or dance. Using Bardic Inspiration: As a Bonus Action, you can inspire another creature within 60 feet who can see or hear you. That creature gains one Bardic Inspiration die. \n\nWithin the next hour, when the creature fails a D20 Test (an Attack roll, Ability Check, or Saving Throw), the creature can roll the Bardic Inspiration die and add the number rolled to the d20, potentially turning the failure into a success. \n\nA creature can have only one Bardic Inspiration die at a time. The die is expended when it is rolled. If you use this feature while you already have no uses of it remaining, you can't use it again until you finish a Long Rest (or Short Rest after level 5).",
                "details": {
                    "Action": "Bonus Action",
                    "uses": {
                        "type": "ability-mod",
                        "ability": "Charisma"
                    },
                    "recharge": "Long Rest (regain all)",
                    "die": {
                        "type": "level-based",
                        "scaling": {
                            "1-4": "d6",
                            "5-9": "d8",
                            "10-14": "d10",
                            "15-20": "d12"
                        }
                    }
                }
            },
            {
                "id": "bard_spellcasting",
                "name": "Spellcasting",
                "summary": """You can cast spells through bardic arts. You start with 2 cantrips and 4 prepared level 1 spells.
                    Prepared spells increase as you level up. You use Charisma for spellcasting and can use a musical instrument
                    as a spellcasting focus.""",
                "description": "You have learned to untangle and reshape the fabric of reality in harmony with your wishes and music. Your spells are part of your vast repertoire, magic that you can tune to different situations. You use Charisma as your spellcasting ability.",
                "details": {
                    "Action": "Passive",
                    "recharge": "Long Rest"
                }
            }
        ],
        2: [
            {
                "id": "bard_expertise_2",
                "name": "Expertise",
                "summary": "You gain Expertise in two of your skill proficiencies of your choice.",
                "description": "Your proficiency bonus is doubled for any ability check you make that uses either of the chosen proficiencies.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 2,
                        "type": "skill_proficiency"
                    }
                }
            },
            {
                "id": "bard_jack_of_all_trades",
                "name": "Jack Of All Trades",
                "summary": "Add half your Proficiency Bonus (round down) to any ability check for skills you lack.",
                "description": "You can add half your proficiency bonus, rounded down, to any ability check you make that doesn't already include your proficiency bonus.",
                "details": {
                    "Action": "Passive",
                    "bonus": "1/2 Proficiency Bonus (down)"
                }
            }
        ],
        3: [
            {
                "id": "bard_subclass",
                "name": "Bard Subclass",
                "type": "subclass_choice",
                "summary": "Choose a subclass: College Of Dance, College Of Glamour, College Of Lore, or College Of Valor.",
                "description": "You delve into the advanced techniques of a bardic college of your choice. Your choice grants you features at 3rd level and again at 6th and 14th levels.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": ["dance", "glamour", "lore", "valor"]
                    },
                    "note": "Grants features at various levels."
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        5: [
            {
                "id": "bard_font_of_inspiration",
                "name": "Font Of Inspiration",
                "summary": "Regain Bardic Inspiration on Short or Long Rest; can expend spell slots to regain uses.",
                "description": "Your inspiration is now more readily available. You regain all of your expended uses of Bardic Inspiration when you finish a Short or Long Rest. \n\nIn addition, you can now expend a spell slot (no Action required) to regain one use of your Bardic Inspiration. You can do so only if you have at least one spell slot remaining and no uses of Bardic Inspiration left.",
                "details": {
                    "Action": "Passive",
                    "recharge": "Short or Long Rest",
                    "recharge_change": "bard_bardic_inspiration",
                    "spell_slot_conversion": "Expend 1 slot to regain 1 use (no Action required)"
                }
            }
        ],
        6: [
            {
                "id": "bard_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Bard subclass.",
                "description": "You gain a new ability based on the Bardic College you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        7: [
            {
                "id": "bard_countercharm",
                "name": "Countercharm",
                "summary": "Use a Reaction to cause a creature to reroll a failed save against Charm or Fear with Advantage.",
                "description": "You gain the ability to use musical notes or words of power to disrupt mind-influencing effects. As a Reaction, you can help an ally reroll a failed save against being Charmed or Frightened.",
                "details": {
                    "Action": "Reaction",
                    "reaction_trigger": "Failure against Charmed or Frightened",
                    "range": "30 ft",
                    "benefit": "Reroll with Advantage"
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        9: [
            {
                "id": "bard_expertise_9",
                "name": "Expertise",
                "summary": "Gain Expertise in two more skill proficiencies of your choice.",
                "description": "You choose two more of your skill proficiencies to become an expert in, further doubling your Proficiency Bonus for those skills.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 2,
                        "type": "skill_proficiency"
                    }
                }
            }
        ],
        10: [
            {
                "id": "bard_magical_secrets_10",
                "name": "Magical Secrets",
                "summary": "Prepare spells from Bard, Cleric, Druid, and Wizard lists.",
                "description": "You have plundered magical knowledge from a wide spectrum of disciplines. Whenever your number of Prepared Spells increases (as shown in the Bard table), you can choose to prepare spells from the Cleric, Druid, and Wizard spell lists in addition to the Bard spell list. \n\nA spell you prepare via this feature counts as a Bard spell for you, and it must be of a level for which you have spell slots.",
                "details": {
                    "Action": "Passive",
                    "list_access": ["Bard", "Cleric", "Druid", "Wizard"],
                    "note": "Chosen spells count as Bard spells."
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        14: [
            {
                "id": "bard_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Bard subclass.",
                "description": "You gain a final, powerful ability based on the Bardic College you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        18: [
            {
                "id": "bard_superior_inspiration",
                "name": "Superior Inspiration",
                "summary": "Regain Bardic Inspiration uses until you have at least two when rolling Initiative.",
                "description": "When you roll Initiative and have 0 or 1 use of Bardic Inspiration left, you regain uses until you have 2.",
                "details": {
                    "Action": "Passive",
                    "trigger": "Initiative",
                    "restoration": "Up to 2 uses"
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        20: [
            {
                "id": "bard_words_of_creation",
                "name": "Words Of Creation",
                "summary": "Always have Power Word Heal and Power Word Kill prepared; can target a second creature.",
                "description": "Your mastery of the bardic arts allows you to utter words that can mend or end lives. You always have the Power Word Heal and Power Word Kill spells prepared, and you can now target a second creature with these spells.",
                "details": {
                    "Action": "Passive",
                    "spells_granted": ["Power Word Heal", "Power Word Kill"],
                    "benefit": "Target a second creature within 10 ft of the first."
                }
            }
        ]
    }
}

CLERIC = {
    "id": "cleric",
    "name": "Cleric",
    "subclasses": CLERIC_SUBCLASSES,
    "description": """Clerics are intermediaries between the mortal world and they were given powers resembling those of the gods. 
        Empowered by divine magic, they serve as healers, protectors, and harbingers of their deity's will. 
        Wielding both holy light and martial might, a Cleric is a pillar of strength for any adventuring party.""",
    "primary_ability": "Wisdom",
    "hit_die": "d8",
    "proficiencies": {
        "saving_throws": ["Wisdom", "Charisma"],
        "armor": ["Light", "Medium", "Shields"],
        "weapons": ["Simple"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["History", "Insight", "Medicine", "Persuasion", "Religion"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Chain Shirt", "Shield", "Mace", "Holy Symbol", "Priest's Pack"],
            "gold": 7
        },
        "option_b": {
            "gold": 110
        }
    },
    "spellcasting": {
        "ability": "Wisdom",
        "progression": "full",
        "preparation_mode": "prepared",
        "focus": ["Holy Symbol"],
        "recharge": "Long Rest",
        "cantrips_known": {1: 3, 4: 4, 10: 5},
        "spells_prepared": {
            1: 4, 2: 5, 3: 6, 4: 7, 5: 9, 6: 10, 7: 11, 8: 12, 9: 14, 10: 15,
            11: 16, 12: 16, 13: 17, 14: 17, 15: 18, 16: 18, 17: 19, 18: 20, 19: 21, 20: 22
        }
    },
    "features": {
        1: [
            {
                "id": "cleric_spellcasting",
                "name": "Spellcasting",
                "summary": "You can cast spells through divine power. You start with 3 cantrips and use Wisdom as your spellcasting ability.",
                "description": "As a conduit for divine power, you can cast Cleric spells. You use Wisdom as your spellcasting ability and can use a Holy Symbol as a spellcasting focus. Every day you can prepare a list of spells to have ready.",
                "details": {
                    "Action": "Passive",
                    "recharge": "Long Rest"
                }
            },
            {
                "id": "cleric_divine_order",
                "name": "Divine Order",
                "summary": "Choose a sacred role: Protector or Thaumaturge.",
                "description": "You have dedicated yourself to a particular sacred role within your divine order. Choose one of the following options:\n\n- **Protector**: You gain proficiency with Martial weapons and training with Heavy armor.\n- **Thaumaturge**: You gain one extra Cleric cantrip of your choice. You also add your Wisdom modifier (minimum of +1) to your Intelligence (Arcana or Religion) checks.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": [
                            {
                                "name": "Protector",
                                "benefit": "Proficiency with Martial weapons and training with Heavy armor."
                            },
                            {
                                "name": "Thaumaturge",
                                "benefit": "Gain one extra Cleric cantrip. Add Wisdom modifier (min +1) to Intelligence (Arcana or Religion) checks."
                            }
                        ]
                    }
                }
            }
        ],
        2: [
            {
                "id": "cleric_channel_divinity",
                "name": "Channel Divinity",
                "summary": "Use divine energy for special effects like Divine Spark or Turn Undead.",
                "description": "You gain the ability to channel divine energy directly from your deity to fuel magical effects. You start with two such effects: Divine Spark and Turn Undead.",
                "details": {
                    "Action": "Action",
                    "uses": {
                        "type": "level-based",
                        "scaling": {
                            "2-5": 2,
                            "6-17": 3,
                            "18-20": 4
                        }
                    },
                    "recharge": "Short Rest (regain 1), Long Rest (regain all)",
                    "save_dc": "8 + Proficiency Bonus + Wisdom modifier",
                    "effects": [
                        {
                            "name": "Divine Spark",
                            "summary": "Heal or damage a creature within 30ft.",
                            "details": {
                                "Action": "Action",
                                "range": "30 ft",
                                "scaling": {
                                    "2-6": "1d8 + WIS",
                                    "7-12": "2d8 + WIS",
                                    "13-17": "3d8 + WIS",
                                    "18-20": "4d8 + WIS"
                                },
                                "effect": "Restore HP or deal Necrotic/Radiant damage (Constitution save for half)."
                            }
                        },
                        {
                            "name": "Turn Undead",
                            "summary": "Undead within 30ft must save or be Frightened and Incapacitated for 1 minute. On their turn they try to move as far away from you as possible.",
                            "details": {
                                "Action": "Action",
                                "range": "30 ft",
                                "save": "Wisdom",
                                "duration": "1 minute or until damaged"
                            }
                        }
                    ]
                }
            }
        ],
        3: [
            {
                "id": "cleric_subclass",
                "name": "Cleric Subclass",
                "type": "subclass_choice",
                "summary": "Choose a divine domain: Life, Light, Trickery, or War.",
                "description": "You choose a divine domain related to your deity. Your choice grants you domain spells and other special features at 3rd level and again at 6th and 17th levels.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": ["life", "light", "trickery", "war"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        5: [
            {
                "id": "cleric_sear_undead",
                "name": "Sear Undead",
                "summary": "Turn Undead deals Radiant damage to those who fail their save.",
                "description": "Whenever you use your Turn Undead feature, you also deal Radiant damage to each affected creature that fails its saving throw. The damage equals a number of d8s equal to your Wisdom modifier (minimum of 1d8). This damage does not end the Turn Undead effect.",
                "details": {
                    "Action": "Passive",
                    "damage": "Xd8 (where X is Wisdom modifier, min 1)",
                    "type": "Radiant",
                    "note": "Does not end the Turn Undead effect."
                }
            }
        ],
        6: [
            {
                "id": "cleric_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Cleric subclass.",
                "description": "You gain a new ability based on the Divine Domain you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        7: [
            {
                "id": "cleric_blessed_strikes",
                "name": "Blessed Strikes",
                "summary": "Choose Divine Strike (+1d8 weapon damage) or Potent Spellcasting (+WIS to cantrip damage).",
                "description": "You are blessed with divine might in battle. You can choose to either add your Wisdom modifier to the damage of your Cleric cantrips or deal an extra 1d8 Radiant damage once per turn with a weapon attack.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": [
                            {
                                "name": "Divine Strike",
                                "benefit": "Once per turn, +1d8 Necrotic or Radiant damage on a weapon hit."
                            },
                            {
                                "name": "Potent Spellcasting",
                                "benefit": "Add Wisdom modifier to damage dealt with Cleric cantrips."
                            }
                        ]
                    }
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        10: [
            {
                "id": "cleric_divine_intervention",
                "name": "Divine Intervention",
                "summary": "As a Magic Action, cast any Cleric spell of level 5 or lower.",
                "description": "You can call on your deity to intervene on your behalf. As a Magic action, you can request any Cleric spell of 5th level or lower (that doesn't require a Reaction) to take effect immediately. You don't need to meet the spell's requirements, including components or a spell slot. Once you use this feature, you can't use it again until you finish a Long Rest.",
                "details": {
                    "Action": "Action",
                    "limit": "Level 5 or lower Cleric spell",
                    "recharge": "Long Rest"
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        14: [
            {
                "id": "cleric_improved_blessed_strikes",
                "name": "Improved Blessed Strikes",
                "summary": "Your Blessed Strikes choice becomes more powerful.",
                "description": "Your divine blessing grows more potent, either increasing your strike damage or granting temporary hit points when using cantrips.",
                "details": {
                    "Action": "Passive",
                    "divine_strike_upgrade": "+2d8 total damage",
                    "potent_spellcasting_upgrade": "Dealing cantrip damage also grants Temp HP (2x WIS mod) to you or an ally within 60ft."
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        17: [
            {
                "id": "cleric_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Cleric subclass.",
                "description": "You gain a final, powerful ability based on the Divine Domain you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        20: [
            {
                "id": "cleric_greater_divine_intervention",
                "name": "Greater Divine Intervention",
                "summary": "Use Divine Intervention to cast a level 9 Cleric spell.",
                "description": "Your connection with your deity is so powerful that you can now request a 9th-level spell through your Divine Intervention. If you use your Divine Intervention to cast a 9th-level spell, you cannot use it again for 2d4 Long Rests.",
                "details": {
                    "Action": "Passive",
                    "upgrade": "Can cast Level 9 Cleric spells",
                    "recharge": "2d4 Long Rests",
                    "recharge_logic": "variable_long_rests",
                    "recharge_penalty": "If level 9 is used, cannot use again for 2d4 Long Rests."
                }
            }
        ]
    }
}

DRUID = {
    "id": "druid",
    "name": "Druid",
    "subclasses": DRUID_SUBCLASSES,
    "description": """Druids are conduits of the natural world's raw power, channeling the elements and assuming the 
        forms of beasts. They serve as guardians of the wilderness, balancing the cycles of life and death, 
        and drawing magic from the ancient rhythms of nature itself.""",
    "primary_ability": "Wisdom",
    "hit_die": "d8",
    "proficiencies": {
        "saving_throws": ["Intelligence", "Wisdom"],
        "armor": ["Light", "Shields"],
        "weapons": ["Simple"],
        "tools": {
            "granted": ["Herbalism Kit"],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Arcana", "Animal Handling", "Insight", "Medicine", "Nature", "Perception", "Religion", "Survival"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Leather Armor", "Shield", "Sickle", "Druidic Focus (Quarterstaff)", "Explorer's Pack", "Herbalism Kit"],
            "gold": 9
        },
        "option_b": {
            "gold": 50
        }
    },
    "spellcasting": {
        "ability": "Wisdom",
        "progression": "full",
        "preparation_mode": "prepared",
        "focus": ["Druidic Focus"],
        "recharge": "Long Rest",
        "cantrips_known": {1: 2, 4: 3, 10: 4},
        "spells_prepared": {
            1: 4, 2: 5, 3: 6, 4: 7, 5: 9, 6: 10, 7: 11, 8: 12, 9: 14, 10: 15,
            11: 16, 12: 16, 13: 17, 14: 17, 15: 18, 16: 18, 17: 19, 18: 20, 19: 21, 20: 22
        }
    },
    "features": {
        1: [
            {
                "id": "druid_spellcasting",
                "name": "Spellcasting",
                "summary": "Cast spells using Wisdom and a Druidic Focus; swap your entire spell list after a Long Rest.",
                "description": "Drawing on the divine essence of nature itself, you can cast spells to shape that essence to your will. You use Wisdom as your spellcasting ability and can use a Druidic Focus as a conduit for your magic. After a Long Rest, you can change your list of prepared spells by communion with nature.",
                "details": {
                    "Action": "Passive",
                    "recharge": "Long Rest"
                }
            },
            {
                "id": "druid_druidic",
                "name": "Druidic",
                "summary": "Know the secret language of Druids and always have Speak with Animals prepared.",
                "description": "You know Druidic, the secret language of Druids. You can speak the language and use it to leave hidden messages. Additionally, your connection to nature is so strong that you always have the Speak with Animals spell prepared.",
                "details": {
                    "Action": "Passive",
                    "spells_granted": ["Speak with Animals"],
                    "language": "Druidic",
                    "hidden_messages_dc": 15
                }
            },
            {
                "id": "druid_primal_order",
                "name": "Primal Order",
                "summary": "Choose a sacred role: Magician or Warden.",
                "description": "You dedicated yourself to a particular sacred role within a druidic order. Choose one of the following options:\n\n- **Magician**: You gain one extra Druid cantrip of your choice. You also add your Wisdom modifier (minimum of +1) to your Intelligence (Arcana or Nature) checks.\n- **Warden**: You gain proficiency with Martial weapons and training with Medium armor.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": [
                            {
                                "name": "Magician",
                                "benefit": "Extra Druid cantrip. Add Wisdom modifier (min +1) to Intelligence (Arcana or Nature) checks."
                            },
                            {
                                "name": "Warden",
                                "benefit": "Proficiency with Martial weapons and training with Medium armor."
                            }
                        ]
                    }
                }
            }
        ],
        2: [
            {
                "id": "druid_wild_shape",
                "name": "Wild Shape",
                "summary": "Shape-shift into a Beast form as a Bonus Action.",
                "description": "The power of nature allows you to assume the form of a beast. As a Bonus Action, you magically assume the shape of a beast that you have seen before and which meets the requirements shown in the Wild Shape table. \n\nWhile in this form, you gain the following benefits: \n- **Temporary Hit Points**: You gain Temporary Hit Points equal to your Druid level. \n- **Statistics**: Your game statistics are replaced by the statistics of the beast, but you retain your alignment, personality, and Intelligence, Wisdom, and Charisma scores. You also retain all of your skill and saving throw proficiencies. \n- **No Spellcasting**: You can't cast spells (until level 18), and your ability to speak or take any action that requires hands is limited by the beast's form. \n\nYour Wild Shape lasts for a number of hours equal to half your Druid level (rounded down) or until you use a Bonus Action to leave it, you drop to 0 Hit Points, or you die.",
                "details": {
                    "Action": "Bonus Action",
                    "uses": {
                        "type": "level-based",
                        "scaling": {
                            "2-5": 2,
                            "6-16": 3,
                            "17-20": 4
                        }
                    },
                    "recharge": "Short Rest (regain 1), Long Rest (regain all)",
                    "duration": "Hours equal to half Druid level",
                    "hp_granted": "Druid level (Temporary HP)",
                    "forms": {
                        "scaling": {
                            "2-3": {"known": 4, "max_cr": "1/4", "fly": False},
                            "4-7": {"known": 6, "max_cr": "1/2", "fly": False},
                            "8-20": {"known": 8, "max_cr": "1", "fly": True}
                        }
                    }
                }
            },
            {
                "id": "druid_wild_companion",
                "name": "Wild Companion",
                "summary": "Expend a spell slot or Wild Shape use to cast Find Familiar (Fey) as a Magic Action.",
                "description": "You gain the ability to summon a spirit that embodies a part of the wilderness. You can expend a use of Wild Shape or a spell slot to cast the Find Familiar spell without material components. The familiar summoned is a Fey spirit.",
                "details": {
                    "Action": "Action",
                    "resource": "Spell slot or Wild Shape use",
                    "familiar_type": "Fey",
                    "duration": "Until Long Rest"
                }
            }
        ],
        3: [
            {
                "id": "druid_subclass",
                "name": "Druid Subclass",
                "type": "subclass_choice",
                "summary": "Choose a Druidic Circle: Land, Moon, Sea, or Stars.",
                "description": "You choose to join a Druidic Circle that shapes your connection to the natural world. Your choice grants you features at 3rd level and again at 6th, 10th, and 14th levels.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": ["land", "moon", "sea", "stars"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "description": "You can further specialize your character's talents by increasing your ability scores or choosing a new Feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        5: [
            {
                "id": "druid_wild_resurgence",
                "name": "Wild Resurgence",
                "summary": "Convert spell slots to Wild Shape uses, or once per Long Rest, convert a Wild Shape use into a Level 1 spell slot.",
                "description": "Your connection to the primal forces allows you to shift energy between your magical forms. You can convert spell slots into uses of Wild Shape, or once per day, use a Wild Shape charge to regain a 1st-level spell slot.",
                "details": {
                    "Action": "Passive",
                    "slot_to_wild_shape": "Expend spell slot to gain 1 use (if none left, 1/turn)",
                    "recharge": "Long Rest",
                    "wild_shape_to_slot": "Expend 1 use to gain Level 1 slot (1/Long Rest)"
                }
            }
        ],
        6: [
            {
                "id": "druid_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Druid subclass.",
                "description": "You gain a new ability based on the Druidic Circle you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        7: [
            {
                "id": "druid_elemental_fury",
                "name": "Elemental Fury",
                "summary": "Choose Potent Spellcasting (+WIS to cantrip damage) or Primal Strike (+1d8 elemental damage on hits).",
                "description": "You can channel the raw fury of the elements through your magic or your physical attacks. You choose whether to bolster the power of your cantrips with your Wisdom or imbue your strikes with elemental energy.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": [
                            {
                                "name": "Potent Spellcasting",
                                "benefit": "Add Wisdom modifier to Druid cantrip damage."
                            },
                            {
                                "name": "Primal Strike",
                                "benefit": "Once per turn, +1d8 Cold, Fire, Lightning, or Thunder damage on a weapon or beast attack."
                            }
                        ]
                    }
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "description": "You can further specialize your character's talents by increasing your ability scores or choosing a new Feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        10: [
            {
                "id": "druid_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Druid subclass.",
                "description": "You gain a new ability based on the Druidic Circle you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "description": "You can further specialize your character's talents by increasing your ability scores or choosing a new Feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        14: [
            {
                "id": "druid_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Druid subclass.",
                "description": "You gain a final, powerful ability based on the Druidic Circle you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        15: [
            {
                "id": "druid_improved_elemental_fury",
                "name": "Improved Elemental Fury",
                "summary": "Your Elemental Fury choice becomes more powerful.",
                "description": "Your mastery over elemental forces reaches its peak, making your previous Elemental Fury choice even more devastating.",
                "details": {
                    "Action": "Passive",
                    "potent_spellcasting_upgrade": "Range increases by 300 ft for cantrips with range >= 10 ft.",
                    "primal_strike_upgrade": "Extra damage increases to 2d8."
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "description": "You can further specialize your character's talents by increasing your ability scores or choosing a new Feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        18: [
            {
                "id": "druid_beast_spells",
                "name": "Beast Spells",
                "summary": "While using Wild Shape, you can cast spells in Beast form (unless material cost/consumption is involved).",
                "description": "You can now channel your magic even while in the form of a beast. You can cast most of your Druid spells while using Wild Shape, provided they don't have expensive or consumed material components.",
                "details": {
                    "Action": "Passive",
                    "restriction": "No spells with specified material cost or consumed components."
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat.",
                "description": "You reach the pinnacle of mortality. You can choose a legendary Epic Boon or another powerful Feat to cement your legacy.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        20: [
            {
                "id": "druid_archdruid",
                "name": "Archdruid",
                "summary": "Regain Wild Shape on Initiative, and other powerful nature benefits.",
                "description": "You have become a master of the natural world. You gain the following benefits: \n\n- **Evergreen Wild Shape**: Whenever you roll Initiative and have no uses of Wild Shape left, you regain one use.\n- **Nature Magician**: You can convert uses of Wild Shape into spell slots. As a Magic action, you can expend a number of Wild Shape uses to regain a spell slot of a level equal to twice the number of uses expended (to a maximum of 5th level). You can use this benefit only once per Long Rest.\n- **Longevity**: The primal magic that you wield causes you to age more slowly. For every 10 years that pass, your body ages only 1 year.",
                "details": {
                    "Action": "Action",
                    "evergreen_wild_shape": "Regain 1 use on Initiative if none are left.",
                    "recharge": "Long Rest",
                    "nature_magician": "Convert multiple Wild Shape uses into a single spell slot (1 use = 2 spell levels, 1/Long Rest).",
                    "longevity": "Age 1 year for every 10 years passed."
                }
            }
        ]
    }
}

FIGHTER = {
    "id": "fighter",
    "name": "Fighter",
    "subclasses": FIGHTER_SUBCLASSES,
    "description": """Fighters are masters of martial combat, skilled with a variety of weapons and armor. 
        Whether a disciplined soldier, a rugged mercenary, or a knightly champion, a Fighter excels on the 
        front lines, using tactical expertise and physical prowess to dominate the battlefield.""",
    "primary_ability": "Strength or Dexterity",
    "hit_die": "d10",
    "proficiencies": {
        "saving_throws": ["Strength", "Constitution"],
        "armor": ["Light", "Medium", "Heavy", "Shields"],
        "weapons": ["Simple", "Martial"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Acrobatics", "Animal Handling", "Athletics", "History", "Insight", "Intimidation", "Persuasion", "Perception", "Survival"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Chain Mail", "Greatsword", "Flail", "8 Javelins", "Dungeoneer's Pack"],
            "gold": 4
        },
        "option_b": {
            "items": ["Studded Leather Armor", "Scimitar", "Shortsword", "Longbow", "20 Arrows", "Quiver", "Dungeoneer's Pack"],
            "gold": 11
        },
        "option_c": {
            "gold": 155
        }
    },
    "features": {
        1: [
            {
                "id": "fighter_fighting_style",
                "name": "Fighting Style",
                "summary": "Gain a Fighting Style feat of your choice; replaceable on level up.",
                "description": "Your training has focused on a particular style of combat. You gain one Fighting Style feat of your choice, such as Archery, Defense, Dueling, Great Weapon Fighting, Protection, or Two-Weapon Fighting. \n\nCombat is your way of life, and you have mastered its various forms. Whenever you gain a Fighter level, you can replace the Fighting Style feat you have with another Fighting Style feat.",
                "details": {
                    "Action": "Passive",
                    "Choice": "Choose 1 Fighting Style Feat",
                    "Flexibility": "Replaceable upon leveling up"
                }
            },
            {
                "id": "fighter_second_wind",
                "name": "Second Wind",
                "summary": "Use a Bonus Action to regain 1d10 + Fighter level HP.",
                "description": "You have a limited well of stamina that you can draw on to protect yourself from harm. On your turn, you can use a Bonus Action to regain hit points equal to 1d10 + your Fighter level.",
                "details": {
                    "Action": "Bonus Action",
                    "Regain": "1d10 + Fighter Level",
                    "uses": {
                        "1-3": 2,
                        "4-9": 3,
                        "10-20": 4
                    },
                    "recharge": "Short Rest (regain 1), Long Rest (regain all)"
                }
            },
            {
                "id": "fighter_weapon_mastery",
                "name": "Weapon Mastery",
                "summary": "Learn the mastery properties of three weapons; can change one choice after a Long Rest.",
                "description": "Your training with weapons allows you to use the mastery properties of particular weapons. You gain the mastery properties of three weapons of your choice. Whenever you finish a Long Rest, you can practice weapons and change one of those choices.",
                "details": {
                    "Action": "Passive",
                    "Initial Choices": "3 Weapons",
                    "Scaling": {
                        "1-3": "3 Choices",
                        "4-9": "4 Choices",
                        "10-15": "5 Choices",
                        "16-20": "6 Choices"
                    },
                    "recharge": "Long Rest",
                    "recharge_effect": "swap_weapon_mastery",
                    "Maintenance": "Can change 1 choice per Long Rest"
                }
            }
        ],
        2: [
            {
                "id": "fighter_action_surge",
                "name": "Action Surge",
                "summary": "Take one additional action (except Magic) on your turn.",
                "description": "You can push yourself beyond your normal limits for a moment. On your turn, you can take one additional action of any kind, provided that it is not the Magic action. This additional action must be taken on the same turn you use this feature.",
                "details": {
                    "Action": "Passive",
                    "uses": {
                        "2-16": 1,
                        "17-20": 2
                    },
                    "Restriction": "Cannot be used for Magic action; once per turn",
                    "recharge": "Short or Long Rest"
                }
            },
            {
                "id": "fighter_tactical_mind",
                "name": "Tactical Mind",
                "summary": "Expend a Second Wind use to add 1d10 to a failed ability check; use isn't expended if the check still fails.",
                "description": "You have a mind for tactics that can apply to more than just combat. When you fail an ability check, you can expend one use of your Second Wind to roll 1d10 and add the number rolled to the total, potentially turning the failure into a success. If the check still fails, the use of Second Wind is not expended.",
                "details": {
                    "Action": "Passive",
                    "Benefit": "+1d10 to failed ability check",
                    "Cost": "1 Second Wind use",
                    "Safety": "Not expended if check still fails"
                }
            }
        ],
        3: [
            {
                "id": "fighter_subclass",
                "name": "Fighter Subclass",
                "type": "subclass_choice",
                "summary": "Choose a martial archetype: Battle Master, Champion, Eldritch Knight, or Psi Warrior.",
                "description": "You choose a martial archetype that defines your combat style. Your choice grants you features at 3rd level and again at 7th, 10th, 15th, and 18th levels.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": ["battle_master", "champion", "eldritch_knight", "psi_warrior"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        5: [
            {
                "id": "fighter_extra_attack",
                "name": "Extra Attack",
                "summary": "Attack twice when taking the Attack action.",
                "description": "You can attack twice, instead of once, whenever you take the Attack action on your turn. The number of attacks increases to three when you reach 11th level and to four when you reach 20th level in this class.",
                "details": {
                    "Action": "Passive",
                }
            },
            {
                "id": "fighter_tactical_shift",
                "name": "Tactical Shift",
                "summary": "Move up to half your speed without provoking opportunity attacks when using Second Wind.",
                "description": "Whenever you use your Second Wind feature, you can move up to half your Speed without provoking Opportunity Attacks.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        6: [
            {
                "id": "feat_or_asi_6",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "description": "You can further specialize your character's talents by increasing your ability scores or choosing a new Feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        7: [
            {
                "id": "fighter_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Fighter subclass.",
                "description": "You gain a new ability based on the Martial Archetype you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        9: [
            {
                "id": "fighter_indomitable",
                "name": "Indomitable",
                "summary": "Reroll a failed saving throw with a bonus equal to your Fighter level.",
                "description": "You can call on your inner strength to overcome a mental or physical challenge. When you fail a saving throw, you can reroll it and add your Fighter level to the new roll.",
                "details": {
                    "Action": "Passive",
                    "uses": {
                        "type": "level-based",
                        "scaling": {
                            "9-12": 1,
                            "13-16": 2,
                            "17-20": 3
                        }
                    },
                    "recharge": "Long Rest",
                    "bonus": "Fighter Level"
                }
            },
            {
                "id": "fighter_tactical_master",
                "name": "Tactical Master",
                "summary": "Replace a weapon's mastery property for an attack.",
                "description": "Your mastery of combat allows you to apply different tactical effects to your attacks, regardless of the weapon you are using. Whenever you hit a creature with a weapon you have mastered, you can replace the weapon's normal mastery property with one of the following tactical masteries:\n\n- **Push**: The target is pushed 10 feet away.\n- **Sap**: The target has Disadvantage on its next attack roll.\n- **Slow**: The target's Speed is reduced by 10 feet.",
                "details": {
                    "Action": "Passive",
                    "options": ["Push", "Sap", "Slow"]
                }
            }
        ],
        10: [
            {
                "id": "fighter_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Fighter subclass.",
                "description": "You gain a new ability based on the Martial Archetype you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        11: [
            {
                "id": "fighter_extra_attack_2",
                "name": "Two Extra Attacks",
                "summary": "Attack three times when taking the Attack action.",
                "description": "Your martial skill increases, allowing you to strike even faster. You can attack three times whenever you take the Attack action.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        13: [
            {
                "id": "fighter_studied_attacks",
                "name": "Studied Attacks",
                "summary": "Gain Advantage on your next attack roll against a creature if you miss it.",
                "description": "You learn from your missed strikes. If you miss a creature with an attack, you have Advantage on your next attack against that same creature before the end of your next turn.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        14: [
            {
                "id": "feat_or_asi_14",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "description": "You can further specialize your character's talents by increasing your ability scores or choosing a new Feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        15: [
            {
                "id": "fighter_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Fighter subclass.",
                "description": "You gain a new ability based on the Martial Archetype you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        18: [
            {
                "id": "fighter_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Fighter subclass.",
                "description": "You gain a final, powerful ability based on the Martial Archetype you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        20: [
            {
                "id": "fighter_extra_attack_3",
                "name": "Three Extra Attacks",
                "summary": "Attack four times when taking the Attack action.",
                "description": "You reach the pinnacle of combat mastery. You can attack four times whenever you take the Attack action.",
                "details": {
                    "Action": "Passive",
                }
            }
        ]
    }
}

MONK = {
    "id": "monk",
    "name": "Monk",
    "subclasses": MONK_SUBCLASSES,
    "description": """Monks are masters of martial arts who harness the energy within their bodies to achieve 
        extraordinary physical and mental feats. They value discipline and focus, transforming their own 
        bodies into lethal weapons while moving with supernatural speed and grace.""",
    "primary_ability": "Dexterity and Wisdom",
    "hit_die": "d8",
    "proficiencies": {
        "saving_throws": ["Strength", "Dexterity"],
        "armor": [],
        "weapons": ["Simple", "Martial (with Light property)"],
        "tools": {
            "granted": [],
            "choose": 1,
            "options": [
                "Alchemist's Supplies", "Brewer's Supplies", "Calligrapher's Supplies", "Carpenter's Tools",
                "Cartographer's Tools", "Cobbler's Tools", "Cook's Utensils", "Glassblower's Tools",
                "Jeweler's Tools", "Leatherworker's Tools", "Mason's Tools", "Painter's Supplies",
                "Potter's Tools", "Smith's Tools", "Tinker's Tools", "Weaver's Tools", "Woodcarver's Tools",
                "Bagpipes", "Drum", "Dulcimer", "Flute", "Horn", "Lute", "Lyre", "Pan Flute", "Shawm", "Viol"
            ]
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Acrobatics", "Athletics", "History", "Insight", "Religion", "Stealth"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Spear", "5 Daggers", "Artisan's Tools or Musical Instrument (choice)", "Explorer's Pack"],
            "gold": 11
        },
        "option_b": {
            "gold": 50
        }
    },
    "features": {
        1: [
            {
                "id": "monk_martial_arts",
                "name": "Martial Arts",
                "summary": "Use Dexterity for unarmed strikes and Monk weapons; bonus action strike.",
                "description": "Your practice of martial arts gives you mastery of combat styles that use unarmed strikes and monk weapons. You gain the following benefits: \n\n- **Dexterity Proficiency**: You can use Dexterity instead of Strength for the attack and damage rolls of your Unarmed Strikes and Monk Weapons. \n- **Martial Arts Die**: You can roll a d6 in place of the normal damage of your Unarmed Strike or Monk Weapon. This die increases as you level up. \n- **Bonus Action Strike**: When you take the Attack action on your turn with an Unarmed Strike or a Monk Weapon, you can make one Unarmed Strike as a Bonus Action.",
                "details": {
                    "Action": "Bonus Action",
                    "bonus_action_attack": "1 Unarmed Strike",
                    "die": {
                        "type": "level-based",
                        "scaling": {
                            "1-4": "1d6",
                            "5-10": "1d8",
                            "11-16": "1d10",
                            "17-20": "1d12"
                        }
                    },
                    "dex_for_unarmed": True,
                    "dex_save_dc": "8 + Proficiency Bonus + Dexterity modifier (for Grapple/Shove)"
                }
            },
            {
                "id": "monk_unarmored_defense",
                "name": "Unarmored Defense",
                "summary": "AC = 10 + DEX + WIS when not wearing armor or using a Shield.",
                "description": "While you are wearing no armor and not wielding a shield, your Armor Class equals 10 + your Dexterity modifier + your Wisdom modifier.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        2: [
            {
                "id": "monk_focus",
                "name": "Monk's Focus",
                "summary": "Harness Focus Points for special martial arts maneuvers.",
                "description": "You can harness the focus within yourself to perform extraordinary feats. You have Focus points that you can spend to use the following abilities: \n\n- **Flurry Of Blows**: Immediately after you take the Attack action on your turn, you can spend 1 Focus point to make two Unarmed Strikes as a Bonus Action. \n- **Patient Defense**: You can take the Disengage action as a Bonus Action. Alternatively, you can spend 1 Focus point to take both the Disengage and the Dodge actions as a Bonus Action. \n- **Step Of The Wind**: You can take the Dash action as a Bonus Action. Alternatively, you can spend 1 Focus point to take both the Disengage and the Dash actions as a Bonus Action, and your jump distance is doubled for the turn.",
                "details": {
                    "Action": "Bonus Action",
                    "points": {
                        "type": "level-based",
                        "scaling": {
                            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                            "11": 11, "12": 12, "13": 13, "14": 14, "15": 15, "16": 16, "17": 17, "18": 18, "19": 19, "20": 20
                        }
                    },
                    "recharge": "Short or Long Rest",
                    "save_dc": "8 + Proficiency Bonus + Wisdom modifier",
                    "effects": [
                        {
                            "name": "Flurry Of Blows",
                            "cost": "1 Focus Point",
                            "benefit": "Two Unarmed Strikes as a Bonus Action."
                        },
                        {
                            "name": "Patient Defense",
                            "cost": "0 or 1 Focus Point",
                            "benefit": "Bonus Action Disengage; or expend 1 point for both Disengage and Dodge."
                        },
                        {
                            "name": "Step Of The Wind",
                            "cost": "0 or 1 Focus Point",
                            "benefit": "Bonus Action Dash; or expend 1 point for both Disengage and Dash, with double jump distance."
                        }
                    ]
                }
            },
            {
                "id": "monk_unarmored_movement",
                "name": "Unarmored Movement",
                "summary": "Increase Speed while not wearing armor or using a Shield.",
                "description": "Your speed increases while you are not wearing armor or wielding a shield. This bonus increases as you reach certain monk levels.",
                "details": {
                    "Action": "Passive",
                    "scaling": {
                        "2-5": "+10 ft",
                        "6-9": "+15 ft",
                        "10-13": "+20 ft",
                        "14-17": "+25 ft",
                        "18-20": "+30 ft"
                    }
                }
            },
            {
                "id": "monk_uncanny_metabolism",
                "name": "Uncanny Metabolism",
                "summary": "Once per Long Rest, regain all Focus Points and some HP when rolling Initiative.",
                "description": "Your body has an uncanny ability to recover. When you roll for Initiative, you can regain all your Focus points and some hit points.",
                "details": {
                    "Action": "Passive",
                    "trigger": "Initiative",
                    "healing": "Monk Level + Martial Arts Die",
                    "recharge": "Long Rest"
                }
            }
        ],
        3: [
            {
                "id": "monk_deflect_attacks",
                "name": "Deflect Attacks",
                "summary": "Use a Reaction to reduce damage from Bludgeoning, Piercing, or Slashing attacks.",
                "description": "You can use your reaction to deflect or catch the missile when you are hit by a ranged weapon attack, or to deflect a physical blow.",
                "details": {
                    "Action": "Reaction",
                    "reaction": "When hit by Physical attack",
                    "reduction": "1d10 + DEX + Monk Level",
                    "redirect_cost": "1 Focus Point (if damage reduced to 0)",
                    "redirect_damage": "2 Martial Arts Dice + DEX"
                }
            },
            {
                "id": "monk_subclass",
                "name": "Monk Subclass",
                "type": "subclass_choice",
                "summary": "Choose a monastic tradition: Warrior of Mercy, Shadow, Elements, or Open Hand.",
                "description": "You choose a monastic tradition that you follow. Your choice grants you features at 3rd level and again at 6th, 11th, and 17th levels.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": ["mercy", "shadow", "elements", "open_hand"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "description": "You can further specialize your character's talents by increasing your ability scores or choosing a new Feat.",
                "details": {
                    "Action": "Passive",
                }
            },
            {
                "id": "monk_slow_fall",
                "name": "Slow Fall",
                "summary": "Reduce falling damage by 5x Monk Level as a Reaction.",
                "description": "You can use your reaction when you fall to reduce any falling damage you take by an amount equal to five times your monk level.",
                "details": {
                    "Action": "Reaction",
                }
            }
        ],
        5: [
            {
                "id": "monk_extra_attack",
                "name": "Extra Attack",
                "summary": "Attack twice when taking the Attack action.",
                "description": "You can attack twice, instead of once, whenever you take the Attack action on your turn.",
                "details": {
                    "Action": "Passive",
                }
            },
            {
                "id": "monk_stunning_strike",
                "name": "Stunning Strike",
                "summary": "Expend 1 Focus Point to stun a target until your next turn on a failed Con save.",
                "description": "You can interfere with the focus in an opponent's body. When you hit another creature with a melee weapon attack, you can spend 1 focus point to attempt a stunning strike.",
                "details": {
                    "Action": "Passive",
                    "cost": "1 Focus Point",
                    "save": "Constitution",
                    "fail": "Stunned until start of next turn",
                    "success": "Speed halved, next attack against it has Advantage"
                }
            }
        ],
        6: [
            {
                "id": "monk_empowered_strikes",
                "name": "Empowered Strikes",
                "summary": "Unarmed strikes can deal Force damage instead of Bludgeoning.",
                "description": "Your unarmed strikes can deal Force damage instead of Bludgeoning damage. You choose which damage type to use whenever you hit.",
                "details": {
                    "Action": "Passive",
                }
            },
            {
                "id": "monk_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Monk subclass.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        7: [
            {
                "id": "monk_evasion",
                "name": "Evasion",
                "summary": "Take half damage on failed Dex saves and no damage on successes.",
                "description": "Your instinctive agility lets you dodge out of the way of certain area effects. When you are subjected to an effect that allows you to make a Dexterity saving throw to take only half damage, you instead take no damage if you succeed on the saving throw, and only half damage if you fail.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "description": "You can further specialize your character's talents by increasing your ability scores or choosing a new Feat.",
                "details": {
                    "Action": "Passive",
                }
            },
        ],
        9: [
            {
                "id": "monk_acrobatic_movement",
                "name": "Acrobatic Movement",
                "summary": "Move along vertical surfaces and across liquids without falling.",
                "description": "You gain the ability to move along vertical surfaces and across liquids on your turn without falling during the move.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        10: [
            {
                "id": "monk_heightened_focus",
                "name": "Heightened Focus",
                "summary": "Your Flurry of Blows, Patient Defense, and Step of the Wind become more powerful.",
                "description": "Your mastery of focus becomes even more potent, enhancing your core abilities.",
                "details": {
                    "Action": "Passive",
                    "flurry_upgrade": "Three Unarmed Strikes instead of two.",
                    "defense_upgrade": "Gain Temporary HP (2x Martial Arts dice).",
                    "step_upgrade": "Move a willing creature with you."
                }
            },
            {
                "id": "monk_self_restoration",
                "name": "Self-Restoration",
                "summary": "Remove Charmed, Frightened, or Poisoned at end of turn; no exhaustion from lack of food/drink.",
                "description": "Your internal discipline allows you to shrug off mental and physical ailments. You can now automatically end certain conditions affecting you at the end of your turn.",
                "details": {
                    "Action": "Passive",
                    "conditions": ["Charmed", "Frightened", "Poisoned"]
                }
            }
        ],
        11: [
            {
                "id": "monk_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Monk subclass.",
                "description": "You gain a new ability based on the Monastic Tradition you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "description": "You can further specialize your character's talents by increasing your ability scores or choosing a new Feat.",
                "details": {
                    "Action": "Passive",
                }
            },
        ],
        13: [
            {
                "id": "monk_deflect_energy",
                "name": "Deflect Energy",
                "summary": "Deflect Attacks now works against any damage type.",
                "description": "Your ability to deflect attacks expands to encompass all forms of energy. You can now use your Deflect Attacks feature against any damage type, not just physical blows.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        14: [
            {
                "id": "monk_disciplined_survivor",
                "name": "Disciplined Survivor",
                "summary": "Proficiency in all saving throws; expend 1 Focus Point to reroll a failed save.",
                "description": "Your discipline grants you mastery over your physical and mental responses. You gain proficiency in all saving throws, and you can spend focus to reroll a failed save.",
                "details": {
                    "Action": "Passive",
                    "cost": "1 Focus Point (on failed save)",
                    "benefit": "Reroll saving throw"
                }
            }
        ],
        15: [
            {
                "id": "monk_perfect_focus",
                "name": "Perfect Focus",
                "summary": "Regain Focus Points up to 4 if you have 3 or fewer when rolling Initiative.",
                "description": "Your focus is so refined that it replenishes itself in the heat of battle. If you are low on Focus when combat begins, you instantly regain some of your strength.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "description": "You can further specialize your character's talents by increasing your ability scores or choosing a new Feat.",
                "details": {
                    "Action": "Passive",
                }
            },
        ],
        17: [
            {
                "id": "monk_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Monk subclass.",
                "description": "You gain a final, powerful ability based on the Monastic Tradition you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        18: [
            {
                "id": "monk_superior_defense",
                "name": "Superior Defense",
                "summary": "Expend 3 Focus Points for 1 minute of resistance to all damage except Force.",
                "description": "You can enter a state of heightened defense that shrugs off almost any harm. By spending Focus, you gain resistance to nearly all forms of damage for a short time.",
                "details": {
                    "Action": "Passive",
                    "cost": "3 Focus Points",
                    "duration": "1 minute",
                    "benefit": "Resistance to all damage except Force"
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        20: [
            {
                "id": "monk_body_and_mind",
                "name": "Body And Mind",
                "summary": "Dexterity and Wisdom scores increase by 4, to a maximum of 25.",
                "description": "You have achieved ultimate mastery of your physical form and mental state. Your Dexterity and Wisdom scores increase by 4. Your maximum for those scores is now 25.",
                "details": {
                    "Action": "Passive",
                    "stat_increase": "+4 DEX, +4 WIS",
                    "cap_increase": "Max 25"
                }
            }
        ]
    }
}

PALADIN = {
    "id": "paladin",
    "name": "Paladin",
    "subclasses": PALADIN_SUBCLASSES,
    "description": """Paladins are holy warriors bound by sacred oaths to serve a higher power or cause. 
        They combine martial prowess with divine magic, using their power to heal the wounded, 
        smite the wicked, and protect their allies with powerful auras of grace and courage.""",
    "primary_ability": "Strength and Charisma",
    "hit_die": "d10",
    "proficiencies": {
        "saving_throws": ["Wisdom", "Charisma"],
        "armor": ["Light", "Medium", "Heavy", "Shields"],
        "weapons": ["Simple", "Martial"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Athletics", "Insight", "Intimidation", "Medicine", "Persuasion", "Religion"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Chain Mail", "Shield", "Longsword", "6 Javelins", "Holy Symbol", "Priest's Pack"],
            "gold": 9
        },
        "option_b": {
            "gold": 150
        }
    },
    "spellcasting": {
        "ability": "Charisma",
        "progression": "half",
        "preparation_mode": "prepared",
        "focus": ["Holy Symbol"],
        "recharge": "Long Rest",
        "spells_prepared": {
            1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 6, 7: 7, 8: 7, 9: 9, 10: 9,
            11: 10, 12: 10, 13: 11, 14: 11, 15: 12, 16: 12, 17: 14, 18: 14, 19: 15, 20: 15
        }
    },
    "features": {
        1: [
            {
                "id": "paladin_lay_on_hands",
                "name": "Lay On Hands",
                "summary": "Use a healing pool (5x Paladin Level) to restore HP or remove Poisoned as a Bonus Action.",
                "description": "Your blessed touch can heal wounds and cure ailments. You have a pool of healing power that replenishes when you take a Long Rest.",
                "details": {
                    "Action": "Bonus Action",
                    "pool": "5 * Paladin Level",
                    "recharge": "Long Rest",
                    "poison_removal_cost": 5
                }
            },
            {
                "id": "paladin_spellcasting",
                "name": "Spellcasting",
                "summary": "Cast Paladin spells using Charisma and a Holy Symbol; swap one spell after a Long Rest.",
                "description": "You have learned to cast divine spells through meditation and prayer. You use your Charisma whenever a spell refers to your spellcasting ability.",
                "details": {
                    "Action": "Passive",
                    "recharge": "Long Rest"
                }
            },
            {
                "id": "paladin_weapon_mastery",
                "name": "Weapon Mastery",
                "summary": "Use mastery properties of two weapons; can change choices after a Long Rest.",
                "description": "Your training with weapons allows you to use the mastery properties of particular weapons. You gain the mastery properties of two weapons of your choice.",
                "details": {
                    "Action": "Passive",
                    "masteries": 2,
                    "recharge": "Long Rest",
                    "recharge_effect": "swap_weapon_mastery"
                }
            }
        ],
        2: [
            {
                "id": "paladin_fighting_style",
                "name": "Fighting Style",
                "summary": "Gain a Fighting Style feat or choose Blessed Warrior for two Cleric cantrips.",
                "description": "You adopt a particular style of combat as your specialty. You can choose one Fighting Style feat of your choice, or you can choose the *Blessed Warrior* option to gain clerical magic. \n\n*Blessed Warrior* grants you two cantrips from the Cleric spell list that count as Paladin spells for you and use Charisma as your spellcasting ability.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": [
                            {"name": "Fighting Style Feat", "type": "fighting_style_feat"},
                            {"name": "Blessed Warrior", "benefit": "2 Cleric cantrips (Charisma-based)"}
                        ]
                    }
                }
            },
            {
                "id": "paladin_smite",
                "name": "Paladin's Smite",
                "summary": "Divine Smite is always prepared; cast it once per Long Rest for free.",
                "description": "You can call upon divine energy to strike down your foes. You have the Divine Smite spell always prepared. \n\nIn addition, you can cast Divine Smite once without expending a spell slot. You regain the ability to do so when you finish a Long Rest.",
                "details": {
                    "Action": "Bonus Action",
                    "spells_granted": ["Divine Smite"],
                    "free_cast": "1/Long Rest",
                    "recharge": "Long Rest"
                }
            }
        ],
        3: [
            {
                "id": "paladin_channel_divinity",
                "name": "Channel Divinity",
                "summary": "Harness divine energy for effects like Divine Sense.",
                "description": "You can channel divine energy directly from your oath. You can use this energy to sense celestial, fiendish, or undead presences nearby.",
                "details": {
                    "Action": "Bonus Action",
                    "uses": {
                        "type": "level-based",
                        "scaling": {
                            "3-10": 2,
                            "11-20": 3
                        }
                    },
                    "recharge": "Short Rest (regain 1), Long Rest (regain all)",
                    "effects": [
                        {
                            "name": "Divine Sense",
                            "action": "Bonus Action",
                            "duration": "10 minutes",
                            "benefit": "Identify Celestial, Fiend, or Undead within 60ft."
                        }
                    ]
                }
            },
            {
                "id": "paladin_subclass",
                "name": "Paladin Subclass",
                "type": "subclass_choice",
                "summary": "Choose a Sacred Oath: Devotion, Glory, Ancients, or Vengeance.",
                "description": "You take a Sacred Oath that binds you as a Paladin. Your choice grants you features at 3rd level and again at 7th, 15th, and 20th levels.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": ["devotion", "glory", "ancients", "vengeance"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        5: [
            {
                "id": "paladin_extra_attack",
                "name": "Extra Attack",
                "summary": "Attack twice when taking the Attack action.",
                "description": "You can attack twice, instead of once, whenever you take the Attack action on your turn.",
                "details": {
                    "Action": "Passive",
                }
            },
            {
                "id": "paladin_faithful_steed",
                "name": "Faithful Steed",
                "summary": "Find Steed is always prepared; can cast it once per Long Rest without a spell slot.",
                "description": "You can summon a loyal celestial mount to aid you. You have the Find Steed spell always prepared, and you can cast it for free once per day.",
                "details": {
                    "Action": "Action",
                    "spells_granted": ["Find Steed"],
                    "free_cast": "1/Long Rest",
                    "recharge": "Long Rest"
                }
            }
        ],
        6: [
            {
                "id": "paladin_aura_of_protection",
                "name": "Aura Of Protection",
                "summary": "You and allies within 10ft gain a bonus to saving throws.",
                "description": "Your divine presence protects you and your companions. Whenever you or a creature of your choice within 10 feet of you must make a saving throw, the creature gains a bonus to the saving throw equal to your Charisma modifier (minimum bonus of +1). You must be conscious to grant this bonus.",
                "details": {
                    "Action": "Passive",
                    "range": "10 ft",
                    "bonus": "Charisma modifier (min +1)"
                }
            }
        ],
        7: [
            {
                "id": "paladin_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Paladin subclass.",
                "description": "You gain a new ability based on the Sacred Oath you took at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        9: [
            {
                "id": "paladin_abjure_foes",
                "name": "Abjure Foes",
                "summary": "Expend a Channel Divinity use to Frighten multiple creatures.",
                "description": "As a Magic action, you present your Holy Symbol and expend one use of your Channel Divinity to castigate your foes. Each creature of your choice that can see or hear you within 60 feet must make a Wisdom saving throw. \n\nOn a failed save, the creature is Frightened for 1 minute or until it takes any damage. While it is Frightened, its Speed is 0, and it can't benefit from any bonus to its speed. \n\nOn a successful save, the creature's speed is halved for 1 minute or until it takes any damage.",
                "details": {
                    "Action": "Action",
                    "cost": "1 Channel Divinity use",
                    "targets": "Charisma modifier (min 1)",
                    "range": "60 ft"
                }
            }
        ],
        10: [
            {
                "id": "paladin_aura_of_courage",
                "name": "Aura Of Courage",
                "summary": "You and allies in your aura have immunity to the Frightened condition.",
                "description": "Your inner courage radiates outward, preventing you and nearby allies from being frightened.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        11: [
            {
                "id": "paladin_radiant_strikes",
                "name": "Radiant Strikes",
                "summary": "Deal an extra 1d8 Radiant damage on all melee hits.",
                "description": "You are so infused with righteous might that all your melee strikes deal extra radiant damage. Whenever you hit a creature with a melee weapon or an Unarmed Strike, the target takes an extra 1d8 Radiant damage.",
                "details": {
                    "Action": "Passive",
                    "extra_damage": "1d8 Radiant",
                    "note": "Applies to all melee weapon attacks and unarmed strikes."
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        14: [
            {
                "id": "paladin_restoring_touch",
                "name": "Restoring Touch",
                "summary": "Lay On Hands can remove several conditions for 5 points each.",
                "description": "Your healing touch becomes even more powerful. When you use your Lay on Hands, you can expend 5 Hit Points from your pool to end one of the following conditions on the target: Blinded, Charmed, Deafened, Frightened, Paralyzed, or Stunned. You can end multiple conditions with a single use of Lay on Hands, expending 5 Hit Points for each condition ended.",
                "details": {
                    "Action": "Bonus Action",
                    "conditions": ["Blinded", "Charmed", "Deafened", "Frightened", "Paralyzed", "Stunned"],
                    "cost_per_condition": 5
                }
            }
        ],
        15: [
            {
                "id": "paladin_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Paladin subclass.",
                "description": "You gain a new ability based on the Sacred Oath you took at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        18: [
            {
                "id": "paladin_aura_expansion",
                "name": "Aura Expansion",
                "summary": "Your Aura of Protection range increases to 30ft.",
                "description": "The power of your divine aura grows, extending its reach to protect allies across a much larger area.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        20: [
            {
                "id": "paladin_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Paladin subclass.",
                "description": "You gain a final, powerful ability based on the Sacred Oath you took at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ]
    }
}

RANGER = {
    "id": "ranger",
    "name": "Ranger",
    "subclasses": RANGER_SUBCLASSES,
    "description": """Rangers are masters of the wilderness, combining martial skill with primal magic. 
        They excel at tracking and hunting dangerous foes, using their deep connection to nature to 
        navigate treacherous terrain and strike with deadly precision.""",
    "primary_ability": "Dexterity and Wisdom",
    "hit_die": "d10",
    "proficiencies": {
        "saving_throws": ["Strength", "Dexterity"],
        "armor": ["Light", "Medium", "Shields"],
        "weapons": ["Simple", "Martial"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 3,
            "options": ["Animal Handling", "Athletics", "Insight", "Investigation", "Nature", "Perception", "Stealth", "Survival"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Studded Leather Armor", "Scimitar", "Shortsword", "Longbow", "20 Arrows", "Quiver", "Druidic Focus (spring of mistletoe)", "Explorer's Pack"],
            "gold": 7
        },
        "option_b": {
            "gold": 150
        }
    },
    "spellcasting": {
        "ability": "Wisdom",
        "progression": "half",
        "preparation_mode": "prepared",
        "focus": ["Druidic Focus"],
        "recharge": "Long Rest",
        "spells_prepared": {
            1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 6, 7: 7, 8: 7, 9: 9, 10: 9,
            11: 10, 12: 10, 13: 11, 14: 11, 15: 12, 16: 12, 17: 14, 18: 14, 19: 15, 20: 15
        }
    },
    "features": {
        1: [
            {
                "id": "ranger_spellcasting",
                "name": "Spellcasting",
                "summary": "Cast Ranger spells using Wisdom and a Druidic Focus; swap one spell after a Long Rest.",
                "description": "You have learned to cast spells derived from the primal forces of nature. You use your Wisdom whenever a spell refers to your spellcasting ability.",
                "details": {
                    "Action": "Passive",
                    "spells_lvl_1": 2,
                    "recharge": "Long Rest"
                }
            },
            {
                "id": "ranger_favored_enemy",
                "name": "Favored Enemy",
                "summary": "Hunter's Mark is always prepared; cast it for free multiple times.",
                "description": "You are a master of hunting certain types of foes. You always have the *Hunter's Mark* spell prepared. \n\nYou can cast *Hunter's Mark* a number of times equal to your Proficiency Bonus without expending a spell slot. You regain all expended uses when you finish a Long Rest.",
                "details": {
                    "Action": "Bonus Action",
                    "spells_granted": ["Hunter's Mark"],
                    "free_casts": "Proficiency Bonus",
                    "recharge": "Long Rest"
                }
            },
            {
                "id": "ranger_weapon_mastery",
                "name": "Weapon Mastery",
                "summary": "Use mastery properties of two weapons; can change choices after a Long Rest.",
                "description": "Your training with weapons allows you to use the mastery properties of particular weapons. You gain the mastery properties of two weapons of your choice.",
                "details": {
                    "Action": "Passive",
                    "masteries": 2,
                    "recharge": "Long Rest",
                    "recharge_effect": "swap_weapon_mastery"
                }
            }
        ],
        2: [
            {
                "id": "ranger_deft_explorer",
                "name": "Deft Explorer",
                "summary": "Gain Expertise in one skill and learn two languages.",
                "description": "Your experience in the wild has made you exceptionally skilled and knowledgeable. You gain Expertise in a skill and learn new languages.",
                "details": {
                    "Action": "Passive",
                    "expertise_choice": 1,
                    "languages": 2
                }
            },
            {
                "id": "ranger_fighting_style",
                "name": "Fighting Style",
                "summary": "Gain a Fighting Style feat or choose Druidic Warrior for two Druid cantrips.",
                "description": "You adopt a particular style of combat as your specialty. You can choose one Fighting Style feat of your choice, or you can choose the *Druidic Warrior* option to gain druidic magic. \n\n*Druidic Warrior* grants you two cantrips from the Druid spell list that count as Ranger spells for you and use Wisdom as your spellcasting ability.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": [
                            {"name": "Fighting Style Feat", "type": "fighting_style_feat"},
                            {"name": "Druidic Warrior", "benefit": "2 Druid cantrips (Wisdom-based)"}
                        ]
                    }
                }
            }
        ],
        3: [
            {
                "id": "ranger_subclass",
                "name": "Ranger Subclass",
                "type": "subclass_choice",
                "summary": "Choose a Ranger Archetype: Beast Master, Fey Wanderer, Gloom Stalker, or Hunter.",
                "description": "You choose a Ranger Archetype that defines your specialization. Your choice grants you features at 3rd level and again at 7th, 11th, and 15th levels.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": ["beast_master", "fey_wanderer", "gloom_stalker", "hunter"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        5: [
            {
                "id": "ranger_extra_attack",
                "name": "Extra Attack",
                "summary": "Attack twice when taking the Attack action.",
                "description": "You can attack twice, instead of once, whenever you take the Attack action on your turn.",
                "details": {
                    "Action": "Passive"
                }
            }
        ],
        6: [
            {
                "id": "ranger_roving",
                "name": "Roving",
                "summary": "Speed increases by 10ft; gain Climb and Swim speeds.",
                "description": "Your movement becomes swifter and more versatile. While you are not wearing Heavy Armor, your Speed increases by 10 feet. You also gain a Climbing Speed and a Swimming Speed equal to your Speed.",
                "details": {
                    "Action": "Passive",
                    "speed_bonus": "+10 ft",
                    "modes": ["Climb", "Swim"],
                    "restriction": "No Heavy Armor"
                }
            }
        ],
        7: [
            {
                "id": "ranger_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Ranger subclass.",
                "description": "You gain a new ability based on the Ranger Archetype you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        9: [
            {
                "id": "ranger_expertise",
                "name": "Expertise",
                "summary": "Gain Expertise in two more skill proficiencies.",
                "description": "Your mastery of your skills continues to grow. You choose two more of your skill proficiencies to gain Expertise in.",
                "details": {
                    "Action": "Passive",
                    "expertise_choice": 2
                }
            }
        ],
        10: [
            {
                "id": "ranger_tireless",
                "name": "Tireless",
                "summary": "Give yourself Temporary HP and decrease Exhaustion level on a Short Rest.",
                "description": "As a Magic action, you can give yourself a number of Temporary Hit Points equal to 1d8 plus your Wisdom modifier (minimum of 1). You can use this action a number of times equal to your Wisdom modifier (minimum of once), and you regain all expended uses when you finish a Long Rest. Whenever you finish a Short Rest, your Exhaustion level, if any, decreases by 1.",
                "details": {
                    "Action": "Action",
                    "temp_hp": "1d8 + Wisdom modifier",
                    "temp_hp_uses": "Wisdom modifier (min 1)",
                    "exhaustion_recovery": "Short Rest decreases level by 1",
                    "recharge": "Long Rest"
                }
            }
        ],
        11: [
            {
                "id": "ranger_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Ranger subclass.",
                "description": "You gain a new ability based on the Ranger Archetype you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        13: [
            {
                "id": "ranger_relentless_hunter",
                "name": "Relentless Hunter",
                "summary": "Damage cannot break your Concentration on Hunter's Mark.",
                "description": "Your focus on your prey is absolute. Taking damage can no longer break your concentration on your Hunter's Mark spell.",
                "details": {
                    "Action": "Passive"
                }
            }
        ],
        14: [
            {
                "id": "ranger_natures_veil",
                "name": "Nature's Veil",
                "summary": "Use a Bonus Action to become Invisible until the end of your next turn.",
                "description": "You can draw on the powers of nature to hide yourself from view. You can become invisible for a short time to gain a tactical advantage.",
                "details": {
                    "Action": "Bonus Action",
                    "uses": "Wisdom modifier (min 1)",
                    "recharge": "Long Rest"
                }
            }
        ],
        15: [
            {
                "id": "ranger_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Ranger subclass.",
                "description": "You gain a final, powerful ability based on the Ranger Archetype you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        17: [
            {
                "id": "ranger_precise_hunter",
                "name": "Precise Hunter",
                "summary": "Advantage on attack rolls against the creature marked by your Hunter's Mark.",
                "description": "Your precision against your marked prey is unmatched, giving you Advantage on all attack rolls against them.",
                "details": {
                    "Action": "Passive"
                }
            }
        ],
        18: [
            {
                "id": "ranger_feral_senses",
                "name": "Feral Senses",
                "summary": "Gain Blindsight with a range of 30ft.",
                "description": "Your senses are so sharp that you no longer need sight to detect nearby enemies. You gain Blindsight, allowing you to sense anything within 30 feet.",
                "details": {
                    "Action": "Passive",
                    "range": "30 ft"
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        20: [
            {
                "id": "ranger_foe_slayer",
                "name": "Foe Slayer",
                "summary": "Hunter's Mark damage die increases to d10.",
                "description": "You have become the ultimate hunter. Your strikes against your marked prey are even more deadly. The damage die of your *Hunter's Mark* spell increases to a d10.",
                "details": {
                    "Action": "Passive"
                }
            }
        ]
    }
}

ROGUE = {
    "id": "rogue",
    "name": "Rogue",
    "subclasses": ROGUE_SUBCLASSES,
    "description": """Rogues are masters of stealth, skill, and precision. They excel at exploiting 
        their enemies' weaknesses, striking with deadly accuracy when their foes are distracted, 
        and using a vast array of tools and talents to overcome any obstacle.""",
    "primary_ability": "Dexterity",
    "hit_die": "d8",
    "proficiencies": {
        "saving_throws": ["Dexterity", "Intelligence"],
        "armor": ["Light"],
        "weapons": ["Simple", "Martial (with Finesse or Light properties)"],
        "tools": {
            "granted": ["Thieves' Tools"],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 4,
            "options": ["Acrobatics", "Athletics", "Deception", "Insight", "Intimidation", "Investigation", "Perception", "Persuasion", "Sleight of Hand", "Stealth"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Leather Armor", "2 Daggers", "Shortsword", "Shortbow", "20 Arrows", "Quiver", "Thieves' Tools", "Burglar's Pack"],
            "gold": 8
        },
        "option_b": {
            "gold": 100
        }
    },
    "features": {
        1: [
            {
                "id": "rogue_expertise_1",
                "name": "Expertise",
                "summary": "Gain Expertise in two of your skill proficiencies.",
                "description": "You gain a mastery over your chosen skills that few can match. You choose two of your skill proficiencies to gain Expertise in.",
                "details": {
                    "Action": "Passive",
                    "expertise_choice": 2
                }
            },
            {
                "id": "rogue_sneak_attack",
                "name": "Sneak Attack",
                "summary": "Deal extra damage once per turn under specific conditions.",
                "description": "You know how to strike where it hurts most. Once per turn, you can deal extra damage to a creature you hit with an attack if you have Advantage on the attack roll and the attack uses a Finesse weapon or a Ranged weapon. \n\nYou don't need Advantage on the attack roll if another enemy of the target is within 5 feet of it, that enemy isn't Incapacitated, and you don't have Disadvantage on the attack roll. \n\nThe extra damage is a number of d6s that increases as you level up in this class.",
                "details": {
                    "Action": "Passive",
                    "die": {
                        "type": "level-based",
                        "formula": "(level + 1) // 2",
                        "scaling": {
                            "1-2": "1d6", "3-4": "2d6", "5-6": "3d6", "7-8": "4d6", "9-10": "5d6",
                            "11-12": "6d6", "13-14": "7d6", "15-16": "8d6", "17-18": "9d6", "19-20": "10d6"
                        }
                    },
                    "restriction": "Finesse or Ranged weapon"
                }
            },
            {
                "id": "rogue_thieves_cant",
                "name": "Thieves' Cant",
                "summary": "You know Thieves' Cant and one other language of your choice.",
                "description": "You have learned the secret language of the criminal underworld, allowing you to hide messages in seemingly normal conversation.",
                "details": {
                    "Action": "Passive",
                    "languages": ["Thieves' Cant", "Choice of 1"]
                }
            },
            {
                "id": "rogue_weapon_mastery",
                "name": "Weapon Mastery",
                "summary": "Use mastery properties of two weapons; can change choices after a Long Rest.",
                "description": "Your training with weapons allows you to use the mastery properties of particular weapons. You gain the mastery properties of two weapons of your choice.",
                "details": {
                    "Action": "Passive",
                    "masteries": 2,
                    "recharge": "Long Rest",
                    "recharge_effect": "swap_weapon_mastery"
                }
            }
        ],
        2: [
            {
                "id": "rogue_cunning_action",
                "name": "Cunning Action",
                "summary": "On your turn, you can take a Bonus Action to Dash, Disengage, or Hide.",
                "description": "Your quick thinking and agility allow you to move and act quickly. You can take a Bonus Action on each of your turns in combat to Dash, Disengage, or Hide.",
                "details": {
                    "Action": "Bonus Action",
                }
            }
        ],
        3: [
            {
                "id": "rogue_subclass",
                "name": "Rogue Subclass",
                "type": "subclass_choice",
                "summary": "Choose a Rogue Archetype: Arcane Trickster, Assassin, Soulknife, or Thief.",
                "description": "You choose a Rogue Archetype that defines your methodology. Your choice grants you features at 3rd level and again at 9th, 13th, and 17th levels.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": ["arcane_trickster", "assassin", "soulknife", "thief"]
                    }
                }
            },
            {
                "id": "rogue_steady_aim",
                "name": "Steady Aim",
                "summary": "Bonus Action to gain Advantage on next attack; reduces speed to 0.",
                "description": "By holding perfectly still, you can strike with incredible precision. You can use a Bonus Action to gain Advantage on your next attack roll.",
                "details": {
                    "Action": "Bonus Action",
                    "restriction": "Cannot have moved, reduces speed to 0 for turn"
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        5: [
            {
                "id": "rogue_cunning_strike",
                "name": "Cunning Strike",
                "summary": "Forgo Sneak Attack damage dice to apply tactical effects.",
                "description": "You have learned to sacrifice raw damage for tactical advantage. When you deal Sneak Attack damage, you can add one of the following Cunning Strike effects by forgoing 1d6 of your Sneak Attack damage:\n\n- **Poison**: The target must succeed on a Constitution saving throw or be Poisoned for 1 minute.\n- **Trip**: The target must succeed on a Dexterity saving throw or be knocked Prone (Large or smaller targets only).\n- **Withdraw**: You immediately move up to half your Speed without provoking Opportunity Attacks.",
                "details": {
                    "Action": "Passive",
                    "effects": [
                        {"name": "Poison", "cost": "1d6", "save": "Constitution", "fail": "Poisoned (1 min)"},
                        {"name": "Trip", "cost": "1d6", "save": "Dexterity", "fail": "Prone (Large or smaller)"},
                        {"name": "Withdraw", "cost": "1d6", "benefit": "Move half speed without Opportunity Attacks"}
                    ],
                    "save_dc": "8 + Proficiency Bonus + Dexterity modifier"
                }
            },
            {
                "id": "rogue_uncanny_dodge",
                "name": "Uncanny Dodge",
                "summary": "Use a Reaction to halve damage from an attack you can see.",
                "description": "When an attacker that you can see hits you with an attack, you can use your reaction to halve the attack's damage against you.",
                "details": {
                    "Action": "Reaction",
                }
            }
        ],
        6: [
            {
                "id": "rogue_expertise_6",
                "name": "Expertise",
                "summary": "Gain Expertise in two more skill proficiencies.",
                "description": "Your mastery of your skills continues to grow. You choose two more of your skill proficiencies to gain Expertise in.",
                "details": {
                    "Action": "Passive",
                    "expertise_choice": 2
                }
            }
        ],
        7: [
            {
                "id": "rogue_evasion",
                "name": "Evasion",
                "summary": "Take half damage on failed Dex saves and no damage on successes.",
                "description": "Your instinctive agility lets you dodge out of the way of certain area effects. When you succeed on a Dexterity save for half damage, you instead take no damage.",
                "details": {
                    "Action": "Passive",
                }
            },
            {
                "id": "rogue_reliable_talent",
                "name": "Reliable Talent",
                "summary": "Treat any d20 roll of 9 or lower as a 10 for skill and tool checks you are proficient in.",
                "description": "You have refined your chosen skills until they approach perfection. Whenever you make an ability check that lets you add your proficiency bonus, you can treat a d20 roll of 9 or lower as a 10.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        9: [
            {
                "id": "rogue_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Rogue subclass.",
                "description": "You gain a new ability based on the Rogue Archetype you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        10: [
            {
                "id": "feat_or_asi_10",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores (Unique extra feat for Rogues).",
                "description": "As a Rogue, you gain an extra opportunity to specialize your talents. You can increase your ability scores or choose a new Feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        11: [
            {
                "id": "rogue_improved_cunning_strike",
                "name": "Improved Cunning Strike",
                "summary": "Use up to two Cunning Strike effects simultaneously, paying the total cost.",
                "description": "Your tactical expertise allows you to apply even more pressure. You can now use two of your Cunning Strike effects on a single attack.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        13: [
            {
                "id": "rogue_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Rogue subclass.",
                "description": "You gain a new ability based on the Rogue Archetype you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        14: [
            {
                "id": "rogue_devious_strikes",
                "name": "Devious Strikes",
                "summary": "Unlock more powerful Cunning Strike options.",
                "description": "You have mastered even more debilitating tactical strikes. You gain the following options for your Cunning Strike:\n\n- **Daze (Cost 2d6)**: The target must succeed on a Constitution saving throw or be Dazed until the end of its next turn. A Dazed creature can move or take one action/bonus action, but not both.\n- **Knock Out (Cost 6d6)**: The target must succeed on a Constitution saving throw or be Unconscious for 1 minute or until it takes damage.\n- **Obscure (Cost 3d6)**: The target must succeed on a Dexterity saving throw or be Blinded until the end of its next turn.",
                "details": {
                    "Action": "Passive",
                    "additional_effects": [
                        {"name": "Daze", "cost": "2d6", "save": "Constitution", "fail": "Limited to move, Action, or Bonus Action"},
                        {"name": "Knock Out", "cost": "6d6", "save": "Constitution", "fail": "Unconscious (1 min or damage)"},
                        {"name": "Obscure", "cost": "3d6", "save": "Dexterity", "fail": "Blinded until end of next turn"}
                    ]
                }
            }
        ],
        15: [
            {
                "id": "rogue_slippery_mind",
                "name": "Slippery Mind",
                "summary": "Gain proficiency in Wisdom and Charisma saving throws.",
                "description": "Your mind is difficult to influence. You gain proficiency in Wisdom and Charisma saving throws.",
                "details": {
                    "Action": "Passive",
                    "saving_throws_granted": ["Wisdom", "Charisma"]
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        17: [
            {
                "id": "rogue_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Rogue subclass.",
                "description": "You gain a final, powerful ability based on the Rogue Archetype you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        18: [
            {
                "id": "rogue_elusive",
                "name": "Elusive",
                "summary": "Attack rolls cannot have Advantage against you unless you are Incapacitated.",
                "description": "You are so evasive that attackers rarely gain the upper hand against you. No attack roll has Advantage against you while you aren't Incapacitated.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        20: [
            {
                "id": "rogue_stroke_of_luck",
                "name": "Stroke Of Luck",
                "summary": "Turn a failed d20 test into a 20.",
                "description": "You have an uncanny knack for succeeding when you need it most. If you fail a D20 test, you can turn the roll into a 20 instead.",
                "details": {
                    "Action": "Passive",
                    "recharge": "Short or Long Rest"
                }
            }
        ]
    }
}

SORCERER = {
    "id": "sorcerer",
    "name": "Sorcerer",
    "subclasses": SORCERER_SUBCLASSES,
    "description": """Sorcerers carry a magical birthright conferred upon them by an exotic bloodline, 
        some otherworldly influence, or exposure to unknown cosmic forces. Their magic is not 
        studied but innate, flowing from a wellspring of power within.""",
    "primary_ability": "Charisma",
    "hit_die": "d6",
    "proficiencies": {
        "saving_throws": ["Constitution", "Charisma"],
        "armor": [],
        "weapons": ["Simple"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Arcana", "Deception", "Insight", "Intimidation", "Persuasion", "Religion"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Spear", "2 Daggers", "Arcane Focus (crystal)", "Dungeoneer's Pack"],
            "gold": 28
        },
        "option_b": {
            "gold": 50
        }
    },
    "spellcasting": {
        "ability": "Charisma",
        "progression": "full",
        "preparation_mode": "learned",
        "focus": ["Arcane Focus"],
        "recharge": "Long Rest",
        "cantrips_known": {1: 4, 4: 5, 10: 6},
        "spells_prepared": {
            1: 2, 2: 4, 3: 6, 4: 7, 5: 9, 6: 10, 7: 11, 8: 12, 9: 14, 10: 15,
            11: 16, 12: 16, 13: 17, 14: 17, 15: 18, 16: 18, 17: 19, 18: 20, 19: 21, 20: 22
        }
    },
    "features": {
        1: [
            {
                "id": "sorcerer_spellcasting",
                "name": "Spellcasting",
                "summary": "Cast Sorcerer spells using Charisma and an Arcane Focus; can swap one spell on level up.",
                "description": "An event in your past, or in the life of a precursor, left an indelible mark on you, infusing you with arcane magic. This magic is yours to command through your force of personality.",
                "details": {
                    "Action": "Passive",
                    "recharge": "Long Rest"
                }
            },
            {
                "id": "sorcerer_innate_sorcery",
                "name": "Innate Sorcery",
                "summary": "Unleash magic for 1 minute, increasing Spell DC and gaining Advantage.",
                "description": "You can touch the source of magic within you to temporarily enhance your spellcasting. As a Bonus Action, you can unleash a surge of innate magic that lasts for 1 minute or until you are Incapacitated or you die. \n\nWhile this surge is active, you gain the following benefits: \n\n- **Increased Potency**: Your Spell Save DC for Sorcerer spells increases by 1. \n- **Arcane Precision**: You have Advantage on the attack rolls of your Sorcerer spells.",
                "details": {
                    "Action": "Bonus Action",
                    "duration": "1 minute",
                    "uses": 2,
                    "recharge": "Long Rest",
                    "benefits": ["+1 to Spell Save DC", "Advantage on Sorcerer spell attack rolls"]
                }
            }
        ],
        2: [
            {
                "id": "sorcerer_font_of_magic",
                "name": "Font Of Magic",
                "summary": "Harness Sorcery Points to create spell slots or fuel Metamagic.",
                "description": "You tap into a deep wellspring of magic within yourself. This wellspring is represented by Sorcery Points, which you can use to create spell slots or empower your spells. \n\n**Converting Sorcery Points to Spell Slots**: You can expend Sorcery Points to create extra spell slots as a Bonus Action. \n\n**Converting Spell Slots to Sorcery Points**: As a Bonus Action, you can expend a spell slot to regain a number of Sorcery Points equal to the level of the slot expended.",
                "details": {
                    "Action": "Bonus Action",
                    "points": {
                        "type": "level-based",
                        "scaling": {
                            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                            "11": 11, "12": 12, "13": 13, "14": 14, "15": 15, "16": 16, "17": 17, "18": 18, "19": 19, "20": 20
                        }
                    },
                    "recharge": "Long Rest",
                    "flexible_casting": {
                        "slot_creation_costs": {
                            "1": 2, "2": 3, "3": 5, "4": 6, "5": 7
                        }
                    }
                }
            },
            {
                "id": "sorcerer_metamagic",
                "name": "Metamagic",
                "summary": "Alter your spells using Sorcery Points.",
                "description": "You gain the ability to twist your spells to suit your needs. You can use Sorcery Points to apply special effects like extending a spell's range or doubling its duration.",
                "details": {
                    "Action": "Passive",
                    "options_known": {
                        "type": "level-based",
                        "scaling": {
                            "2-9": 2,
                            "10-16": 4,
                            "17-20": 6
                        }
                    },
                    "options": SORCERER_METAMAGIC
                }
            }
        ],
        3: [
            {
                "id": "sorcerer_subclass",
                "name": "Sorcerer Subclass",
                "type": "subclass_choice",
                "summary": "Choose a Sorcerous Origin: Aberrant, Clockwork, Draconic, or Wild Magic.",
                "description": "You choose a Sorcerous Origin that defines the source of your magic. Your choice grants you features at 3rd level and again at 6th, 14th, and 18th levels.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": ["aberrant_sorcery", "clockwork_sorcery", "draconic_sorcery", "wild_magic_sorcery"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        5: [
            {
                "id": "sorcerer_sorcerous_restoration",
                "name": "Sorcerous Restoration",
                "summary": "Regain Sorcery Points on a Short Rest.",
                "description": "You have learned to recover your sorcerous energy through short periods of rest. Once per Long Rest, you can regain half your Sorcerer level (rounded up) in Sorcery Points when you finish a Short Rest.",
                "details": {
                    "Action": "Passive",
                    "uses": 1,
                    "trigger": "Short Rest",
                    "amount": "Level / 2 (round up)",
                    "recharge": "Long Rest"
                }
            }
        ],
        6: [
            {
                "id": "sorcerer_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Sorcerer subclass.",
                "description": "You gain a new ability based on the Sorcerous Origin you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        7: [
            {
                "id": "sorcerer_sorcery_incarnate",
                "name": "Sorcery Incarnate",
                "summary": "Spend 2 Sorcery Points to activate Innate Sorcery; use up to two Metamagics per spell while active.",
                "description": "You can manifest your sorcerous power in its purest form. You can expend Sorcery Points to activate your Innate Sorcery, and while it's active, you can apply multiple Metamagic effects to a single spell.",
                "details": {
                    "Action": "Passive",
                    "cost_to_activate": "2 Sorcery Points",
                    "benefit": "Dual Metamagic use while Innate Sorcery is active"
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        14: [
            {
                "id": "sorcerer_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Sorcerer subclass.",
                "description": "You gain a new ability based on the Sorcerous Origin you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        18: [
            {
                "id": "sorcerer_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Sorcerer subclass.",
                "description": "You gain a final, powerful ability based on the Sorcerous Origin you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        20: [
            {
                "id": "sorcerer_arcane_apotheosis",
                "name": "Arcane Apotheosis",
                "summary": "While Innate Sorcery is active, use one Metamagic per turn for free.",
                "description": "You have achieved a perfect harmony with the arcane. While your Innate Sorcery is active, you can use one Metamagic effect on your spells for free each turn. \n\nIn addition, if you use your Metamagic on a spell while your Innate Sorcery is active, you can use any of your Metamagic options, even if you don't know them.",
                "details": {
                    "Action": "Passive",
                    "benefit": "Free Metamagic once per turn during Innate Sorcery"
                }
            }
        ]
    }
}

WARLOCK = {
    "id": "warlock",
    "name": "Warlock",
    "subclasses": WARLOCK_SUBCLASSES,
    "description": """Warlocks are seekers of knowledge that lie hidden in the fabric of the multiverse. 
        Through pacts made with mysterious beings of great power, warlocks unlock magical effects, 
        both subtle and spectacular.""",
    "primary_ability": "Charisma",
    "hit_die": "d8",
    "proficiencies": {
        "saving_throws": ["Wisdom", "Charisma"],
        "armor": ["Light"],
        "weapons": ["Simple"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Arcana", "Deception", "History", "Intimidation", "Investigation", "Nature", "Religion"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["Leather Armor", "Sickle", "2 Daggers", "Arcane Focus (orb)", "Book (occult lore)", "Scholar's Pack"],
            "gold": 15
        },
        "option_b": {
            "gold": 100
        }
    },
    "spellcasting": {
        "ability": "Charisma",
        "progression": "pact",
        "preparation_mode": "learned",
        "focus": ["Arcane Focus"],
        "recharge": "Short or Long Rest",
        "cantrips_known": {1: 2, 4: 3, 10: 4},
        "spells_prepared": {
            1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 10,
            11: 11, 12: 11, 13: 12, 14: 12, 15: 13, 16: 13, 17: 14, 18: 14, 19: 15, 20: 15
        }
    },
    "features": {
        1: [
            {
                "id": "warlock_eldritch_invocations",
                "name": "Eldritch Invocations",
                "summary": "Gain fragments of forbidden knowledge that grant you magical abilities.",
                "description": "In your study of occult lore, you have unearthed Eldritch Invocations, fragments of forbidden knowledge that imbue you with an abiding magical ability. \n\nAt 1st level, you gain one invocation of your choice. As you gain levels in this class, you learn additional invocations. Whenever you gain a level in this class, you can study your occult lore and replace one invocation you know with another one that you could learn at that level.",
                "details": {
                    "Action": "Passive",
                    "invocations_known": {
                        "type": "level-based",
                        "scaling": {
                            "1": 1, "2": 3, "5": 5, "7": 6, "9": 7, "12": 8, "15": 9, "18": 10
                        }
                    },
                    "options": WARLOCK_ELDRITCH_INVOCATIONS
                }
            },
            {
                "id": "warlock_pact_magic",
                "name": "Pact Magic",
                "summary": "Cast Warlock spells using Charisma and an Arcane Focus; slots recharge on a Short Rest.",
                "description": "Your arcane research and the magic bestowed on you by your patron have given you facility with spells.",
                "details": {
                    "Action": "Passive",
                    "recharge": "Short or Long Rest"
                }
            }
        ],
        2: [
            {
                "id": "warlock_magical_cunning",
                "name": "Magical Cunning",
                "summary": "Expend 1 minute to regain half your Pact Magic spell slots.",
                "description": "You can perform an occult ritual to regain some of your expended Pact Magic spell slots. By spending 1 minute in ritualistic prayer or meditation, you regain a number of Pact Magic spell slots equal to half your total number of Pact Magic spell slots (rounded up). \n\nYou regain the ability to do so when you finish a Long Rest.",
                "details": {
                    "Action": "Passive",
                    "uses": 1,
                    "recharge": "Long Rest",
                    "benefit": "Regain half Pact Magic slots (round up)"
                }
            }
        ],
        3: [
            {
                "id": "warlock_subclass",
                "name": "Warlock Subclass",
                "type": "subclass_choice",
                "summary": "Choose a Otherworldly Patron: Archfey, Celestial, Fiend, or Great Old One.",
                "description": "You choose an Otherworldly Patron who defines the source of your pact. Your choice grants you features at 3rd level and again at 6th, 10th, and 14th levels.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": ["archfey_patron", "celestial_patron", "fiend_patron", "great_old_one_patron"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        6: [
            {
                "id": "warlock_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Warlock subclass.",
                "description": "You gain a new ability based on the Otherworldly Patron you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        9: [
            {
                "id": "warlock_contact_patron",
                "name": "Contact Patron",
                "summary": "Contact Other Plane is always prepared; cast it once for free with auto-success to contact your patron.",
                "description": "You can communicate directly with your patron to seek guidance. You have the Contact Other Plane spell always prepared, and you can cast it for free with automatic success once per day.",
                "details": {
                    "Action": "Passive",
                    "uses": 1,
                    "spells_granted": ["Contact Other Plane"],
                    "free_cast_benefit": "Auto-success on saving throw",
                    "recharge": "Long Rest"
                }
            }
        ],
        10: [
            {
                "id": "warlock_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Warlock subclass.",
                "description": "You gain a new ability based on the Otherworldly Patron you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        11: [
            {
                "id": "warlock_mystic_arcanum_6",
                "name": "Mystic Arcanum (Level 6)",
                "summary": "Choose a level 6 Warlock spell to cast once per Long Rest without a spell slot.",
                "description": "Your patron bestows upon you a magical secret called an arcanum. You can choose one 6th-level spell from the warlock spell list to cast once without expending a spell slot.",
                "details": {
                    "Action": "Passive",
                    "uses": 1,
                    "arcanum_level": 6,
                    "recharge": "Long Rest"
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        13: [
            {
                "id": "warlock_mystic_arcanum_7",
                "name": "Mystic Arcanum (Level 7)",
                "summary": "Choose a level 7 Warlock spell to cast once per Long Rest without a spell slot.",
                "description": "Your patron bestows upon you another arcanum. You can choose one 7th-level spell from the warlock spell list to cast once without expending a spell slot.",
                "details": {
                    "Action": "Passive",
                    "uses": 1,
                    "arcanum_level": 7,
                    "recharge": "Long Rest"
                }
            }
        ],
        14: [
            {
                "id": "warlock_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Warlock subclass.",
                "description": "You gain a final, powerful ability based on the Otherworldly Patron you chose at 3rd level.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        15: [
            {
                "id": "warlock_mystic_arcanum_8",
                "name": "Mystic Arcanum (Level 8)",
                "summary": "Choose a level 8 Warlock spell to cast once per Long Rest without a spell slot.",
                "description": "Your patron bestows upon you another arcanum. You can choose one 8th-level spell from the warlock spell list to cast once without expending a spell slot.",
                "details": {
                    "Action": "Passive",
                    "uses": 1,
                    "arcanum_level": 8,
                    "recharge": "Long Rest"
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        17: [
            {
                "id": "warlock_mystic_arcanum_9",
                "name": "Mystic Arcanum (Level 9)",
                "summary": "Choose a level 9 Warlock spell to cast once per Long Rest without a spell slot.",
                "description": "Your patron bestows upon you a final arcanum. You can choose one 9th-level spell from the warlock spell list to cast once without expending a spell slot.",
                "details": {
                    "Action": "Passive",
                    "uses": 1,
                    "arcanum_level": 9,
                    "recharge": "Long Rest"
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat.",
                "details": {
                    "Action": "Passive",
                }
            }
        ],
        20: [
            {
                "id": "warlock_eldritch_master",
                "name": "Eldritch Master",
                "summary": "Magical Cunning now regains all expended Pact Magic spell slots.",
                "description": "You have achieved total mastery of your eldritch power. Your Magical Cunning feature now regains all of your Pact Magic spell slots instead of only half.",
                "details": {
                    "Action": "Passive",
                }
            }
        ]
    }
}

WIZARD = {
    "id": "wizard",
    "name": "Wizard",
    "subclasses": WIZARD_SUBCLASSES,
    "description": """Wizards are supreme magic-users, defined and united as a class by the spells they cast. 
        Drawing on the subtle weave of magic that permeates the cosmos, wizards cast spells of explosive fire, 
        arcing lightning, subtle deception, and brute-force mind control.""",
    "primary_ability": "Intelligence",
    "hit_die": "d6",
    "proficiencies": {
        "saving_throws": ["Intelligence", "Wisdom"],
        "armor": [],
        "weapons": ["Simple"],
        "tools": {
            "granted": [],
            "choose": 0,
            "options": []
        },
        "skills": {
            "granted": [],
            "choose": 2,
            "options": ["Arcana", "History", "Insight", "Investigation", "Medicine", "Nature", "Religion"]
        }
    },
    "starting_equipment": {
        "option_a": {
            "items": ["2 Daggers", "Arcane Focus (Quarterstaff)", "Robe", "Spellbook", "Scholar's Pack"],
            "gold": 5
        },
        "option_b": {
            "gold": 55
        }
    },
    "spellcasting": {
        "ability": "Intelligence",
        "progression": "full",
        "preparation_mode": "prepared",
        "focus": ["Arcane Focus", "Spellbook"],
        "recharge": "Long Rest",
        "cantrips_known": {1: 3, 4: 4, 10: 5},
        "spells_prepared": {
            1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9, 7: 10, 8: 11, 9: 12, 10: 13,
            11: 16, 12: 16, 13: 17, 14: 18, 15: 19, 16: 20, 17: 21, 18: 22, 19: 23, 20: 25
        },
        "spellbook": {
            "initial_spells": 6,
            "spells_per_level": 2,
            "weight": "3 lbs",
            "pages": 100
        }
    },
    "features": {
        1: [
            {
                "id": "wizard_spellcasting",
                "name": "Spellcasting",
                "summary": "Cast Wizard spells using Intelligence and a Spellbook; can swap one spell on level up.",
                "description": "As a student of arcane magic, you have a spellbook containing spells that show the first glimmerings of your true power.",
                "details": {
                    "Action": "Passive",
                    "recharge": "Long Rest"
                }
            },
            {
                "id": "wizard_ritual_adept",
                "name": "Ritual Adept",
                "summary": "Cast any Wizard spell in your spellbook as a ritual.",
                "description": "You can cast any wizard spell in your spellbook as a ritual if that spell has the Ritual tag. You don't need to have the spell prepared to cast it in this way, but it must be in your spellbook.",
                "details": {
                    "Action": "Passive",
                    "effect": "Cast ritual spells from spellbook without preparation"
                }
            },
            {
                "id": "wizard_arcane_recovery",
                "name": "Arcane Recovery",
                "summary": "Regain spell slots on a Short Rest equal to half your level.",
                "description": "You have learned to regain some of your magical energy by studying your spellbook. Once per day when you finish a Short Rest, you can choose expended spell slots to recover. \n\nThe combined level of the spell slots you recover can be no more than half your wizard level (rounded up), and none of the slots can be of 6th level or higher. For example, if you're a 4th-level wizard, you can recover up to two levels worth of spell slots.",
                "details": {
                    "Action": "Passive",
                    "uses": 1,
                    "recharge": "Long Rest",
                    "trigger": "Short Rest",
                    "max_slot_level": 5,
                    "recovery_amount": "Wizard Level / 2 (round up)"
                }
            }
        ],
        2: [
            {
                "id": "wizard_scholar",
                "name": "Scholar",
                "summary": "Gain Expertise in one proficient academic skill.",
                "description": "Your academic studies have made you an expert in a particular field of knowledge. You choose one of your skill proficiencies from the following list to gain Expertise in: Arcana, History, Investigation, Medicine, Nature, or Religion.",
                "details": {
                    "Action": "Passive",
                    "expertise_choice_options": ["Arcana", "History", "Investigation", "Medicine", "Nature", "Religion"]
                }
            }
        ],
        3: [
            {
                "id": "wizard_subclass",
                "name": "Wizard Subclass",
                "type": "subclass_choice",
                "summary": "Choose an Arcane Tradition: Abjurer, Diviner, Evoker, or Illusionist.",
                "description": "You choose an Arcane Tradition that defines your specialization. Your choice grants you features at 3rd level and again at 6th, 10th, and 14th levels.",
                "details": {
                    "Action": "Passive",
                    "choice": {
                        "choose": 1,
                        "options": ["abjurer", "diviner", "evoker", "illusionist"]
                    }
                }
            }
        ],
        4: [
            {
                "id": "feat_or_asi_4",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive"
                }
            }
        ],
        5: [
            {
                "id": "wizard_memorize_spell",
                "name": "Memorize Spell",
                "summary": "After a Short Rest, swap one prepared spell for another in your spellbook.",
                "description": "You can quickly study your spellbook to change one of your prepared spells. Whenever you finish a Short Rest, you can choose one of the Wizard spells you have prepared and replace it with another spell of the same level from your spellbook.",
                "details": {
                    "Action": "Passive",
                    "uses": 1,
                    "trigger": "Short Rest",
                    "recharge": "Short Rest",
                    "effect": "Swap one prepared spell after a Short Rest"
                }
            }
        ],
        6: [
            {
                "id": "wizard_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Wizard subclass.",
                "description": "You gain a new ability based on the Arcane Tradition you chose at 3rd level.",
                "details": {
                    "Action": "Passive"
                }
            }
        ],
        8: [
            {
                "id": "feat_or_asi_8",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive"
                }
            }
        ],
        10: [
            {
                "id": "wizard_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Wizard subclass.",
                "description": "You gain a new ability based on the Arcane Tradition you chose at 3rd level.",
                "details": {
                    "Action": "Passive"
                }
            }
        ],
        12: [
            {
                "id": "feat_or_asi_12",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive"
                }
            }
        ],
        14: [
            {
                "id": "wizard_subclass_feature",
                "name": "Subclass Feature",
                "type": "subclass_feature",
                "summary": "Gain a feature from your chosen Wizard subclass.",
                "description": "You gain a final, powerful ability based on the Arcane Tradition you chose at 3rd level.",
                "details": {
                    "Action": "Passive"
                }
            }
        ],
        16: [
            {
                "id": "feat_or_asi_16",
                "name": "Feat or ASI",
                "summary": "Choose a feat or increase ability scores.",
                "details": {
                    "Action": "Passive"
                }
            }
        ],
        18: [
            {
                "id": "wizard_spell_mastery",
                "name": "Spell Mastery",
                "summary": "Cast a chosen level 1 and level 2 spell at will.",
                "description": "You have achieved such mastery over certain spells that you can cast them at will. Choose a 1st-level wizard spell and a 2nd-level wizard spell that are in your spellbook. You can cast those spells at their lowest level without expending a spell slot when you have them prepared. \n\nWhen taking a Long Rest, you can go deep in study to swap one or both of these spells for different spells of the same levels.",
                "details": {
                    "Action": "Passive",
                    "uses": 1,
                    "recharge": "Long Rest",
                    "recharge_effect": "swap_mastery_spells",
                    "at_will_levels": [1, 2]
                }
            }
        ],
        19: [
            {
                "id": "epic_boon_or_feat_19",
                "name": "Epic Boon or Feat",
                "summary": "Choose a powerful Epic Boon or another feat.",
                "details": {
                    "Action": "Passive"
                }
            }
        ],
        20: [
            {
                "id": "wizard_signature_spell",
                "name": "Signature Spell",
                "summary": "Choose two level 3 spells to cast once for free.",
                "description": "You gain mastery over two powerful spells and can cast them with little effort. Choose two 3rd-level wizard spells in your spellbook as your signature spells. You always have these spells prepared, and they don't count against the number of spells you have prepared. \n\nYou can cast each of them once at 3rd level without expending a spell slot. When you do so, you can't do so again until you finish a Short or Long Rest.",
                "details": {
                    "Action": "Passive",
                    "uses": 2,
                    "signature_level": 3,
                    "recharge": "Short or Long Rest"
                }
            }
        ]
    }
}


CLASSES = {
    "barbarian": BARBARIAN,
    "bard": BARD,
    "cleric": CLERIC,
    "druid": DRUID,
    "fighter": FIGHTER,
    "monk": MONK,
    "paladin": PALADIN,
    "ranger": RANGER,
    "rogue": ROGUE,
    "sorcerer": SORCERER,
    "warlock": WARLOCK,
    "wizard": WIZARD
}
