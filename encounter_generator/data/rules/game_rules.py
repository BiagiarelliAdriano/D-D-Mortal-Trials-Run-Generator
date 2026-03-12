CLASS_HIT_DICE = {
    "Barbarian": 12,
    "Bard": 8,
    "Cleric": 8,
    "Druid": 8,
    "Fighter": 10,
    "Monk": 8,
    "Paladin": 10,
    "Ranger": 10,
    "Rogue": 8,
    "Sorcerer": 6,
    "Warlock": 8,
    "Wizard": 6,
}

BRUTAL_STRIKE_OPTIONS = {
    "forceful_blow": {
        "name": "Forceful Blow",
        "description": "The target is pushed 15ft straight away from you. You can then move up to half your Speed straight toward the target without provoking Opportunity Attacks."
    },
    "hamstring_blow": {
        "name": "Hamstring Blow",
        "description": "The target's Speed is reduced by 15ft until the start of your next turn. A target can be affected by only one Harmstring Blow at a time, the most recent one."
    },
    "staggering_blow": {
        "name": "Staggering Blow",
        "description": "The target has Disadvantage on the next saving throw it makes, and it can't make Opportunity Attacks until the start of your next turn."
    },
    "sundering_blow": {
        "name": "Sundering Blow",
        "description": "Before the start of your next turn, the next attack roll made by another creature against the target gains a +5 bonus to the roll. An attack roll can gain only one Sundering Blow bonus."
    }
}

WEAPON_MASTERY_OPTIONS = {
    "Cleave": {
        "name": "cleave",
        "Action": "Passive",
        "description": "If you hit a creature with a Melee Attack Roll using this weapon, you can make a Melee Attack Roll with the weapon against a second creature within 5ft of the first that is also within your reach. On a hit, the second creature takes the weapon's damage, but don't add your ability modifier to that damage unless that modifier is negative. You can make this extra Attack only once per turn."
    },
    "Graze": {
        "name": "graze",
        "Action": "Passive",
        "description": "If your Attack Roll with this weapon misses a creature, you can deal damage to that creature equal to the ability modifier you used to make the Attack Roll. This damage is the same type dealt by the weapon, and the damage can be increased only by increasing the ability modifier."
    },
    "Nick": {
        "name": "nick",
        "Action": "Passive",
        "description": "When you make the extra Attack of the Light property, you can make it as part of the Attack Action instead of a Bonus Action. You can make this extra Attack only once per turn"
    },
    "Push": {
        "name": "push",
        "Action": "Passive",
        "description": "If you hit a creature with this weapon, you can push the creature up to 10ft straight away from yourself if it is Large or smaller."
    },
    "Sap": {
        "name": "sap",
        "Action": "Passive",
        "description": "If you hit a creature withi this weapon, that creature has Disadvantage on its next Attack Roll before the start of your next turn."
    },
    "Slow": {
        "name": "slow",
        "Action": "Passive",
        "description": "If you hit a creature with this weapon and deal damage to it, you can reduce its Speed by 10ft until the start of your next turn. If the creature is hit more than once by weapons that have this property, the Speed reduction doesn't exceed 10ft."
    },
    "Topple": {
        "name": "topple",
        "Action": "Passive",
        "description": "If you hit a creature with this weapon, you can force the creature to make a Constitution Saving Throw, DC 8 plus the ability modifier used to make the Attack Roll and your Proficiency Bonus. On a failed save, the creature has the Prone condition."
    },
    "Vex": {
        "name": "vex",
        "Action": "Passive",
        "description": "If you hit a creature with this weapon and deal damage to the creature, you have Advantage on your next Attack Roll against that creature before the end of your next turn."
    }
}