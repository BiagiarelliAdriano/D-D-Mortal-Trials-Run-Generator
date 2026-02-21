"""
Subclass definitions for the Monk class.
"""

MONK_SUBCLASSES = {
    "mercy": {
        "id": "mercy",
        "name": "Warrior of Mercy",
        "description": "Monks of the Way of Mercy learn to manipulate the life force of others to bring aid to those in need. They are wandering physicians to the poor and hurt, but to their enemies, they are bringers of a swift end, using their knowledge of anatomy to strike with lethal precision.",
        "features": {
            3: [
                {
                    "id": "mercy_hand_of_harm",
                    "name": "Hand Of Harm",
                    "summary": "Once per turn, expend 1 Focus Point on an Unarmed Strike hit to deal extra Necrotic damage.",
                    "details": {
                        "cost": "1 Focus Point",
                        "damage": "Martial Arts die + Wisdom modifier",
                        "type": "Necrotic",
                        "limit": "Once per turn"
                    }
                },
                {
                    "id": "mercy_hand_of_healing",
                    "name": "Hand Of Healing",
                    "summary": "Magic action: expend 1 Focus Point to heal a creature. Can replace one Flurry of Blows strike for free healing.",
                    "details": {
                        "action": "Magic Action (or part of Flurry of Blows)",
                        "cost": "1 Focus Point (0 if replacing Flurry of Blows strike)",
                        "healing": "Martial Arts die + Wisdom modifier"
                    }
                },
                {
                    "id": "mercy_implements_of_mercy",
                    "name": "Implements of Mercy",
                    "summary": "Gain proficiency in Insight, Medicine, and Herbalism Kit.",
                    "details": {
                        "skills": ["Insight", "Medicine"],
                        "tools": ["Herbalism Kit"]
                    }
                }
            ],
            6: [
                {
                    "id": "mercy_physicians_touch",
                    "name": "Physician's Touch",
                    "summary": "Hand of Harm can Poison; Hand of Healing can end Blinded, Deafened, Paralyzed, Poisoned, or Stunned.",
                    "details": {
                        "hand_of_harm_upgrade": "Target is Poisoned until end of your next turn",
                        "hand_of_healing_upgrade": "End one: Blinded, Deafened, Paralyzed, Poisoned, or Stunned"
                    }
                }
            ],
            11: [
                {
                    "id": "mercy_flurry_of_healing_and_harm",
                    "name": "Flurry Of Healing And Harm",
                    "summary": "Replace Flurry of Blows strikes with free Hand of Healing; use free Hand of Harm with Flurry (Wis mod/Long Rest).",
                    "details": {
                        "healing_buff": "Replace both Flurry of Blows strikes with Hand of Healing for 0 Focus Points each",
                        "harm_buff": "Use Hand of Harm during Flurry of Blows for 0 Focus Points",
                        "uses": "Wisdom modifier (minimum 1)",
                        "recharge": "Long Rest"
                    }
                }
            ],
            17: [
                {
                    "id": "mercy_hand_of_ultimate_mercy",
                    "name": "Hand Of Ultimate Mercy",
                    "summary": "Magic action: expend 5 Focus Points to revive a creature that died within 24 hours.",
                    "details": {
                        "action": "Magic Action",
                        "cost": "5 Focus Points",
                        "time_limit": "24 hours",
                        "healing": "4d10 + Wisdom modifier",
                        "cleanse": "Removes Blinded, Deafened, Paralyzed, Poisoned, and Stunned",
                        "recharge": "Long Rest"
                    }
                }
            ]
        }
    },
    "shadow": {
        "id": "shadow",
        "name": "Warrior of Shadow",
        "description": "Monks of the Way of Shadow follow a tradition that values stealth and subterfuge. These monks might be called ninjas or shadowdancers, and they serve as spies and assassins. They draw on the power of the Umbral Realm to wrap themselves in darkness and move unseen across the battlefield.",
        "features": {
            3: [
                {
                    "id": "shadow_arts",
                    "name": "Shadow Arts",
                    "summary": "Cast Darkness (1 Focus Point, can see through it); gain Darkvision (60ft) and Minor Illusion.",
                    "details": {
                        "darkness_spell": {
                            "cost": "1 Focus Point",
                            "components": False,
                            "special": "Can see within the area; can move the area 60ft at start of turn (no action)."
                        },
                        "darkvision": "60ft (or +60ft if already possessed)",
                        "minor_illusion": "Known (Wisdom casting ability)"
                    }
                }
            ],
            6: [
                {
                    "id": "shadow_step",
                    "name": "Shadow Step",
                    "summary": "Bonus Action: teleport 60ft between Dim Light/Darkness; gain Advantage on next melee attack.",
                    "details": {
                        "action": "Bonus Action",
                        "range": "60ft",
                        "condition": "Start and end must be in Dim Light or Darkness",
                        "advantage": "Advantage on next melee attack roll this turn"
                    }
                }
            ],
            11: [
                {
                    "id": "shadow_improved_shadow_step",
                    "name": "Improved Shadow Step",
                    "summary": "Expend 1 Focus Point to remove light requirement for Shadow Step and make an Unarmed Strike as part of the BA.",
                    "details": {
                        "buff": "Expend 1 Focus Point to ignore light/darkness requirement",
                        "extra_attack": "Make an Unarmed Strike as part of the Shadow Step Bonus Action"
                    }
                }
            ],
            17: [
                {
                    "id": "shadow_cloak_of_shadows",
                    "name": "Cloak Of Shadows",
                    "summary": "Magic Action (3 Focus Points) in Dim/Darkness: become Invisible and move through obstacles (1 min). Free Flurry of Blows.",
                    "details": {
                        "action": "Magic Action",
                        "cost": "3 Focus Points",
                        "condition": "Must be in Dim Light or Darkness",
                        "duration": "1 minute (ends early in Bright Light or if Incapacitated)",
                        "benefits": [
                            "Invisible condition",
                            "Move through occupied spaces (Difficult Terrain)",
                            "Flurry of Blows costs 0 Focus Points"
                        ]
                    }
                }
            ]
        }
    },
    "elements": {
        "id": "elements",
        "name": "Warrior of the Elements",
        "description": "Monks of the Way of the Elements channel the raw power of the primordial planes. By focusing their life force, they can extend their strikes with elemental energy, wreath themselves in protective auras, and unleash devastating bursts of fire, ice, or lightning upon their foes.",
        "features": {
            3: [
                {
                    "id": "elements_elemental_attunement",
                    "name": "Elemental Attunement",
                    "summary": "Expend 1 Focus Point (10 min) for +10ft reach, elemental damage, and a 10ft push/pull on hit.",
                    "details": {
                        "cost": "1 Focus Point",
                        "duration": "10 minutes",
                        "benefits": [
                            "Unarmed Strike reach +10ft",
                            "Damage type: Acid, Cold, Fire, Lightning, or Thunder"
                        ],
                        "on_hit": "Strength save (DC 8 + Wis + Prof) or move target 10ft toward/away"
                    }
                },
                {
                    "id": "elements_manipulate_elements",
                    "name": "Manipulate Elements",
                    "summary": "Know the Elementalism spell (Wisdom).",
                    "details": {
                        "spell": "Elementalism",
                        "ability": "Wisdom"
                    }
                }
            ],
            6: [
                {
                    "id": "elements_elemental_burst",
                    "name": "Elemental Burst",
                    "summary": "Magic Action (2 Focus Points): 20ft sphere burst (120ft range) for 3x Martial Arts die damage.",
                    "details": {
                        "action": "Magic Action",
                        "cost": "2 Focus Points",
                        "range": "120ft",
                        "area": "20ft radius Sphere",
                        "damage": "3x Martial Arts die",
                        "types": ["Acid", "Cold", "Fire", "Lightning", "Thunder"],
                        "save": "Dexterity (Half on success)"
                    }
                }
            ],
            11: [
                {
                    "id": "elements_stride_of_the_elements",
                    "name": "Stride Of The Elements",
                    "summary": "Fly and Swim speeds equal to walking speed while Elemental Attunement is active.",
                    "details": {
                        "condition": "Elemental Attunement active",
                        "speeds": ["Fly", "Swim"]
                    }
                }
            ],
            17: [
                {
                    "id": "elements_elemental_epitome",
                    "name": "Elemental Epitome",
                    "summary": "Gain damage resistance, extra Step of the Wind speed/damage, and extra Unarmed Strike damage.",
                    "details": {
                        "resistance": "Acid, Cold, Fire, Lightning, or Thunder (changeable at start of turn)",
                        "step_of_the_wind_buff": "+20ft speed; 5ft aura deals 1 Martial Arts die damage to creatures entered",
                        "extra_damage": "Once per turn: +1 Martial Arts die damage on Unarmed Strike hit"
                    }
                }
            ]
        }
    },
    "open_hand": {
        "id": "open_hand",
        "name": "Warrior of the Open Hand",
        "description": "Monks of the Way of the Open Hand are the ultimate masters of martial arts combat, whether armed or unarmed. They learn techniques to push and trip their opponents, manipulate focus to heal their bodies, and eventually master the technique of the Quivering Palm to deal lethal strikes with a single touch.",
        "features": {
            3: [
                {
                    "id": "open_hand_technique",
                    "name": "Open Hand Technique",
                    "summary": "Impose Addle (no reactions), Push (15ft), or Topple (Prone) when hitting with Flurry of Blows.",
                    "details": {
                        "trigger": "Hit with Flurry of Blows attack",
                        "options": {
                            "addle": "Target can't make Opportunity Attacks until start of its next turn",
                            "push": "Strength save or pushed 15ft away",
                            "topple": "Dexterity save or Prone condition"
                        }
                    }
                }
            ],
            6: [
                {
                    "id": "open_hand_wholeness_of_body",
                    "name": "Wholeness Of Body",
                    "summary": "Bonus Action: heal 1 Martial Arts die + Wisdom mod HP (Wis mod/Long Rest).",
                    "details": {
                        "action": "Bonus Action",
                        "healing": "1 Martial Arts die + Wisdom modifier",
                        "uses": "Wisdom modifier (minimum 1)",
                        "recharge": "Long Rest"
                    }
                }
            ],
            11: [
                {
                    "id": "open_hand_fleet_step",
                    "name": "Fleet Step",
                    "summary": "When taking a Bonus Action other than Step of the Wind, use Step of the Wind for free immediately after.",
                    "details": {
                        "trigger": "Any Bonus Action except Step of the Wind",
                        "effect": "Use Step of the Wind immediately after"
                    }
                }
            ],
            17: [
                {
                    "id": "open_hand_quivering_palm",
                    "name": "Quivering Palm",
                    "summary": "Expend 4 Focus Points to set up lethal vibrations (10d12 Force damage when ended).",
                    "details": {
                        "activation_cost": "4 Focus Points",
                        "trigger": "Hit with Unarmed Strike",
                        "duration": "Days equal to Monk level",
                        "execution": "Action (or forgo 1 Attack) while on same plane",
                        "damage": "10d12 Force (Half on failed Con save)",
                        "limit": "Only one creature at a time"
                    }
                }
            ]
        }
    }
}
