"""
Subclass definitions for the Barbarian class.
"""

BARBARIAN_SUBCLASSES = {
    "berserker": {
        "id": "berserker",
        "name": "Path Of The Berserker",
        "description": "For some barbarians, rage is a means to an end—that end being violence. The Path of the Berserker is a path of untamed fury, slick with blood. As you enter the berserker's rage, you thrill in the chaos of battle, heedless of your own health or well-being.",
        "features": {
            3: [
                {
                    "id": "berserker_frenzy",
                    "name": "Frenzy",
                    "summary": "Deal extra d6s of damage (equal to Rage Bonus) on your first Reckless Attack hit each turn.",
                    "details": {
                        "damage_die": "d6",
                        "die_count": "Rage Bonus",
                        "restriction": "First hit on turn, must use Reckless Attack while Raging"
                    }
                }
            ],
            6: [
                {
                    "id": "berserker_mindless_rage",
                    "name": "Mindless Rage",
                    "summary": "Immunity to Charmed and Frightened conditions while Raging; ends existing effects upon entering Rage."
                }
            ],
            10: [
                {
                    "id": "berserker_retaliation",
                    "name": "Retaliation",
                    "summary": "Use a Reaction to make a melee attack against a creature within 5ft that deals damage to you."
                }
            ],
            14: [
                {
                    "id": "berserker_intimidating_presence",
                    "name": "Intimidating Presence",
                    "summary": "Bonus Action to Frighten creatures in a 30ft Emanation (WIS save); can recharge by expending a Rage use.",
                    "details": {
                        "action": "Bonus Action",
                        "area": "30ft Emanation",
                        "save_dc": "8 + STR mod + Proficiency Bonus",
                        "recharge": "Long Rest or expend one Rage use"
                    }
                }
            ]
        }
    },
    "wild_heart": {
        "id": "wild_heart",
        "name": "Path Of The Wild Heart",
        "description": "The Path of the Wild Heart is a journey that brings a barbarian into spiritual kinship with the natural world. Your rage is not just fury; it is a primal connection to the animal spirits that guide and protect you.",
        "features": {
            3: [
                {
                    "id": "wild_heart_animal_speaker",
                    "name": "Animal Speaker",
                    "summary": "Cast Beast Sense and Speak with Animals as Rituals using Wisdom.",
                    "details": {
                        "spells": ["Beast Sense", "Speak with Animals"],
                        "casting_mode": "Ritual only",
                        "ability": "Wisdom"
                    }
                },
                {
                    "id": "wild_heart_rage_of_the_wilds",
                    "name": "Rage of the Wilds",
                    "summary": "Choose an animal spirit benefit whenever you activate your Rage.",
                    "details": {
                        "options": {
                            "Bear": "Resistance to all damage types except Force, Necrotic, Psychic, and Radiant.",
                            "Eagle": "Dash and Disengage as part of the Bonus Action used to Rage; can take both as a Bonus Action while Raging.",
                            "Wolf": "Allies have Advantage on attack rolls against enemies within 5ft of you."
                        }
                    }
                }
            ],
            6: [
                {
                    "id": "wild_heart_aspect_of_the_wilds",
                    "name": "Aspect of the Wilds",
                    "summary": "Gain a permanent animal aspect, swappable on a Long Rest.",
                    "details": {
                        "options": {
                            "Owl": "Gain 60ft Darkvision (or +60ft if you already have it).",
                            "Panther": "Gain a Climb Speed equal to your Speed.",
                            "Salmon": "Gain a Swim Speed equal to your Speed."
                        },
                        "recharge": "Long Rest (to swap)"
                    }
                }
            ],
            10: [
                {
                    "id": "wild_heart_nature_speaker",
                    "name": "Nature Speaker",
                    "summary": "Cast Commune with Nature as a Ritual using Wisdom.",
                    "details": {
                        "spells": ["Commune with Nature"],
                        "casting_mode": "Ritual only",
                        "ability": "Wisdom"
                    }
                }
            ],
            14: [
                {
                    "id": "wild_heart_power_of_the_wilds",
                    "name": "Power of the Wilds",
                    "summary": "Gain an advanced animal spirit benefit whenever you activate your Rage.",
                    "details": {
                        "options": {
                            "Falcon": "Gain a Fly Speed equal to your Speed while unarmored.",
                            "Lion": "Enemies within 5ft have Disadvantage vs targets other than you or another Wild Heart Barbarian.",
                            "Ram": "Melee hits can knock Large or smaller creatures Prone."
                        }
                    }
                }
            ]
        }
    }
}
