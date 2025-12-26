SPECIES = [
    {
        "name": "Aasimar",
        "description": """Aasimar are mortals born with an echo of divine resonance within them.
            Not chosen by Gods—who grant no favors—but shaped by inner force, they reflect celestial
            power through sheer will. Their features hint at radiant potential: luminous eyes,
            glowing veins, halos of light. These signs begin faint, growing as the Aasimar learns to 
            waken their soul's brilliance. In Kharoth, they are not messengers of the divine—but mortals
            whose ambition burns bright enough to mimic it.""",
        "creature_type": "Humanoid",
        "size": ["Medium", "Small"],
        "speed": "30ft",
        "traits": [
            "Celestial Resistance. You have resistance to Necrotic damage and Radiant damage.",
            "Darkvision. You have Darkvision with a range of 60ft.",
            """Healing Hands. As a Magic Action, you touch a creature and roll a number of d4s
                equal to your Proficiency Bonus. The creature regains that many Hit Points.
                Once you use this trait, you can't use it again until you finish a Long Rest.""",
                "Light Bearer. You know the Light cantrip. Charisma is your spellcasting ability for it.",
            """Celestial Revelation. When you reach character level 3, you can transform as a
                Bonus Action using one of the options below (choose each time you transform).
                The transformation lasts 1 minute or until you end it (no action required).
                You regain this ability after a Long Rest.
                Once per turn during the transformation, when you deal damage to a target,
                you can deal extra damage equal to your Proficiency Bonus — Radiant or Necrotic
                depending on the form. The three forms are:
                Heavenly Wings: You gain a Fly speed equal to your walking speed.
                Inner Radiance: You emit bright light (10 ft) and dim light (10 ft), and
                creatures within 10 ft take Radiant damage equal to your Proficiency Bonus
                at the end of your turn.
                Necrotic Shroud: Flightless wings sprout, and creatures within 10 ft
                must make a Charisma save (DC 8 + Cha mod + Prof Bonus) or become Frightened
                until the end of your next turn."""
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
        "creature_type": "Humanoid",
        "size": "Medium",
        "speed": "30ft",
        "traits": [
            "As a Dragonborn, you have these special traits.",
            """Draconic Ancestry. Your lineage stems from a dragon progenitor. Choose the kind of dragon from the
                Draconic Ancestors list. Your choice affects your Breath Weapon and Damage Resistance traits as well
                as your appearance.
                Draconic Ancestors list:
                - Black: Acid Damage.
                - Blue: Lightning Damage.
                - Brass: Fire Damage.
                - Bronze: Lightning Damage.
                - Copper: Acid Damage.
                - Gold: Fire Damage.
                - Green: Poison Damage.
                - Red: Fire Damage.
                - Silver: Cold Damage.
                - White: Cold Damage.""",
            """Breath Weapon. When you take the Attack action on your turn, you can replace one of your attacks with
                an exhalation of magical energy in either a 15ft Cone or a 30ft Line that is 5ft wide
                (choose the shape each time). Each creature in that area must make a Dexterity saving throw
                (DC 8 plus your Constitution modifier and Proficiency Bonus). On a failed save, a creature takes 1d10
                damage of the type determined by your Draconic Acenstry trait. On a successful save, a creature takes
                half as much damage. This damage increases by 1d10 when you reach character levels 5 (2d10), 11 (3d10),
                and 17 (4d10).
                You can use this Breath Weapon a number of times equal to your Proficiency Bonus, and you regain all
                expanded uses when you finish a Long Rest.""",
            """Damage Resistance. You have Resistance to the damage type determined by your Draconic Ancenstry trait.""",
            """Darkvision. You have Darkvision with a range of 60ft.""",
            """Draconic Flight. When you reach character level 5, you can channel draconic magic to give yourself
                temporary flight. As a Bonus Action, you sprout spectral wings on your back that last for 10 minutes
                or until you retract the wings (no action required) or have the Incapacitated condition. During that
                time, you have a Fly Speed equal to your Speed. Your wings appear to be made of the same energy as your
                Breath Weapon. Once you use this trait, you can't use it again until you finish a Long Rest.""",
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
        "creature_type": "Humanoid",
        "size": "Medium",
        "speed": "30ft",
        "traits": [
            "As a Dwarf, you have these special traits.",
            """Darkvision. You have Darkvision with a range of 120ft.""",
            """Dwarven Resilience. You have Resistance to Poison damage. You also have Advantage on saving throws you make
                to avoid or end the Poisoned condition.""",
            """Dwarven Toughness. Your Hit Point maximum increases by 1, and it increases by 1 again whenever you
                gain a level.""",
            """Stonecunning. As a Bonus Action, you gain Tremorsense with a range of 60ft for 10 minutes. You must be on
                a stone surface or touching a stone surface to use this Tremorsense. The stone can be natural or worked.
                You can use this Bonus Action a number of times equal to your Proficiency Bonus, and you regain all
                expended uses when you finish a Long Rest.""",
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
        "variations": ["Drow", "High Elves", "Wood Elves"],
        "creature_type": "Humanoid",
        "size": "Medium",
        "speed": "30ft",
        "traits": [
            "As an Elf, you have these special traits.",
            """Darkvision. You have Darkvision with a range of 60ft.""",
            """Elven Lineage. You are part of a lineage that grants you supernatural abilities. Choose a lineage
                from the Elven Lineages list. You gain the level 1 benefit of that lineage.
                When you reach character levels 3 and 5, you learn a higher-level spell, as shown on the list.
                You always have that spell prepared. You can cast it once without a spell slot, and you regain
                ability to cast it in that way when you finish a Long Rest. You can also cast the spell using any
                spell slots you have of the appropriate level.
                Intelligence, Wisdom, or Charisma is your spellcasting ability for the spells you cast with this trait
                (choose the ability when you select the lineage).""",
            """Elven Lineages.
                - Drow
                    Level 1. The range of your Darkvision increases to 120ft. You also know the Dancing Lights cantrip.
                    Level 3. Faerie Fire.
                    Level 5. Darkness.
                - High Elf
                    Level 1. You know the Prestidigitation cantrip. Whenever you finish a Long Rest, you can replace
                    that cantrip with a different cantrip from the Wizard spell list.
                    Level 3. Detect Magic.
                    Level 5. Misty Step.
                - Wood Elf
                    Level 1. Your Speed increases to 35ft. You also know the Druidcraft cantrip.
                    Level 3. Longstrider.
                    Level 5. Pass Without Trace.""",
            """Fey Ancestry. You have Advantage on saving throws you make to avoid or end the Charmed condition.""",
            """Keen Senses. You have proficiency in the Insight, Perception, or Survival skill.""",
            """Trance. You don't need to sleep, and magic can't put you to sleep. You can finish a Long Rest in 4
                hours if you spend those hours in a trancelike meditation, during which you retain consciousness.""",
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
        "variations": ["Forest", "Rock"],
        "creature_type": "Humanoid",
        "size": "Small",
        "speed": "30ft",
        "traits": [
            "As a Gnome, you have these special traits.",
            """Darkvision. You have Darkvision with a range oof 60ft.""",
            """Gnomish Cunning. You have Advantage on Intelligence, Wisdom, and Charisma saving throws.""",
            """Gnomish Lineage. You are part of a lineage that grants you supernatural abilities. Choose one
                of the following options; whichever one you choose, Intelligence, Wisdom, or Charisma is your
                spellcasting ability for the spells you castt with this trait (choose the ability when you select the lineage):""",
            """Forest Gnome. You know the Minor Illusion cantrip. You also always have the Speak with Animals
                spell prepared. You can cast it without a spell slot a number of times equal to your Proficiency Bonus,
                and you regain all expended uses when you finish a Long Rest. You can also use any spell slots
                you have to cast the spell.""",
            """Rock Gnome. You know the Mending and Prestidigitation cantrips. In addition, you can spend 10 minutes
                casting Prestidigitation to create a Tiny clockwork device (AC 5, 1HP), such as a toy, fire starter,
                or music box. When you create the device, you determine its function by choosing one effect from
                Prestidigitation; the device produces that effect whenever you or another creature takes a Bonus Action
                to activate it with a touch. If the chosen effect has options within it, you choose one of those options
                for the device when you create it. For example, if you choose the spell's ignite-extinguish effect,
                you determine whether the device ignites or extinguishes fire; the device doesn't do both. You can have
                three such devices in existence at a time, and each falls apart 8 hours after its creation or when
                you dismantle it with a touch as a Utilize action.""",
        ]
    },
    {
        "name": "Goliath",
        "description": """Goliaths are living echoes of a forgotten age, when stone itself still moved and warred beneath
            the sky. Their bodies carry the memory of that ancient struggle, marked by frost, shaped by impact, and tempered
            in silence. To them, glory is not a prize, but a burden earned through pain, ritual, and self-mastery.
            In a world obsessed with ascent, Goliaths walk a different path: one carved not upward, but inward, toward
            a greatness that neither Gods nor mortals can define for them.""",
        "variations": ["Cloud", "Fire", "Frost", "Hill", "Stone", "Storm"],
        "creature_type": "Humanoid",
        "size": "Medium",
        "speed": "35ft",
        "traits": [
            "As a Goliath, you have these special traits",
            """Giant Ancestry. You are descended from Giants. Choose one of the following benefits, a supernatural
                boon from your ancestry; you can use the chosen benefit a number of times equal to your
                Proficiency Bonus, and you regain all expended uses when you finish a Long Rest:
                    - Cloud's Jaunt (Cloud Giant). As a Bonus Action, you magically teleport up to 30ft to an
                    unoccupied space you can see.
                    - Fire's Burn (Fire Giant). When you hit a target with an attack roll and deal damage to it,
                    you can also deal 1d10 Fire damage to that target.
                    - Frost's Chill (Frost Giant). When you hit a target with an attack roll and deal damage to it,
                    you can also deal 1d6 Cold damage to that target and reduce its Speed by 10ft until the start
                    of your next turn.
                    - Hill's Tumble (Hill Giant). When you hit a Large or smaller creature with an attack roll and deal
                    damage to it, you can give that target the Prone condition.
                    - Stone's Endurance (Stone Giant). When you take damage, you can take a Reaction to roll 1d12.
                    Add your Constitution modifier to the number rolled and reduce the damage by that total.
                    - Storm's Thunder (Storm Giant). When you take damage from a creature within 60ft of you,
                    you can take a Reaction to deal 1d8 Thunder damage to that creature.""",
                """Large Form. Starting at character level 5, you can change your size to Large as a Bonus Action if
                    you're in a big enough space. This transformation lasts for 10 minutes or until you end it
                    (no action required). For that duration, you have Advantage on Strength checks, and your Speed
                    increases by 10ft. Once you use this trait, you can't use it again until you finish a Long Rest.""",
                """Powerful Build. You have Advantage on any saving throw you make to end the Grappled condition.
                    You also count as one size larger when determining your carrying capacity.""",
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
        "creature_type": "Humanoid",
        "size": "Small",
        "speed": "30ft",
        "traits": [
            "As a Halfling, you have these special traits.",
            """Brave. You have Advantage on saving throws you make to avoid or end the Frightened condition.""",
            """Halfling Nimbleness. You can move through the space of any creature that is a size larger than you,
                but you can't stop in the same space.""",
            """Luck. When you roll a 1 on the d20 of a D20 Test, you can reroll the die, and you must use the new roll.""",
            """Naturally Stealthy. You can take the Hide action even when you are obscured only by a creature
                that is at least one size larger than you.""",
        ]
    },
    {
        "name": "Human",
        "description": """Humans are the restless flame of Kharoth. Short-lived and stubborn, they chase meaning
            through conquest, invention, and legacy, refusing to accept the silence of the Gods as final.
            In every shattered land and forgotten ruin, you will find humans building, rebuilding, and breaking again
            in pursuit of something more. They are not defined by blood or tradition, but by choice.
            Among all mortal kin, they burn brightest when the world is darkest, even when no one asks them to.""",
        "creature_type": "Humanoid",
        "size": ["Medium", "Small"],
        "speed": "30ft",
        "traits": [
            "As a Human, you have these special traits.",
            """Resourceful. You gain Heroic Inspiration whenever you finish a Long Rest.""",
            """Skillful. You gain proficiency in one skill of your choice.""",
            """Versatile. You gain an Origin feat of your choice.""",
        ]
    },
    {
        "name": "Orc",
        "description": """Orcs are shaped by histories that no longer serve them, forged in cycles of violence
            they did not begin but refuse to repeat. Their strength is real, but so is their restraint.
            In the eyes of others they are fury made flesh, but within, they carry stories of discipline, grif,
            and endurance. Many walk the world not in search of battle, but of purpose beyond blood. When orcs fight,
            it is with clarity. When they endure, it is with the weight of everything they were told they had to be.""",
        "creature_type": "Humanoid",
        "size": "Medium",
        "speed": "30ft",
        "traits": [
            "As an Orc, you have these special traits.",
            """Adrenaline Rush. You can take the Dash action as a Bonus Action. When you do so, you gain a number
                of Temporary Hit Points equal to your Proficiency Bonus.
                You can use this trait a number of times equal to your Proficiency Bonus, and you regain all
                expended uses when you finish a Short or Long Rest.""",
            """Darkvision. You have Darkvision with a range of 120ft.""",
            """Relentless Endurance. When you are reduced to 0 Hit Points but not killed outright, you can drop to
                1 Hit Point instead. Once you use this trait, you can't do so again until you finish a Long Rest.""",
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
        "creature_type": "Humanoid",
        "size": "Medium",
        "speed": "30ft",
        "traits": [
            "As an Orc, you have these special traits.",
            """Adrenaline Rush. You can take the Dash action as a Bonus Action. When you do so, you gain a number
                of Temporary Hit Points equal to your Proficiency Bonus.
                You can use this trait a number of times equal to your Proficiency Bonus, and you regain all
                expended uses when you finish a Short or Long Rest.""",
            """Darkvision. You have Darkvision with a range of 120ft.""",
            """Relentless Endurance. When you are reduced to 0 Hit Points but not killed outright, you can drop to
                1 Hit Point instead. Once you use this trait, you can't do so again until you finish a Long Rest.""",
        ]
    },
]