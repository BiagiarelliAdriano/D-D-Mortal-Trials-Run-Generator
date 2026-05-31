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
                    "description": "Once per turn when you hit a creature with an Unarmed Strike and deal damage, you can expend 1 Focus Point to deal extra Necrotic damage equal to one roll of your Martial Arts die plus your Wisdom modifier.",
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
                    "description": "As a Magic action, you can expend 1 Focus Point to touch a creature and restore a number of Hit Points equal to a roll of your Martial Arts die plus your Wisdom modifier. When you use your Flurry of Blows, you can replace one of the Unarmed Strikes with a use of this feature without expending a Focus Point for the healing.",
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
                    "description": "You gain proficiency in the Insight and Medicine skills and proficiency with the Herbalism Kit.",
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
                    "description": "Your Hand of Harm and Hand of Healing improve, as detailed below. \n *-Hand of Harm-* When you use Hand of Harm on a creature, you can also give that creature the Poisoned condition until the end of your next turn. \n *-Hand of Healing-* When you use Hand of Healing, you can also end one of the following conditions on the creature you heal: Blinded, Deafened, Paralyzed, Poisoned, or Stunned.",
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
                    "description": "When you use Flurry of Blows, you can replace each of the Unarmed Strikes with a use of Hand of Healing without expending Focus Points for the healing. In addition, when you make an Unarmed Strike with Flurry of Blows and deal damage, you can use Hand of Harm with that strike without expending a Focus Point for Hand of Harm. You can still use Hand of Harm only once per turn. You can use these benefits a total number of times equal to your Wisdom modifier (minimum of once). You regain all expended uses when you finish a Long Rest.",
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
                    "description": "Your mastery of life energy opens the door to the ultimate mercy. As a Magic action, you can touch the corpse of a creature that died within the past 24 hours and expend 5 Focus Points. The creature then returns to life with a number of Hit Points equal to 4d10 plus your Wisdom modifier. If the creature died with any of the following conditions, the creature revives with the conditions removed: Blinded, Deafened, Paralyzed, Poisoned, and Stunned. Once you use this feature, you can't use it again until you finish a Long Rest.",
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
                    "description": "You have learned to draw on the power of the Shadowfell, gaining the following benefits. \n *-Darkness-* You can expend 1 Focus Point to cast the Darkness spell without spell components. You can see within the spell's area when you cast it with this feature. While the spell persists, you can move its area of Darkness to a space within 60 feet of yourself at the start of each of your turns. \n *-Darkvision-* You gain Darkvision with a range of 60 feet. If you already have Darkvision, its range increases by 60 feet. \n *Shadowy Figments-* You know the Minor Illusion spell. Wisdom is your spellcasting ability for it.",
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
                    "description": "While entirely within Dim Light or Darkness, you can use a Bonus Action to teleport up to 60 feet to an unoccupied space you can see that is also in Dim Light or Darkness. You then have Advantage on the next melee attack you make before the end of the current turn.",
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
                    "description": "You can draw on your Shadowfell connection to empower your teleportation. When you use your Shadow Step, you can expend 1 Focus Point to remove the requirement that you must start and end in Dim Light or Darkness for that use of the feature. As part of this Bonus Action, you can make an Unarmed Strike immediately after you teleport.",
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
                    "description": "As a Magic action while entirely within Dim Light or Darkness, you can expend 3 Focus Points to shroud yourself with shadows for 1 minute, until you have the Incapacitated condition, or until you end your turn in Bright Light. While shrouded by these shadows, you gain the following benefits. *-Invisibility-* You have the Invisible condition. *-Partially Incorporeal-* You can move through occupied spaces as if they were Difficult Terrain. If you end your turn in such a space, you are shunted to the last unoccupied space you were in. *-Shadow Flurry-* You can use your Flurry of Blows without expending any Focus Points.",
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
                    "description": "At the start of your turn, you can expend 1 Focus Point to imbue yourself with elemental energy. The energy lasts for 10 minutes or until you have the Incapacitated condition. You gain the following benefits while this feature is active. *-Reach-* When you make an Unarmed Strike, your reach is 10 feet greater than normal, as elemental energy extends from you. *-Elemental Strikes-* Whenever you hit with your Unarmed Strike, you can cause it to deal your choice of Acid, Cold, Fire, Lightning, or Thunder damage rather than its normal damage type. When you deal one of these types with it, you can also force the target to make a Strength saving throw. On a failed save, you can move the target up to 10 feet toward or away from you, as elemental energy swirls around it.",
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
                    "description": "You know the Elementalism spell. Wisdom is your spellcasting ability for it.",
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
                    "description": "As a Magic action, you can expend 2 Focus Points to cause elemental energy to burst in a 20-foot-radius Sphere centered on a point within 120 feet of yourself. Choose a damage type: Acid, Cold, Fire, Lightning, or Thunder. Each creature in the Sphere must make a Dexterity saving throw. On a failed save, a creature takes damage of the chosen type equal to three rolls of your Martial Arts die. On a successful save, a creature takes half as much damage.",
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
                    "description": "While your Elemental Attunement is active, you also have a Fly Speed and a Swim Speed equal to your Speed.",
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
                    "description": "While your Elemental Attunement is active, you also gain the following benefits. \n *-Damage Resistance-* You gain Resistance to one of the following damage types of your choice: Acid, Cold, Fire, Lightning, or Thunder. At the start of each of your turns, you can change this choice. \n *-Destructive Stride-* When you use your Step of the Wind, your Speed increases by 20 feet until the end of the turn. For that duration, any creature of your choice takes damage equal to one roll of your Martial Arts die when you enter a space within 5 feet of it. The damage type is your choice of Acid, Cold, Fire, Lightning, or Thunder. A creature can take this damage only once per turn. *-Empowered Strikes-* Once on each of your turns, you can deal extra damage to a target equal to one roll of your Martial Arts die when you hit it with an Unarmed Strike. The extra damage is the same type dealt by that strike.",
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
                    "description": "Whenever you hit a creature with an attack granted by your Flurry of Blows, you can impose one of the following effects on that target. \n *-Addle-* The target can't make Opportunity Attacks until the start of its next turn. \n *-Push-* The target must succeed on a Strength saving throw or be pushed up to 15 feet away from you. \n *-Topple-* The target must succeed on a Dexterity saving throw or have the Prone condition.",
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
                    "description": "You gain the ability to heal yourself. As a Bonus Action, you can roll your Martial Arts die. You regain a number of Hit Points equal to the number rolled plus your Wisdom modifier (minimum of 1 Hit Point regained). You can use this feature a number of times equal to your Wisdom modifier (minimum of once), and you regain all expended uses when you finish a Long Rest.",
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
                    "description": "When you take a Bonus Action other than Step of the Wind, you can also use Step of the Wind immediately after that Bonus Action.",
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
                    "description": "You gain the ability to set up lethal vibrations in someone's body. When you hit a creature with an Unarmed Strike, you can expend 4 Focus Points to start these imperceptible vibrations, which last for a number of days equal to your Monk level. The vibrations are harmless unless you take an action to end them. Alternatively, when you take the Attack action on your turn, you can forgo one of the attacks to end the vibrations. To end them, you and the target must be on the same plane of existence. When you end them, the target must make a Constitution saving throw, taking 10d12 Force damage on a failed save or half as much damage on a successful one. You can have only one creature under the effect of this feature at a time. You can end the vibrations harmlessly (no action required).",
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
