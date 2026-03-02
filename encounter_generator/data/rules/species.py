SPECIES = [
    {
        "name": "Aasimar",
        "description": """Aasimar are mortals born with an echo of divine resonance within them.
            Not chosen by Gods—who grant no favors—but shaped by inner force, they reflect celestial
            power through sheer will. Their features hint at radiant potential: luminous eyes,
            glowing veins, halos of light. These signs begin faint, growing as the Aasimar learns to 
            waken their soul's brilliance. In Kharoth, they are not messengers of the divine—but mortals
            whose ambition burns bright enough to mimic it.""",
        "summary": "Mortals with divine resonance, reflecting celestial power through sheer will in Kharoth.",
        "creature_type": "Humanoid",
        "size": ["Medium", "Small"],
        "speed": "30ft",
        "features": [
            {
                "id": "aasimar_celestial_resistance",
                "name": "Celestial Resistance",
                "summary": "Resistance to Necrotic and Radiant damage.",
                "description": "Your celestial heritage grants you an innate resilience against the energies of life and death. You have resistance to Necrotic damage and Radiant damage."
            },
            {
                "id": "aasimar_darkvision",
                "name": "Darkvision",
                "summary": "See in the dark up to 60ft.",
                "description": "You can see in dim light within 60 feet of you as if it were bright light, and in darkness as if it were dim light. You can't discern color in darkness, only shades of gray."
            },
            {
                "id": "aasimar_healing_hands",
                "name": "Healing Hands",
                "summary": "Touch a creature to heal them (d4s equal to Prof Bonus).",
                "description": "As a Magic Action, you touch a creature and roll a number of d4s equal to your Proficiency Bonus. The creature regains that many Hit Points. Once you use this trait, you can't use it again until you finish a Long Rest.",
                "details": {
                    "Action": "Magic Action",
                    "Healing": "PB x d4",
                    "Usage": "1 / Long Rest"
                }
            },
            {
                "id": "aasimar_light_bearer",
                "name": "Light Bearer",
                "summary": "You know the Light cantrip.",
                "description": "You know the Light cantrip. Charisma is your spellcasting ability for it."
            },
            {
                "id": "aasimar_celestial_revelation",
                "name": "Celestial Revelation",
                "summary": "Transform to gain wings, radiance, or a shroud (lvl 3).",
                "description": "When you reach character level 3, you can transform as a Bonus Action using one of the options below (choose each time you transform). The transformation lasts 1 minute or until you end it (no action required). You regain this ability after a Long Rest.\n\nOnce per turn during the transformation, when you deal damage to a target, you can deal extra damage equal to your Proficiency Bonus (Radiant or Necrotic depending on the form).",
                "details": {
                    "Action": "Bonus Action",
                    "Duration": "1 Minute",
                    "Usage": "1 / Long Rest",
                    "Extra Damage": "PB (once/turn)",
                    "Options": [
                        {
                            "name": "Heavenly Wings",
                            "description": "Two shimmering, spectral wings sprout from your back. You gain a Fly speed equal to your walking speed."
                        },
                        {
                            "name": "Inner Radiance",
                            "description": "You emit bright light in a 10-foot radius and dim light for an additional 10 feet. At the end of each of your turns, each creature within 10 feet of you takes Radiant damage equal to your Proficiency Bonus."
                        },
                        {
                            "name": "Necrotic Shroud",
                            "description": "Skeletal, flightless wings sprout from your back. Each creature within 10 feet of you must succeed on a Charisma saving throw (DC 8 + Cha mod + Prof Bonus) or become Frightened until the end of your next turn."
                        }
                    ]
                }
            }
        ]
    },
    {
        "name": "Dragonborn",
        "description": """Dragonborn are mortal echoes of the ancient dragons that once ruled the skies
            and split mountains with their breath. Their origin lies in a time when nature, shaped by
            divine law but left to evolve on its own, brought forth eggs unlike any before, vessels where
            draconic essence crystallized in mortal form. Whether these eggs were laid by dragons or born
            from the world's own ambition, none can say. Dragonborn resemble wingless, upright dragons. Scales
            glistening in hues of fire and frost, horns curling from their brows, eyes bright with inner flame.
            Their breath holds echoes of the elements, and their presence carries the weight of ancient power.
            Though they share the blood of dragons, their destiny is their own to forge.""",
        "summary": "Mortal echoes of ancient dragons, channeling elemental breath and draconic majesty.",
        "variations": ["Black", "Blue", "Brass", "Bronze", "Copper", "Gold", "Green", "Red", "Silver", "White"],
        "creature_type": "Humanoid",
        "size": "Medium",
        "speed": "30ft",
        "features": [
            {
                "id": "dragonborn_draconic_ancestry",
                "name": "Draconic Ancestry",
                "summary": "Choose a dragon progenitor to determine your damage type.",
                "description": "Your lineage stems from a dragon progenitor. Your choice affects your Breath Weapon and Damage Resistance traits as well as your appearance.",
                "details": {
                    "Ancestors": "Black, Blue, Brass, Bronze, Copper, Gold, Green, Red, Silver, White"
                }
            },
            {
                "id": "dragonborn_breath_weapon",
                "name": "Breath Weapon",
                "summary": "Exhale elemental energy in a cone or line.",
                "description": "When you take the Attack action on your turn, you can replace one of your attacks with an exhalation of magical energy in either a 15ft Cone or a 30ft Line that is 5ft wide (choose the shape each time). Each creature in that area must make a Dexterity saving throw (DC 8 + Con mod + Prof Bonus). On a failed save, a creature takes elemental damage. On a successful save, a creature takes half as much damage.",
                "details": {
                    "Action": "Replace 1 Attack",
                    "Area": "15ft Cone or 30ft Line",
                    "Damage": {
                        "1": "1d10",
                        "5": "2d10",
                        "11": "3d10",
                        "17": "4d10"
                    },
                    "Usage": "PB / Long Rest"
                }
            },
            {
                "id": "dragonborn_damage_resistance",
                "name": "Damage Resistance",
                "summary": "Resistance to your ancestry's damage type.",
                "description": "You have Resistance to the damage type determined by your Draconic Ancestry trait."
            },
            {
                "id": "dragonborn_darkvision",
                "name": "Darkvision",
                "summary": "See in the dark up to 60ft.",
                "description": "You have Darkvision with a range of 60ft."
            },
            {
                "id": "dragonborn_draconic_flight",
                "name": "Draconic Flight",
                "summary": "Sprout spectral wings to fly (lvl 5).",
                "description": "Starting at level 5, you can channel draconic magic to give yourself temporary flight. As a Bonus Action, you sprout spectral wings on your back that last for 10 minutes or until you retract them (no action required).",
                "details": {
                    "Action": "Bonus Action",
                    "Duration": "10 Minutes",
                    "Speed": "Flight = Walking Speed",
                    "Usage": "1 / Long Rest"
                }
            }
        ]
    },
    {
        "name": "Dwarf",
        "description": """Dwarves are steadfast folk of stone and forge, known for their deep traditions, enduring
            craftsmanship, and unshakable resolve. Many trace their origins to mountainholds older than recorded history,
            carved from the bones of the world long before The Convergence. Dwarves live long lives, often exceeding 350 years,
            and carry with them generations of memory, custom, and pride.
            Short and stout, their bodies are built to withstand both time and battle. Thick-bearded and strong-handed,
            they are often seen adorned with runes, braids, or heirlooms passed down across centuries. Though not all
            Dwarves dwell beneath the mountains, their hearts are shaped by them: resilient, deliberate, and bound by oath.
            Whether forging legendary weapons, preserving ancient lore, or fighting to uphold their clan's honor.
            Dwarves bring a legacy of grit and glory to every corner of Kharoth.""",
        "summary": "Resilient masters of stone and forge, defined by ancient tradition and undying pride.",
        "creature_type": "Humanoid",
        "size": "Medium",
        "speed": "30ft",
        "features": [
            {
                "id": "dwarf_darkvision",
                "name": "Darkvision",
                "summary": "See in the dark up to 120ft.",
                "description": "You have Darkvision with a range of 120ft."
            },
            {
                "id": "dwarf_dwarven_resilience",
                "name": "Dwarven Resilience",
                "summary": "Resistance to Poison damage and advantage on poison saves.",
                "description": "You have Resistance to Poison damage. You also have Advantage on saving throws you make to avoid or end the Poisoned condition."
            },
            {
                "id": "dwarf_dwarven_toughness",
                "name": "Dwarven Toughness",
                "summary": "+1 Max HP per level.",
                "description": "Your Hit Point maximum increases by 1, and it increases by 1 again whenever you gain a level."
            },
            {
                "id": "dwarf_stonecunning",
                "name": "Stonecunning",
                "summary": "Gain Tremorsense 60ft on stone surfaces.",
                "description": "As a Bonus Action, you gain Tremorsense with a range of 60ft for 10 minutes. You must be on a stone surface or touching a stone surface to use this Tremorsense. The stone can be natural or worked.",
                "details": {
                    "Action": "Bonus Action",
                    "Duration": "10 Minutes",
                    "Range": "60ft",
                    "Usage": "PB / Long Rest"
                }
            }
        ]
    },
    {
        "name": "Elf",
        "description": """Elves are timeless beings shaped by wonder, memory, and grace. Said to be among the first mortals
            sculpted in the Age of Making, they have always walked closer to the arcane than most. An Elf can live well over
            700 years, and many remember events that have become myth to other species. To be Elven is to live in rhythms
            measured not in days, but in centuries.
            Tall and slender, with eyes like starlight and voices like wind through leaves, Elves embody elegance made flesh.
            Their features reflect the realms that bore them: wood, moon, sea, and beyond, each lineage etched into their spirit.
            Driven by curiosity, beauty, and personal truth, Elves do not rush, but they do not forget. Whether singing to trees
            older than empires or dueling for ideals older than kings, they remain ever as they were: watchful, wondrous,
            and endlessly enduring.
            Drow. Drow elves born of shadowed realms and deep stone, marked by obsidian skin, pale hair, and luminous eyes.
            Raised in forgotten cities beneath the earth, they are proud, cunning, and fiercely independent. Though once
            hidden from the world, many now rise to claim their place in it, on their own terms.
            High Elves. High Elves are graceful, long-lived Elves known for their sharp intellect and deep arcane affinity.
            Raised in radiant cities or ancient strongholds, they stufy magic as a birthright and tradition. To them,
            knowledge is power, and legacy is earned through mastery.
            Wood Elves. Wood Elves are reclusive and swift, shaped by generations spent among the wild places of Kharoth.
            They are guided by instinct, tradition, and a deep bond with the natural world, valuing freedom, survival,
            and harmony above all else.""",
        "summary": "Timeless and graceful beings with deep arcane ties and lineages older than memory.",
        "variations": ["Drow", "High Elves", "Wood Elves"],
        "creature_type": "Humanoid",
        "size": "Medium",
        "speed": "30ft",
        "features": [
            {
                "id": "elf_darkvision",
                "name": "Darkvision",
                "summary": "See in the dark up to 60ft.",
                "description": "You have Darkvision with a range of 60ft."
            },
            {
                "id": "elf_elven_lineage",
                "name": "Elven Lineage",
                "summary": "Gain spells based on your lineage (Drow, High Elf, or Wood Elf).",
                "description": "You are part of a lineage that grants you supernatural abilities. You gain benefits at levels 1, 3, and 5. Intelligence, Wisdom, or Charisma is your spellcasting ability for the spells you cast with this trait.",
                "details": {
                    "Options": [
                        {
                            "name": "Drow",
                            "description": "Level 1: Darkvision 120ft, Dancing Lights cantrip. Level 3: Faerie Fire. Level 5: Darkness."
                        },
                        {
                            "name": "High Elf",
                            "description": "Level 1: Prestidigitation (swappable on long rest). Level 3: Detect Magic. Level 5: Misty Step."
                        },
                        {
                            "name": "Wood Elf",
                            "description": "Level 1: +5ft Speed, Druidcraft cantrip. Level 3: Longstrider. Level 5: Pass Without Trace."
                        }
                    ]
                }
            },
            {
                "id": "elf_fey_ancestry",
                "name": "Fey Ancestry",
                "summary": "Advantage on saves against being Charmed.",
                "description": "You have Advantage on saving throws you make to avoid or end the Charmed condition."
            },
            {
                "id": "elf_keen_senses",
                "name": "Keen Senses",
                "summary": "Proficiency in Insight, Perception, or Survival.",
                "description": "You have proficiency in the Insight, Perception, or Survival skill."
            },
            {
                "id": "elf_trance",
                "name": "Trance",
                "summary": "4-hour meditation instead of sleep.",
                "description": "You don't need to sleep, and magic can't put you to sleep. You can finish a Long Rest in 4 hours if you spend those hours in a trancelike meditation, during which you retain consciousness."
            }
        ]
    },
    {
        "name": "Gnome",
        "description": """In the fractured lands of Kharoth, gnomes are not mere tinkers or whimsical pranksters. They are
            Ingenious Shadows, survivors and seekers of forbidden knowledge, masters of arcane draft and cunning invention.
            Unlike the myths spun by mortals who crave simple stories, gnomes are defined by relentless curiosity and
            unyielding resolve, carving out niches of influence through intellect and guile.
            Born with sharp minds and nimble fingers, gnomes refuse to rely on divine favor or ancestral blessings. Their
            magic and inventions spring from understanding the fabric of reality itself, bending laws of nature to their will.
            In a world shaped by divine indifference and mortal ambition, gnomes thrive by adaptation and innovation, often
            embracing the obscure and dangerous to gain an edge.
            Their small stature belies a fierce pride and resilience; many gnomes seek the objective of leaving a legacy for
            the Gods only with the purpose of testing their creations, their minds, and themselves against the greatest
            challenges possible. They are often found in shadowed enclaves or bustling workshops, where arcane runes mingle
            with mechanical gears, and every failure is but a lesson toward mastery.""",
        "summary": "Cunning and ingenious masters of invention and arcane manipulation in Kharoth.",
        "variations": ["Forest", "Rock"],
        "creature_type": "Humanoid",
        "size": "Small",
        "speed": "30ft",
        "features": [
            {
                "id": "gnome_darkvision",
                "name": "Darkvision",
                "summary": "See in the dark up to 60ft.",
                "description": "You have Darkvision with a range of 60ft."
            },
            {
                "id": "gnome_gnomish_cunning",
                "name": "Gnomish Cunning",
                "summary": "Advantage on Int, Wis, and Cha saving throws.",
                "description": "You have Advantage on Intelligence, Wisdom, and Charisma saving throws."
            },
            {
                "id": "gnome_gnomish_lineage",
                "name": "Gnomish Lineage",
                "summary": "Gain spells based on your lineage (Forest or Rock).",
                "description": "You are part of a lineage that grants you supernatural abilities. Intelligence, Wisdom, or Charisma is your spellcasting ability for the spells you cast with this trait.",
                "details": {
                    "Options": [
                        {
                            "name": "Forest Gnome",
                            "description": "You know the Minor Illusion cantrip. You also always have the Speak with Animals spell prepared, which you can cast without a spell slot PB times per day."
                        },
                        {
                            "name": "Rock Gnome",
                            "description": "You know the Mending and Prestidigitation cantrips. You can create Tiny clockwork devices that produce Prestidigitation effects."
                        }
                    ]
                }
            }
        ]
    },
    {
        "name": "Goliath",
        "description": """Goliaths are living echoes of a forgotten age, when stone itself still moved and warred beneath
            the sky. Their bodies carry the memory of that ancient struggle, marked by frost, shaped by impact, and tempered
            in silence. To them, glory is not a prize, but a burden earned through pain, ritual, and self-mastery.
            In a world obsessed with ascent, Goliaths walk a different path: one carved not upward, but inward, toward
            a greatness that neither Gods nor mortals can define for them.""",
        "summary": "Stalwart echoes of a stone-age, seeking glory through endurance and self-mastery.",
        "variations": ["Cloud", "Fire", "Frost", "Hill", "Stone", "Storm"],
        "creature_type": "Humanoid",
        "size": "Medium",
        "speed": "35ft",
        "features": [
            {
                "id": "goliath_giant_ancestry",
                "name": "Giant Ancestry",
                "summary": "Choice of supernatural boon (teleport, damage, reduction).",
                "description": "You are descended from Giants. You have a supernatural boon from your ancestry that you can use PB times per day.",
                "details": {
                    "Usage": "PB / Long Rest",
                    "Options": [
                        {
                            "name": "Cloud's Jaunt",
                            "description": "As a Bonus Action, you magically teleport up to 30ft to an unoccupied space you can see."
                        },
                        {
                            "name": "Fire's Burn",
                            "description": "When you hit a target with an attack roll and deal damage, deal 1d10 extra Fire damage."
                        },
                        {
                            "name": "Frost's Chill",
                            "description": "When you hit a target with an attack roll and deal damage, deal 1d6 extra Cold damage and reduce Speed by 10ft."
                        },
                        {
                            "name": "Hill's Tumble",
                            "description": "When you hit a Large or smaller creature with an attack roll and deal damage, knock it Prone."
                        },
                        {
                            "name": "Stone's Endurance",
                            "description": "When you take damage, use a Reaction to roll 1d12 + Con mod and reduce the damage by that total."
                        },
                        {
                            "name": "Storm's Thunder",
                            "description": "When you take damage from a creature within 60ft, use a Reaction to deal 1d8 Thunder damage to it."
                        }
                    ]
                }
            },
            {
                "id": "goliath_large_form",
                "name": "Large Form",
                "summary": "Transform to Large size (lvl 5).",
                "description": "Starting at character level 5, you can change your size to Large as a Bonus Action. For 10 minutes, you have Advantage on Strength checks and your Speed increases by 10ft.",
                "details": {
                    "Action": "Bonus Action",
                    "Duration": "10 Minutes",
                    "Usage": "1 / Long Rest"
                }
            },
            {
                "id": "goliath_powerful_build",
                "name": "Powerful Build",
                "summary": "Advantage on grapple saves and increased carrying capacity.",
                "description": "You have Advantage on any saving throw you make to end the Grappled condition. You also count as one size larger when determining your carrying capacity."
            }
        ]
    },
    {
        "name": "Halfling",
        "description": """Halflings are quiet survivors in a world that rarely makes room for the small.
            Their strength lies in memory, in tight-knit bonds, and in knowing when to step forward and when
            to disappear. They carry with them an uncanny luck, subtle and persistent, as if the world hesitates
            before harming them. Most halflings never speak of it. They simply press on with calm smiles and sharp
            eyes, weathering storms that break others, and enduring not through might, but through something no one
            can quite name.""",
        "summary": "Small, tight-knit survivors sustained by grit and an uncanny, silent luck.",
        "creature_type": "Humanoid",
        "size": "Small",
        "speed": "30ft",
        "features": [
            {
                "id": "halfling_brave",
                "name": "Brave",
                "summary": "Advantage on saves against being Frightened.",
                "description": "You have Advantage on saving throws you make to avoid or end the Frightened condition."
            },
            {
                "id": "halfling_nimbleness",
                "name": "Halfling Nimbleness",
                "summary": "Move through the space of larger creatures.",
                "description": "You can move through the space of any creature that is a size larger than you, but you can't stop in the same space."
            },
            {
                "id": "halfling_luck",
                "name": "Luck",
                "summary": "Reroll 1s on d20 tests.",
                "description": "When you roll a 1 on the d20 of a D20 Test, you can reroll the die, and you must use the new roll."
            },
            {
                "id": "halfling_naturally_stealthy",
                "name": "Naturally Stealthy",
                "summary": "Hide behind larger creatures.",
                "description": "You can take the Hide action even when you are obscured only by a creature that is at least one size larger than you."
            }
        ]
    },
    {
        "name": "Human",
        "description": """Humans are the restless flame of Kharoth. Short-lived and stubborn, they chase meaning
            through conquest, invention, and legacy, refusing to accept the silence of the Gods as final.
            In every shattered land and forgotten ruin, you will find humans building, rebuilding, and breaking again
            in pursuit of something more. They are not defined by blood or tradition, but by choice.
            Among all mortal kin, they burn brightest when the world is darkest, even when no one asks them to.""",
        "summary": "Restless and versatile, humans shape their own fate through choice and ambition.",
        "creature_type": "Humanoid",
        "size": ["Medium", "Small"],
        "speed": "30ft",
        "features": [
            {
                "id": "human_resourceful",
                "name": "Resourceful",
                "summary": "Gain Heroic Inspiration on a long rest.",
                "description": "You gain Heroic Inspiration whenever you finish a Long Rest."
            },
            {
                "id": "human_skillful",
                "name": "Skillful",
                "summary": "Gain one skill proficiency.",
                "description": "You gain proficiency in one skill of your choice."
            },
            {
                "id": "human_versatile",
                "name": "Versatile",
                "summary": "Gain one Origin feat.",
                "description": "You gain an Origin feat of your choice."
            }
        ]
    },
    {
        "name": "Orc",
        "description": """Orcs are shaped by histories that no longer serve them, forged in cycles of violence
            they did not begin but refuse to repeat. Their strength is real, but so is their restraint.
            In the eyes of others they are fury made flesh, but within, they carry stories of discipline, grif,
            and endurance. Many walk the world not in search of battle, but of purpose beyond blood. When orcs fight,
            it is with clarity. When they endure, it is with the weight of everything they were told they had to be.""",
        "summary": "Strength tempered by restraint, seeking purpose and endurance in a harsh world.",
        "creature_type": "Humanoid",
        "size": "Medium",
        "speed": "30ft",
        "features": [
            {
                "id": "orc_adrenaline_rush",
                "name": "Adrenaline Rush",
                "summary": "Bonus Action Dash + Temporary HP.",
                "description": "You can take the Dash action as a Bonus Action. When you do so, you gain a number of Temporary Hit Points equal to your Proficiency Bonus.",
                "details": {
                    "Action": "Bonus Action",
                    "Temp HP": "PB",
                    "Usage": "PB / Short or Long Rest"
                }
            },
            {
                "id": "orc_darkvision",
                "name": "Darkvision",
                "summary": "See in the dark up to 120ft.",
                "description": "You have Darkvision with a range of 120ft."
            },
            {
                "id": "orc_relentless_endurance",
                "name": "Relentless Endurance",
                "summary": "Drop to 1 HP instead of 0 once per day.",
                "description": "When you are reduced to 0 Hit Points but not killed outright, you can drop to 1 Hit Point instead.",
                "details": {
                    "Usage": "1 / Long Rest"
                }
            }
        ]
    },
    {
        "name": "Tiefling",
        "description": """Tieflings are the children of consequences. Their forms bear the marks of ancient pacts,
            forgotten sins, or unknowable powers that once touched their bloodline. Yet they are not bound by that past.
            In the eyes of the world, they are often feared or judged before they speak. So Tieflings learn early how to
            shape perception, how to wield fear, or how to walk alone. Many seek the Trials not to escape their legacy,
            but to forge one stronger. One chosen, not inherited.
            Abyssal. Abyssal Tieflings bear the scars of the abyss not just in form, but in will. Marked by shadow
            and flame, they carry a fierce, volatile power that hums beneath their skin. Feared even among their kin,
            they walk a razor's edge between destruction and control, seeking to master the chaos within or be consumed by it.
            Chthonic. Chthonic Tieflings are shadows born of earth's forgotten depths, carrying ancient whispers beneath their skin.
            Their connection to the subterrean realms grants them eerie calm and unsettling resilience, as if the bones of the world
            pulse through their veins. They move quietly between worlds, drawing strength from darkness without surrendering
            to it, ever watchful for the legacy they will carve from the void.
            Infernal. Infernal Tieflings carry the blaze of a harsh legacy, embers of ancient power that burn within their blood.
            Their presence commands attention, a living reminder of the price of ambition and the fire that fuesl it.
            Fierce and proud, they walk the line between destruction and discipline, shaping their fate through will
            as much""",
        "summary": "Individuals marked by otherworldly legacies, forging their own paths through will and pride.",
        "variations": ["Abyssal", "Chthonic", "Infernal"],
        "creature_type": "Humanoid",
        "size": ["Medium", "Small"],
        "speed": "30ft",
        "features": [
            {
                "id": "tiefling_darkvision",
                "name": "Darkvision",
                "summary": "See in the dark up to 60ft.",
                "description": "You have Darkvision with a range of 60ft."
            },
            {
                "id": "tiefling_otherworldly_presence",
                "name": "Otherworldly Presence",
                "summary": "You know the Thaumaturgy cantrip.",
                "description": "You know the Thaumaturgy cantrip. When you cast it with this trait, the spell uses the same spellcasting ability you use for your Fiendish Legacy trait."
            },
            {
                "id": "tiefling_fiendish_legacy",
                "name": "Fiendish Legacy",
                "summary": "Gain spells and resistance based on your legacy (Abyssal, Chthonic, or Infernal).",
                "description": "You are the recipient of a legacy that grants you supernatural abilities. You gain benefits at levels 1, 3, and 5. Intelligence, Wisdom, or Charisma is your spellcasting ability for the spells you cast with this trait.",
                "details": {
                    "Options": [
                        {
                            "name": "Abyssal",
                            "description": "Resistance to Poison damage. Level 1: Poison Spray cantrip. Level 3: Ray of Sickness. Level 5: Hold Person."
                        },
                        {
                            "name": "Chthonic",
                            "description": "Resistance to Necrotic damage. Level 1: Chill Touch cantrip. Level 3: False Life. Level 5: Ray of Enfeeblement."
                        },
                        {
                            "name": "Infernal",
                            "description": "Resistance to Fire damage. Level 1: Fire Bolt cantrip. Level 3: Hellish Rebuke. Level 5: Darkness."
                        }
                    ]
                }
            }
        ]
    },
]