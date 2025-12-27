WILD_SURGES = {
    "1": {
        "name": "Wild Surge Of Abyssal Legion",
        "description": """Wild Magic tears open rifts to the shadowy depths beyond reality, summoning lesser fiends to the battlefield.
            On Initiative count 20 each Round, PB - 1 Quasits spawn in a random location within the map, all with an Initiative score of 10.
            On their turn, they attack the nearest creature indiscriminately but will not attack each other.""",
        "echo of ascendance": """Infernal Authority.
            The chaotic power of the Surge grants you authority over summoned fiends. For the rest of the current Encounter:
            Your teeth lengthen into fangs, your eyes glow a deep violet, and your nails sharpen into claws. Your Unarmed Strikes deal 1d6 Slashing damage.
            As a Bonus Action, you can designate one creature you can see within 120ft of you as a target.
            All fiends of CR 1 or below within that range must use their next turn to move as close to the target as possible and attack it.""",
        "echo of ruin": """Abyssal Bond.
            The surging Wild Magic infuses you with infernal resilience. For the rest of the current Encounter:
            Fiends of CR 1 or below have Disadvantage on Attack Rolls against you.
            For as long as a fiend is within 120ft of you, you share that creature's damage Resistances and Immunities.""",
        "worldshift trait": """Demonic Frenzy.
            A creature with this Trait is driven to relentless violence by the chaotic influence of the abyss. For the rest of the current Encounter, it gains the following features:
            After it reduces a creature to 0 Hit Points, it can use its Reaction to move up to its movement Speed and make a single melee attack.
            Each time it reduces a fiend to 0 Hit Points, it gains +1 to all Attack Rolls, Ability Checks and Saving Throws.
            It can gain this benefit a number of times equal to its PB."""
    },
    "2": {
        "name": "Wild Surge Of Arcane Vitality",
        "description": """The battlefield hums as raw magic pulses with living energy, twisting and surging unpredictably.
            The first time a creature casts a leveled spell on each turn, that spell is treated as if it were cast using a spell slot 2 levels higher than the one expended.
            Additionally, if a creature takes the Attack action, it can use a Bonus Action on that turn to cast one of the following Cantrips: Minor Illusion, Poison Spray,
            Ray Of Frost, Spare The Dying. If a Cantrip cast using this Wild Surge requires a Saving Throw, the DC is 12 + PB.""",
        "echo of ascendance": """Spellbound Strike.
            You channel the wild pulse of living magic into every strike. For the rest of the current Encounter:
            The first time you hit a creature with a weapon attack each turn, you deal an additional PBd4 damage of a type you choose from among Cold, Fire or Lightning.
            Your Spell Save DC increases by 1.
            You have a +1 to Spell Attack Rolls.""",
        "echo of ruin": """Guardian Ward.
            The chaotic magic forms a protective aura around you. For the rest of the current Encounter:
            You Resist damage from spells.
            You have Advantage on Saving Throws against spells.
            You can cast the Shield spell without a spell slot or components.""",
        "worldshift trait": """Arcane Tempest.
            A creature with this Trait is infused with living, explosive magical energy. For the rest of the current Encounter, it gains the following features:
            Two PB - 1 level spell slots, each of which can be expended to cast any spell from the Wizard spell list of that level or below.
            If the spell cast forces a Saving Throw, the save DC is 12 + PB. If the spell requires an Attack Roll, it is 14 + PB to hit.
            After it takes damage from a spell, it gains Temporary Hit Points equal to the level of the spell that damaged it."""
    },
    "3": {
        "name": "Wild Surge Of Ascendant Convergence",
        "description": """The crackling Wild Magic of ultimate potential surges across the battlefield, amplifying the power of all who embrace it.
            At the start of the Encounter, each player character chooses Echo Of Ascendance or Echo Of Ruin. The GM then generates a new Wild Surge,
            which can be this Surge again. The new Surge immediately takes effect, with each Ascendant gaining the chosen boon
            (Echo Of Ascendance or Echo Of Ruin) from that Surge, and one enemy creature with the highest CR receiving the Worldshift Trait from that Surge.
            If this Surge triggers itself, the Wild Magic erupts violently into the air, exploding with light, smoke, and arcane energy.
            No further Wild Surge occurs during this Encounter, and the players gain the following Feat:""",
        "echo of ascendance": """Boon Of Wild Magic.
            A spark of primordial Wild Magic has embedded itself within your soul:
            Increase one Ability Score of your choice by 1, to a maximum of 20.
            Once per Long Rest, when you fail a d20 test, you can treat the result of the d20 as a natural 1.
            Once per Long Rest, when you succeed on a d20 test, you can treat the result on the d20 as a natural 20. 
            Once per Run, when you trigger Echo Of Ascendance or Echo Of Ruin, you may forgo that boon to instead gain the Worldshift Trait
            of that Wild Surge for the remainder of the Encounter."""
    },
    "4": {
        "name": "Wild Surge Of Cataclysm",
        "description": """A choking pressure sweeps across the battlefield, as if reality itself momentarily forgets to sustain life.
            The air trembles, the ground pulses, and every beating heart feels the weight of imminent collapse.
            At the start of each creature's turn, they must succeed on a DC 8 + PB Constitution Saving Throw or fall to 1 Hit Point.""",
        "echo of ascendance": """Iron Will Awakening.
            A violent ripple of Nature surges through you, sharpening your instincts and hardening your resolve. For the rest of the current Encounter:
            You can choose to fail Constitution Saving Throws.
            While you have exactly 1 Hit Point, any Attack Roll you make that hits a creature is a Critical Hit.
            You are immune to the Frightened, Paralyzed and Stunned conditions.""",
        "echo of ruin": """Last Heartfire.
            In the face of annihilation, a spark of defiant spirit erupts within you, igniting a beacon of protection. For the rest of the current Encounter:
            If a creature within 30ft of you (including yourself) would fall to 0 Hit Points as a result of taking damage, you can use a reaction to envelope that creature
            with Wild Magic. The damage is reduced to 0 and that creature instead gains PBd12 Temporary Hit Points.""",
        "worldshift trait": """Cataclysm Bound.
            A creature warped by this Surge becomes a vessel of ruin, straddling the line between life and death.
            For the rest of the current Encounter, it gains the following features:
            While it has exactly 1 or 0 Hit Points, the creature is immune to damage, except Radiant damage and damage from Critical Hits.
            If it has 0 Hit Points, it does not die.
            At the end of its turn, if the creature has 0 Hit Points and has not dealt damage to a creature since the start of its last turn, it dies."""
    },
    "5": {
        "name": "Wild Surge Of Chance",
        "description": """Chaotic Wild Magic flows unpredictably, tempting those bold enough to test fate.
            Whenever a creature makes an Attack Roll, it can choose to roll at Disadvantage (if not already at Disadvantage). If it hits, it can choose one of the following boons:
            Its attack deals an additional 2 x PB damage.
            It gains 1d6 x PB Temporary Hit Points.
            It uses its Reaction to move up to 5 x PB feet without provoking Opportunity Attacks.""",
        "echo of ascendance": """Trickster's Edge.
            Mischievous Wild Magic bends luck in your favor. For the rest of the current Encounter:
            Once per turn, if you choose to roll at Disadvantage, you can choose to invoke this Surge before rolling the dice and take the higher result rather than the lower.
            When a creature makes an Attack Roll against you at Advantage, before it rolls you can use your Reaction to force that creature to take the lower
            of the two dice as its result rather than the higher.""",
        "echo of ruin": """Lucky Shield.
            Wild Magic protects you when chance turns against you. For the rest of the current Encounter:
            If you miss an Attack Roll made at Disadvantage, you gain a +PB bonus to your next Attack Roll that isn't made at Disadvantage.
            If a creature hits you with an Attack Roll made at Disadvantage, you can use your Reaction to interfere with its boon.
            You, rather than it, choose the effect it gains from the Surge.""",
        "worldshift trait": """Manipulator Of Fate.
            A creature with this Trait is touched by supernatural fortune. For the rest of the current Encounter, it gains the following features:
            When it makes an Attack Roll at Disadvantage, it gains a +PB bonus to hit.
            When it hits a creature with an Attack Roll made at Disadvantage, it can choose two boons from this Surge rather than only one."""
    },
    "6": {
        "name": "Wild Surge Of Clockwork Advancement",
        "description": """A Surge of mechanical Wild Magic tears through the battlefield, twisting flesh into gleaming metal and infusing beings with precise, whirring machinery.
            All creatures become Constructs and Resist Bludgeoning, Slashing and Piercing damage.""",
        "echo of ascendance": """Overdrive.
            Your newfound mechanical form allows you to push your systems beyond their normal limits. For the rest of the current Encounter:
            Your movement Speed increases by 10ft.
            You can take an additional action on your turn. If you do, at the end of that turn you must succeed on a DC 12 + PB Constitution Saving Throw
            or have the Stunned condition until the end of your next turn.""",
        "echo of ruin": """Steelframe.
            The Wild Magic reinforces your body with impervious metal. For the rest of the current Encounter:
            Until the end of your next turn, you gain a +PB bonus to your AC and Saving Throws.
            Once per turn, other Constructs take 3 x PB Lightning damage when they enter a space within 10ft of you.""",
        "worldshift trait": """Automaton Berserker.
            A creature with this Trait becomes a relentless mechanical force. For the rest of the current Encounter, it gains the following features:
            Immune to Psychic damage.
            Vulnerable to Lightning damage.
            At the start of its turn, it can choose to take two actions that turn. If it does, both of those actions must be the Attack action, and its movement Speed
            falls to 0 until the end of its next turn. It cannot use this ability if its movement Speed is 0."""
    },
    "7": {
        "name": "Wild Surge Of Colossal Might",
        "description": """Wild Magic surges across the battlefield, infusing creatures with the strength and stature of legendary titans.
            If there is room, creatures grow to Huge in size, their reach increases by 10ft, they have Advantage on Strength checks and Saving Throws
            and their Strength-based weapon attacks deal an additional 1d4 damage.""",
        "echo of ascendance": """Titan's Wrath.
            The chaotic power of Wild Magic channels the rage of colossal beings. For the rest of the current Encounter:
            Once per turn, when you damage a creature, you can choose to deal an additional PBd8 Fire damage to that target.
            You resist Fire damage.
            Creatures Grappled by you take 1d10 Fire damage at the start of each of their turns.""",
        "echo of ruin": """Frostbound Endurance.
            The Surge of Wild Magic fortifies your body with icy resilience. For the rest of the current Encounter:
            You resist Cold and Fire damage.
            Your AC increases by PB as a chilling vortex of ice and snow spirals around you.
            If a creature within 15ft of you targets you with a melee weapon attack, that creature cannot move until the start of its next turn
            as the icy vortex surrounding you briefly freezes it in place.""",
        "worldshift trait": """Earthen Bulwark.
            A creature with this Trait is imbued with the steadfast might of stone titans. For the rest of the current Encounter, it gains the following featuresr:
            Its size increases to maximum size for the space, up to Gargantuan.
            Its weapon attacks deal an additional 1d4 damage.
            It Resists Bludgeoning, Piercing and Slashing damage.
            As a Reaction when hit by an attack, it can gain a PB bonus to its AC until the end of the turn as its skin hardens to stone."""
    },
    "8": {
        "name": "Wild Surge Of Corrosive Mire",
        "description": """A sickly green vapor rises from cracks in the battlefield as bubbling acid seeps upward, hissing and devouring everything it touches.
            Stone softens, roots dissolve and the ground pulses with alchemical venom.
            Creatures that start their turn touching the ground or touch the ground during their turn take PBd4 Acid damage.""",
        "echo of ascendance": """Alchemic Edge.
            The Surge binds caustic energy to your strikes, coating your tools of battle in volatile runoff. For the rest of the current Encounter:
            As a Bonus Action, you can dip a weapon or Arcane Focus you carry into the acid on the ground. If you do, the next time you hit with that weapon or
            damage a creature with a spell, you deal an additional PBd8 Acid damage.""",
        "echo of ruin": """Vile Carapace.
            The corrosive tide refuses to harm you, instead knitting around your body as a protective second skin. For the rest of the current Encounter:
            Each time you would take Acid damage, you instead gain Temporary Hit Points equal to the damage dealt.""",
        "worldshift trait": """Caustic Frenzy.
            The creature's form spasms under the constant sting of dissolving ground, driving it into an unhinged state of pain-fueled aggression.
            For the rest of the current Encounter, it gains the following features:
            If it took Acid damage since the start of its last turn, the creature has Advantage on Attack Rolls and Strength, Dexterity and
            Constitution Saving Throws. It also scores a Critical Hit on an attack of 18-20.
            Attack Rolls made against it have Advantage."""
    },
    "9": {
        "name": "Wild Surge Of Dawning Brilliance",
        "description": """A flood of shimmering, blazing radiance washes over the battlefield, threading itself through air, stone and flesh.
            Shadows are erased, leaving nowhere to hide.
            All creatures shed Bright Light in a 10ft radius, have Disadvantage on Stealth checks and gain no benefit from being Invisible.
            This radiance overrides any Darkness, magical or otherwise.""",
        "echo of ascendance": """Luminary Blade.
            Light surges within you, sharpening conviction and exposing weaknesses in every foe. For the rest of the current Encounter:
            You cannot have Disadvantage on Attack Rolls or Saving Throws.
            Once per turn, when you damage a creature with an attack or spell, you can force it to make a DC12 + PB Charisma Saving Throw.
            On a failed save, the creature is subjected to the effects of the Faerie Fire spell. It can repeat its save at the end of each turn, ending the effect on a success.""",
        "echo of ruin": """Radiant Mender.
            Wild Magic condenses into a gentle, restoring glow that answers your touch. For the rest of the current Encounter:
            As a Bonus Action, you can place a hand on a willing creature and restore PBd4 Hit Points to that creature. If you restore a creature to full HP with this effect,
            you gain Heroic Inspiration.
            Any creature you heal with a spell, item or trait gains PB x 3 Temporary Hit Points.""",
        "worldshift trait": """Blinding Beacon.
            A creature marked by this Trait becomes a walking pillar of unbearable brilliance. For the rest of the current Encounter, it gains the following features:
            Its body radiates painful intensity. Creatures that start their turns within 10ft of it take PBd4 Radiant damage and are Blinded as long as they are within 10ft of it.
            It automatically fails any Stealth checks.
            It Resists Necrotic and Radiant damage."""
    },
    "10": {
        "name": "Wild Surge Of Dawnsworn Unity",
        "description": """A Surge of primal light, drawn from a realm where dawn never ends, floods the battlefield with uplifting brilliance.
        Its luminance strengthens comrades whose spirits are bound in shared purpose.
            Bright sunlight illuminates the entire battlefield, dispelling any area of darkness created by a spell of 8th level or below.
            Creatures bathed in this light gain a +2 bonus to their AC and +PB to all Ability Checks and Saving Throws as long as
            they can see an allied creature within 30ft of them.""",
        "echo of ascendance": """Gift Of The Dawnsworn.
            The first spark of an eternal sunrise fills your body, lifting you lightly from the earth. For the rest of the current Encounter:
            You have a 10ft Fly Speed, carried by drifting motes of light.
            Whenever you make an Attack Roll or a Saving Throw, you can roll a d4 and add the number rolled to your result.""",
        "echo of ruin": """Edict Of The Dawnsworn.
            The higher realm's command reverberates from within you, resonant and absolute. For the rest of the current Encounter:
            You radiate Dim golden Light in a 10ft radius.
            You can cast Command as a Bonus Action. Intelligence, Wisdom or Charisma is your spellcasting ability modifier (choose when you activate this Surge).""",
        "worldshift trait": """Ember-Veiled Soul.
            A creature shaped by this Trait carries the heart of a newborn sun beneath its skin, flickering with disciplined radiance.
            For the rest of the current Encounter, it gains the following features:
            Resistance to Necrotic damage.
            When a creature you can see within 30ft of you hits you with an Attack Roll, you retaliate with a searing bolt of radiant energy.
            That creature must succeed on a DC12 + PB Constitution Saving Throw or take PBd8 Radiant damage and be Blinded until the end of its next turn."""
    },
    "11": {
        "name": "Wild Surge Of Dimensional Incoherence",
        "description": """Chaotic spatial magic ripples outward, bending space and allowing creatures to instantaneously shift across the battlefield.
            All creatures can use a Bonus Action to teleport up to PB x 5ft to an unoccupied space they can see within range.""",
        "echo of ascendance": """Forced Shift.
            Your mastery of the flux lets you impose movement on others. For the rest of the current Encounter:
            You shimmer unpredictably, even when standing still.
            As a Bonus Action, you can teleport one creature within 5ft of you PB x 5ft to an unoccupied space you can see (including in the air).""",
        "echo of ruin": """Spacial Boon.
            Wild Magic of the planes infuses your teleportation with extra effects. For the rest of the current Encounter:
            Whenever you teleport, choose one of the following boons as you reappear:
            You immediately take the Dodge action.
            You immediately make one weapon attack.
            You regain 1d6 x PB Hit Points.""",
        "worldshift trait": """Warpbound Striker.
            A creature infused with this Trait becomes a living ripple in space. For the rest of the current Encounter, it gains the following features:
            When it takes the Attack action, it can teleport up to PB x 5ft immediately before making each Attack Roll.
            It has a cumulative +1 bonus to Attack and Damage Rolls for each time it has teleported that turn.
            Once per turn, when it casts a spell, target(s) of that spell must succeed on a DC12 + PB Charisma Saving Throw or be teleported PB x 5ft to an
            unoccupied space it can see (including in the air)."""
    },
    "12": {
        "name": "Wild Surge Of Draconic Awakening",
        "description": """Wild Magic surges with the raw might of dragons, filling the battlefield with draconic energy and loyal minions.
            On Initiative count 20 each Round, PB + 1 Kobolds appear in random, unoccupied spaces. They chant in unison but take no actions.
            If eight or more kobolds are chanting at the start of Initiative count 20, the chromatic dragon of the highest CR PB + 10 or less appears and
            attacks all creatures on the battlefield indiscriminately.""",
        "echo of ascendance": """Draconic Fury.
            The wild energy of dragons courses through you, empowering your attacks. For the rest of the current Encounter:
            If you damage a Kobold as a part of your action, you can take one additional action that turn.
            You have Advantage on Attack Rolls made against Kobolds.""",
        "echo of ruin": """Wings Of The Ancients.
            Draconic magic grants you physical and elemental enhancements. For the rest of the current Encounter:
            You grow a pair of spectral, draconic wings. You have a Fly Speed equal to your Walking Speed.
            At the start of your turn, choose one damage type from among Acid, Cold, Fire, Lightning or Poison. Until the start of your next turn, you Resist that damage type.""",
        "worldshift trait": """Draconic Commandments.
            A creature with this Trait channels the Surge's draconic energies and minions. For the rest of the current Encounter:
            While there are 2 or more Kobolds on the battlefield, it has a +PB bonus to Ability Checks.
            While there are 4 or more Kobolds on the battlefield, it has a +PB bonus to Attack Rolls.
            While there are 6 or more Kobolds on the battlefield, it has a +PB bonus to Saving Throws.
            While there are 8 or more Kobolds on the battlefield, it is Immune to Acid, Cold, Fire, Lighting and Poison damage, and it has a +PB bonus to AC."""
    },
    "13": {
        "name": "Wild Surge Of Echoing Chorus",
        "description": """A pulse of harmonic Wild Magic ripples through the battlefield, awakening every stone into rhythmic, synchronized motion.
        Pebbles vibrate like tuning forks, boulders sway in complex patterns, and the entire area becomes a living stage of quaking resonance.
            All creatures in the area are Deafened, and the ground becomes Difficult Terrain for any creature not proficient in Performance,
            since only those who can mirror the rhythm can move cleanly through it. Constructs must succeed on a Wisdom Saving Throw (DC 10)
            at the start of each of their turns or be compelled to spend their movement and action dancing uncontrollably until the start of their next turn.""",
        "echo of ascendance": """Maestro's Command.
            The resonant Wild Magic aligns with your pulse, granting you the authority to orchestrate the animated stonework. For the rest of the current Encounter:
            You can cast Animate Objects without a spell slot or components. When you cast it in this way, the maximum number of objects you can animate is equal to your PB,
            and they must be Tiny. Intelligence, Wisdom or Charisma is your spellcasting modifier for this spell (choose when you get this Surge).""",
        "echo of ruin": """Hidden In The Rhythm.
            You slip effortlessly into the shifting harmony, moving in lockstep with the living stones. For the rest of the current Encounter:
            You have Three-Quarter Cover.
            You ignore Difficult Terrain created by the stones.""",
        "worldshift trait": """Rhythmic Ascendant.
            A creature touched by this musical distortion becomes a whirling dancer empowered by resonant motion.
            For the rest of the current Encounter, it gains the following features:
            Its Speed increases by 10ft.
            It gains proficiency in Performance.
            It has Advantage on Performance checks and Dexterity Saving Throws.
            At the start of its turn, it gains Heroic Inspiration if it doesn't have it."""
    },
    "14": {
        "name": "Wild Surge Of Enchanted Mischief",
        "description": """Fey-infused Wild Magic spreads across the battlefield, altering size and perception in unpredictable ways.
            All creatures and their possessions become Tiny, imposing a cumulative -2 penalty to Strenght-based Damage Rolls for each size category lost.
            Damage cannot be reduced below 1. Tiny creatures also have Advantage on Dexterity Saving Throws, take no Falling Damage and their jump distance is tripled.""",
        "echo of ascendance": """Fantasia Trickery.
            The mischievous power of the fey sharpens your cunning. For the rest of the current Encounter:
            You can add your Intelligence, Wisdom or Charisma modifier to your Attack Rolls and Ability Checks (choose when you active this Surge).
            Once per turn, after you damage a creature with an attack or spell, you can force the target to make a DC12 + PB Wisdom Saving Throw.
            On a failed save, that creature is Charmed for the rest of the current Encounter or until it takes damage. A Charmed creature can repeat this
            save at the end of each of its turns, ending the effect on a success.""",
        "echo of ruin": """Petite Strategist.
            Your reduced form grants unexpected advantages. For the rest of the current Encounter:
            You have a +PB bonus to your AC.
            You can take the Dash, Disengage, Dodge or Hide action as a Bonus Action.
            When hit by a weapon attack, you can choose to have that attack push you up to 30ft in a direction you choose. This movement does not provoke Opportunity Attacks.""",
        "worldshift trait": """Towering Bastion.
            A creature with this Trait is immune to the size-altering effects of the Surge. For the rest of the current Encounter, it gains the following features:
            Its size cannot be reduced.
            It has Advantage on melee Attack Rolls against creatures smaller than it.
            When it deals damage to a creature that is two or more sizes smaller than it with a weapon attack, that creature falls Prone."""
    },
    "15": {
        "name": "Wild Surge Of Entropic Decay",
        "description": """A thin shimmer of rot-laced air spreads over the battlefield like invisible mold, gnawing at strength, clarity, and resolve.
            Every motion feels heavier, every breath slightly spoiled.
            Whenever a non-undead creature makes an Attack Roll, Ability Check or Saving Throw, it rolls 1d4 and subtracts the number rolled from their result.""",
        "echo of ascendance": """Graveborne Might.
            A slow-burning necrotic current coils through your frame, sharpening every attack with the hunger of decay. For the rest of the current Encounter:
            Whenever you deal damage to a creature that doesn't have all of its Hit Points, that creature takes an additional PB x 2 Necrotic damage that ignore
            Resistance and you gain Temporary Hit Points equal to the Necrotic damage dealt by this Echo.""",
        "echo of ruin": """Veil Of Withering Night.
            A mantle of necrotic entropy clings to your body, drinking in force and fear alike. For the rest of the current Encounter:
            You gain Resistance to Cold, Necrotic, Poison, Psychic damage from creatures that do not have all their Hit Points.
            The first time each round you take damage, reduce that damage by PB x 2.
            Any creature that hits you with a melee attack takes PB Necrotic damage.""",
        "worldshift trait": """Blightforged Avatar.
            Rot claims the creature entirely, stripping away vitality and leaving a rigid vessel animated by corrupted Wild Magic.
            For the rest of the current Encounter, it gains the following features:
            The creature type is Undead.
            Resistance to Cold and Necrotic damage.
            Immunity to the Exhausted, Frightened and Poisoned condition.
            Resistance to Bludgeoning, Piercing and Slashing damage from weapons."""
    },
    "16": {
        "name": "Wild Surge Of Fractured Pandemonium",
        "description": """Nature convulses and splinters, as if every law of magic momentarily loses its grip. Threads of raw power lash across the battlefield,
            rewriting reality with each pulse.
            On Initiative count 20 each Round, roll 1d4. On a 3 or 4, generate a random Wild Surge. Its effects last for the remainder of the Encounter.
            If an Ascendant triggers an Echo Of Ascendance or an Echo Of Ruin while multiple Surges are active, they gain the effects tied to the most recently
            generated Wild Surge.""",
        "echo of ascendance": """Pandemonium Channeler.
            You briefly become a living conduit of fractured reality. Roll 1d6: You immediately cast one of the following spells without components
            and even if you couldn't cast spells, depending on the number rolled:
            1d6
            1 - Power Word Kill
            2 - Mass Heal
            3 - Shapechange
            4 - Foresight
            5 - Time Stop
            6 - Meteor Swarm""",
        "echo of ruin": """Chaotic Resonance.
            The discordant hum of broken magic settles over you like a shifting mantle of protection. You gain a bonus to your AC and Saving Throws equal to
            twice the number of Wild Surges currently active from this effect.""",
        "worldshift trait": """Pandemonium Overload.
            A creature warped by this Surge becomes a volatile battery of unstable power. For the rest of the current Encounter, it gains the following features:
            Whenever a new Wild Surge is generated by this Surge, the creature may immediately gain the Worldshift Trait associated with that Surge.
            These Traits stack.
            Each time the creature gains a Trait beyond its first, magical instability lashes out, dealing PBd12 damage of a random damage type to the creature."""
    },
    "17": {
        "name": "Wild Surge Of Gale Dominion",
        "description": """A violent storm tears across the battlefield, hurling creatures and debris with unrelenting force.
            The GM rolls 1d4 for each creature to determine the direction of the wind: 1. North, 2. East, 3. South, 4. West. On Initiative count 20,
            all creatures must succeed on a Strength Saving Throw or be pushed 5 x PB ft in the chosen direction the wind blows for each creature.
            Airborne creatures make this Saving Throw at Disadvantage. If a creature is pushed into another creature or object, it stops moving and both take
            PBd4 Bludgeoning damage.""",
        "echo of ascendance": """Skybound.
            The power of Wild Magic lifts you above the fury of the wind. For the rest of the current Encounter:
            You have a Fly Speed equal to twice your Walking Speed.
            Your movement doesn't provoke Opportunity Attacks.
            You automatically succeed on Saving Throws to avoid being moved against your will by wind.""",
        "echo of ruin": """Earthen Anchor.
            Wild Magic roots you against the storm and fortifies your resolve. For the rest of the current Encounter:
            You cannot be moved or knocked Prone against your will.
            You gain Tremorsense out to 30ft.
            Attack Rolls against you cannot be made with Advantage.""",
        "worldshift trait": """Tempest Overlord.
            A creature with this Trait becomes one with the merciless hurricane. For the rest of the current Encounter, it gains the following features:
            It automatically succeeds on Saving Throws to avoid being moved against its will by the wind.
            It has a Fly Speed equal to Walking Speed.
            While airborne, the creature has Advantage on Attack Rolls against non-airborne creatures.
            It can use its Reaction to make a single melee weapon attack against any creature that leaves its reach, even if the creature leaves unwillingly."""
    },
    "18": {
        "name": "Wild Surge Of Gluttonous Delight",
        "description": """A strange, chaotic essence of indulgence saturates the battlefield. Magical, malleable sustenance covers the ground, turning it springy and fragrant.
            Creatures can use a Bonus Action to consume a handful of this magical sustenance, gaining PBd4 Temporary Hit Points as long as they are not Poisoned.
            Each additional use of this Bonus Action requires a DC 5 + PB Constitution Saving Throw or the creature becomes Poisoned for the rest of the current Encounter.
            The DC increases by 1 for that creature each success, and resets on a failure. A creature Poisoned by this effect can repeat the saving throw at the end of
            each of its turns.""",
        "echo of ascendance": """Feast-Fueled Vigor.
            Empowered by chaotic indulgence, for the rest of the current Encounter:
            You can take an additional Bonus Action on each turn if you use the first to consume the magical sustenance.
            You have Advantage on Constitution Saving Throws to avoid or end the Poisoned condition.""",
        "echo of ruin": """Banquet's Boon.
            Joy and fullness empower you in unexpected ways. For the rest of the current Encounter:
            You have Advantage on Charisma (Persuasion and Performance) checks to influence others.
            Once per turn, when a creature is about to make an Attack Roll against you, you can use your Reaction to attempt to sway them.
            Make a contested Persuasion or Performance check against the enemy's Insight. On a success, the creature either wastes its attack or attacks a different
            target within range. If both you and the creature have consumed the magical sustenance during this Encounter, add +PB to this check.""",
        "worldshift trait": """Gluttonous Frenzy.
            A creature imbued with this Trait is overtaken by frenzied delight. For the rest of the current Encounter, it gains the following features:
            Any Temporary Hit Points gained from consuming the magical sustenance are tripled.
            It has Advantage on Constitution Saving Throws to avoid the Poisoned condition.
            The creature more easily bonds with other indulgent creatures. If a creature that has consumed the magical sustenance during
            the current Encounter attempts to use Banquet's Boon on this creature, and it also consumed the sustenance this Encounter, the creature has Disadvantage on its
            Insight check."""
    },
    "19": {
        "name": "Wild Surge Of Gravitic Collapse",
        "description": """A crushing pulse of warped gravity sweeps across the battlefield, forcing all things toward the ground. Movement becomes heavy and
            labored as the air itself grows impossibly dense.
            Creatures cannot jump or fly, and at the end of each turn, creatures with a Strength score of 19 or lower fall Prone.""",
        "echo of ascendance": """Titanborn Pulse.
            Wild energy chooses you as its anchor point, swelling your frame instead of crushing it. For the rest of the current Encounter:
            If your size is Medium or smaller, your size becomes Large if there is room.
            Your Strength score increases to 21.
            Your reach increases by 5ft.
            Your Unarmed Strikes deal 1d6 damage.""",
        "echo of ruin": """Burrower's Cunning.
            While gravity grinds others into the dust, you learn to move through it. For the rest of the current Encounter:
            While Prone, you have a Burrowing Speed equal to your Walking Speed.""",
        "worldshift trait": """Gravity Predator.
            A creature shaped by this surge learns to exploit anything forced to the ground. For the rest of the current Encounter, it gains the following features:
            Strength score increases to 20 if it is lower than 20.
            When it makes an Attack Roll at Advantage against a Prone creature, it can reroll one of the dice once.
            When it hits a Prone creature with an Attack Roll, it can reroll one of the damage dice once."""
    },
    "20": {
        "name": "Wild Surge Of Infernal Wagers",
        "description": """The battlefield becomes a stage for distant hellish spectators. Phantom nobles of the lower realms drift overhead like smoke, whispering bets and
            weaving crooked luck into the flow of combat.
            At the start of each creature's turn, it may petition one of these infernal gamblers for a sliver of stolen power. The creature makes a
            Charisma (Persuasion) check, DC 12 + PB. On a success, it gains a boon of volatile luck: it can add 2d6 to the first Damage Roll or Saving Throw
            it makes before the start of its next turn. If the creature fails to use the boon in time, it is scorched for PBd10 Fire damage. A creature cannot request
            another boon until the end of its next turn.""",
        "echo of ascendance": """Infernal Patronage.
            One of the unseen bettors fastens its hopes, and its greed, to your victory. Its clandestine aid buoys your every move. For the rest of the current Encounter:
            You have Advantage on Attack Rolls and Saving Throws.
            At the end of your turn, one creature you can see within 60ft takes PBd6 Fire damage.""",
        "echo of ruin": """Shield Of Honest Combat.
            A Surge of raw, impartial Wild Magic floods you, rebuking the manipulations of fiends. For the rest of the current Encounter:
            Fiends, and creatures who have received a boon from a fiend, have Disadvantage on Attack Rolls against you, and you have Advantage on Saving Throws to resist
            or avoid their spells and attacks.
            You Resist Fire damage.
            You cannot entreat a boon from a fiend.""",
        "worldshift trait": """Hellbound Favorite.
            A creature marked by this Trait becomes a prized contestant in the infernal wagering halls. For the rest of the current Encounter, it gains the following features:
            It can add 1d6 Fire damage to the first Attack Roll, Damage Roll and Saving Throw it makes each turn.
            It Resists Fire damage.
            It has Advantage on Charisma (Persuasion and Intimidation) checks to interact with devils."""
    },
    "21": {
        "name": "Wild Surge Of Lethargic Twilight",
        "description": """A soft, hypnotic wind drifts across the battlefield, carrying warm currents and faint, otherworldly melodies.
            The area is bathed in Dim Light, like a starlit dusk. All creatures enter into a magical slumber and fall Unconscious.
            Creatures remain Unconscious even if they take damage. Creatures magically wake at the start of their turn and remain Conscious until the end of that turn.
            When a creature's turn ends, it once again collapses into slumber.""",
        "echo of ascendance": """Vital Spark.
            The Surge of Wild Magic invigorates your body and mind, resisting the pull of sleep. For the rest of the current Encounter:
            As long as you have at least 1 Hit Point, you are Immune to the Unconscious condition.
            Your Speed increases by 10ft.
            Your AC increases by 1.""",
        "echo of ruin": """Dreambound.
            Even in deep slumber, your body is protected by Wild Magic. For the rest of the current Encounter:
            While Unconscious, you Resist all damage.
            While you are Unconscious, you have Advantage on all Saving Throws except Dexterity Saving Throws.""",
        "worldshift trait": """Somnolent Fury.
            A creature with this Trait acts with deadly instincts even in sleep. For the rest of the current Encounter, it gains the following features:
            It Resists all damage while Unconscious.
            Once per turn, when it takes damage while Unconscious, it makes a single melee weapon attack at Disadvantage against a random creature within range,
            lashing out in its slumber.
            As a Reaction, when it takes damage while Unconscious, it casts a random spell that it knows (if any), targeting a random creature within range."""
    },
    "22": {
        "name": "Wild Surge Of Malignant Exultation",
        "description": """A Surge of twisted jubilation erupts from a blighted realm where corruption is celebrated. The magic swells with perverse delight,
            empowering those whose spirits resonate with wicked intent.
            Evil-aligned creatures have Advantage on Saving Throws and the first time each turn an Evil-aligned creature deals damage to a creature,
            that creature takes an additional PB Necrotic damage.""",
        "echo of ascendance": """Sovereign Of Dread.
            A cold radiance settles within you, illuminating the secret terror festering at the heart of corruption. For the rest of the current Encounter:
            You can Frighten Evil-aligned creatures, even if they are Immune to the Frightened condition.
            When you deal damage to an Evil-aligned creature, you deal an extra PB Radiant damage.
            The first time each turn you deal Radiant damage to a creature, that creature must succeed on a DC12 + PB Wisdom Saving Throw or be Frightened of you
            for the rest of the current Encounter. A creature can repeat this save at the end of each of its turns, ending the effect on a success.""",
        "echo of ruin": """Beacon Amid Blight.
            A protective radiance envelops you, shielding your spirit from venomous intent. For the rest of the current Encounter:
            If you are not Good-aligned, you can choose to become Good-aligned.
            If you are Good-aligned, you have Advantage on Saving Throws.
            If you are Good-alignment, you are Immune to Necrotic damage and the Frightened condition.""",
        "worldshift trait": """Scion Of Malice.
            A creature altered by this Trait becomes an eager instrument of hateful power, its essence twisted to savor cruelty.
            For the rest of the current Encounter, it gains the following features:
            Its alignment changes to Evil.
            Once per turn, if it deals Necrotic damage to a creature, it gains Heroic Inspiration if it doesn't already have it."""
    },
    "23": {
        "name": "Wild Surge Of Metamorphic Flux",
        "description": """Shifting essence ruptures the battlefield, forcing every creature to momentarily adopt an unstable form.
            On Initiative count 20 each Round, each creature rolls 1d6 and gains the listed boon as its body warps in response to the flux.
            This lasts until Initiative count 20 of the next Round, at which point all creatures re-roll.
            1 - Hummingbird. Receive a Fly Speed equal to half your Walking Speed and you can Hover.
            2 - Snail. Gain Half Cover and your Speed is halved.
            3 - Leopard. Double your Walking Speed and gain a Climb Speed of 30ft.
            4 - Hawk. +2 bonus to Ranged Attack Rolls.
            5 - Bear. +2 bonus to Strength-based Attack Rolls.
            6 - Fox. +1 bonus to Intelligence, Wisdom and Charisma saves; Spell Save DC increases by 1.""",
        "echo of ascendance": """Formshaper Gift.
            Your essence surges with adaptive potential. For the rest of the current Encounter:
            You can cast Polymorph without a spell slot or components but must target yourself or an ally.""",
        "echo of ruin": """Chosen Instincts.
            Your unstable transformation bends partially to your will. For the rest of the current Encounter:
            Instead of rolling on the table, choose two transformations. You gain the benefit of both.""",
        "worldshift trait": """Everchanging Apex.
            The surge ceases to be a passing mutation and instead crowns the creature as a nexus of endless adaptation,
            its form locking in every evolution as reality itself struggles to keep pace. For the rest of the current Encounter, it gains the following features:
            Any boons a creature gains from this Surge lat until the end of the current Encounter instead.
            A bonus to Strength and Dexterity Saving Throws equal to the number of unique boons it has received."""
    },
    "24": {
        "name": "Wild Surge Of Nightmarish Veil",
        "description": """Thick, hallucinatory tendrils of Wild Magic warp the battlefield, filling the air with a pungent, mind-bending haze.
            Those touched by the Surge see horrifying visions and feel a creeping dread.
            Creatures who are Poisoned also gain the Frightened condition, as their senses are overwhelmed by illusions. In addition,
            they take PBd10 Poison damage at the start of their turn.""",
        "echo of ascendance": """Harbinger Of Terror.
            The chaotic power of Wild Magic sharpens your aura into a weapon of fear. For the rest of the current Encounter:
            Once per turn, when you damage a creature, you can force that target to make a DC12 + PB Wisdom Saving Throw. On a failed save, that creature is Frightened
            of you for the rest of the current Encounter, even if Immune to the Frightened condition. A creature can repeat its Saving Throw at the end of each turn,
            ending the effect on a success.""",
        "echo of ruin": """Nightmares Ward.
            The Surge of Wild magic cleanses and fortifies your body. For the rest of the current Encounter:
            You are Immune to the Poisoned condition and Poison damage.
            You are Immune to the Frightened condition.
            As an Action, you can place your hand on one willing, allied creature to end the Poisoned or Frightened condition afflicting them.""",
        "worldshift trait": """Corrupted Miasma.
            A creature infused with this Trait radiates hallucinatory poison and fear. For the rest of the current Encounter, it gains the following features:
            Immune to the Poisoned condition and Poison damage.
            Advantage on Attack Rolls against Frightened creatures.
            Once per turn, when it hits a creature with an Attack Roll, that target must succeed on a DC 12 + PB Constitution Saving Throw or be Poisoned
            for rest of the current Encounter. The target can repeat this save at the end of each of its turns ending the effect on a success."""
    },
    "25": {
        "name": "Wild Surge Of Nullification",
        "description": """A crushing stillness grips the battlefield, as if the world itself inhales and forgets to exhale. Sound dulls, colors fade,
            and the pulse of magic withers beneath an invisible weight.
            Spells of spell level PB - 1 or higher cannot be cast. Any ongoing magical effects from spells of PB - 1 or higher immediately unravel,
            along with lingering effects from previous Wild Surges.""",
        "echo of ascendance": """Defiant Spark.
            A flicker of raw will pushes back against the suffocating silence. Choose one creature within 120ft (including yourself). For the rest of the current Encounter:
            That creature can cast spells unimpeded by the Wild Surge Of Nullification.""",
        "echo of ruin": """Primordial Shell.
            As the suppression deepens, your essence reverts to something ancient and stubbornly physical. For the rest of the current Encounter:
            You resist all damage aside from Bludgeoning, Slashing and Piercing.""",
        "worldshift trait": """Void-Hollowed.
            This creature has been scoured clean of magic, stripped even of the subtle spark shared by living things.
            For the rest of the current Encounter, it gains the following features:
            It cannot cast or Concentrate on spells.
            It gains Resistance to all damage.
            It has Advantage on Strength and Constitution Saving Throws.
            It has Disadvantage on Intelligence, Wisdom and Charisma Saving Throws."""
    },
    "26": {
        "name": "Wild Surge Of Primal Roar",
        "description": """Wild Magic courses through the battlefield, twisting flesh and spirit into bestial forms. Trees sprout fur, moss becomes bristling,
            and all creatures feel a surge of primal ferocity.
            All creatures are Immune to Bludgeoning, Slashing and Piercing damage from weapons. Unarmed Strikes deal 1d8 Slashing damage, that ignores Immunity to it.
            If a creature's Strength modifier is lower than +4, it becomes +4.""",
        "echo of ascendance": """Beast Within.
            The pulse of Wild Magic merges with your own spirit. For the rest of the current Encounter:
            When you take the Attack action on your turn, you can make a number of Unarmed Strikes equal to your Proficiency Bonus.
            If you hit a creature with 3 or more Unarmed Strikes on your turn, you can make an additional Unarmed Strike as a Bonus Action.""",
        "echo of ruin": """Primal Reflexes.
            The chaotic transformation sharpens your senses. For the rest of the current Encounter:
            You have Advantage on Wisdom (Perception and Insight) checks.
            Creatures cannot have Advantage on Attack Rolls against you.
            Once per turn, you can use 10ft of movement to leap 10 x PB ft. This leap does not provoke Opportunity Attacks.""",
        "worldshift trait": """Savage Form.
            A creature transformed by this Trait embraces its primal instincts fully. For the rest of the current Encounter, it gains the following features:
            Its attacks ignore Immunity to Bludgeoning, Piercing and Slashing damage.
            Its movement Speed increases by 5 x PB ft.
            Opportunity Attacks made against it have Disadvantage.
            It can make PB-1 Unarmed Strikes as a Bonus Action (minimum 1)."""
    },
    "27": {
        "name": "Wild Surge Of Resonant Momentum",
        "description": """Vibrant kinetic energy courses through the battlefield, animating the environment with pulsating force.
            Stones tremble, plants sway violently without wind, and the air ripples with crackling Wild Magic.
            All creatures' movement Speeds increase by 20ft. If a creature moves 50ft or more on its turn, all subsequent Attack Rolls it makes on that turn have +PB to hit.""",
        "echo of ascendance": """Momentum Strike.
            The power of Wild Magic imbues your attacks with dynamic force. For the rest of the current Encounter:
            If you move at least 10ft in a straight line toward a creature before hitting it with an Attack Roll, that attack scores a Critical Hit on a d20 roll of 18-20.
            When you score a Critical Hit, you can use a Reaction to take the Disengage or Dodge Action.""",
        "echo of ruin": """Velocity Veil.
            The kinetic energy within you bends perception, making your movements difficult to track. For the rest of the current Encounter:
            You gain +PB to your AC.
            Your movement does not provoke Opportunity Attacks.""",
        "worldshift trait": """Energy Predator.
            A creature with this Trait feeds on the momentum of nearby foes. For the rest of the current Encounter, it gains the following feature:
            As a Bonus Action, you take the Dash action. When you do, creatures of your choice within 30ft of you must succeed on a DC12 + PB Constitution Saving Throw.
            On a failed save, their movement Speed falls to 0 and cannot be increased until the end of their next turn. For each creature that failed the save,
            you gain +1 to your AC until the start of your next turn. (Recharge 6)"""
    },
    "28": {
        "name": "Wild Surge Of Rigid Form",
        "description": """The battlefield is suffused with relentless, unyielding magic of law, forcing all creatures under its influence to follow strict patterns.
            Lawful-aligned creatures can forgo rolling a d20 for Attack Rolls and Saving Throws to get an 11 on the die instead. Additionally, when they damage a creature,
            they can forgo rolling for damage to instead get a result on any damage dice equal to half the dice's maximum roll. For example, a d8 would deal 4 damage.""",
        "echo of ascendance": """Anarchic Burst.
            Wild Magic courses through you, unbinding the constraints of rigid order. For the rest of the current Encounter:
            Your alignment changes to Chaotic.
            You cannot have Disadvantage on Attack Rolls.
            When you roll to attack, you can treat natural 1s as a Critical Hit.
            When you score a Critical Hit, you and the target of your attack are each teleported to a random, unoccupied space PB x 5ft away.""",
        "echo of ruin": """Iron Directive.
            The unbending laws of magic lend you focus and protection. For the rest of the current Encounter:
            Your alignment changes to Lawful.
            You gain +PB to your d20 tests.
            You gain +PB to your AC.""",
        "worldshift trait": """Immutable Arbiter.
            A creature with this Trait embodies the uncompromising force of law. For the rest of the current Encounter, it gains the following features:
            Its alignment changes to Lawful.
            Any Critical Hit against it becomes a normal hit.
            When it takes the Attack action on its turn, it can make a number of attacks equal to the number of creatures that dealt damage to it
            since the end of its last turn (minimum of 1).
            It gains a bonus to its Attack Rolls equal to the number of creatures that dealt damage to it since the end of its last turn."""
    },
    "29": {
        "name": "Wild Surge Of Scorching Inferno",
        "description": """Wild fire erupts across the battlefield, feeding on the very essence of life and Wild Magic.
            All movement Speeds increase by 20ft, and all damage rolls deal an additional PB Fire damage.""",
        "echo of ascendance": """Emberstrike.
            The chaos of Wild Magic ignites your attacks. For the rest of the current Encounter:
            Once per turn, when you deal Fire damage to a creature with an attack or spell, that creature must succeed on a DC12 + PB Constitution Saving Throw or
            start burning, taking PBd6 Fire damage at the start of each of their turns.""",
        "echo of ruin": """Cinder Ward.
            The volatile heart of Wild Magic surrounds you with a protective, fiery shell. For the rest of the current Encounter:
            You gain 5 x PB Temporary Hit Points. For as long as you have these Temporary Hit Points, you resist Fire damage and are immune to Cold damage.""",
        "worldshift trait": """Magma Eruption.
            Infused with molten Wild Magic, a creature with this Trait gains the following features for the rest of the current Encounter:
            Immune to Fire damage.
            In place of one of your attacks, when you take the Attack action on your turn, you can release a burst of flame from your mouth or body in a 5 x PB foot cone.
            Creatures in that area must succeed on a DC 12 + PB Dexterity Saving Throw, taking PBd12 Fire damage on a failed save or half as much on a success. (Recharge 6)."""
    },
    "30": {
        "name": "Wild Surge Of Scorching Relay",
        "description": """Wild Magic crackles unpredictably, leaping from one creature to the next like a chain of living sparks.
            At the start of the first creature's turn in Initiative order, that creature rolls 2d12. If any die shows a 1, it erupts in flames and the creature takes
            Fire damage equal to the total of all dice rolled. Otherwise, that creature chooses another creature within 120ft that has not yet rolled to avoid exploding.
            That creature rolls at the start of its turn, with an additional d12 for each preceding roll. This continues until a die explodes or all creatures have rolled.
            After that, the effect resets the dice to the starting 2d12, and starts again at the start of the first creature's turn in Initiative order.""",
        "echo of ascendance": """Embermaster.
            The Surge of Wild Magic grants you control over the volatile flames. For the rest of the current Encounter:
            When you or an allied creature within 30ft of you rolls to avoid the effects of this Wild Surge, you can use your Reaction to reroll any d12.
            You must use the result of the new roll.""",
        "echo of ruin": """Flameguard.
            Wild Magic hardens your body against the scorching chaos. For the rest of the current Encounter:
            You gain Resistance to Fire damage.
            The next time you would explode, you don't. Instead, continue the chain as normal by choosing the next creature affected by this Surge.""",
        "worldshift trait": """Pyroclast Sovereign.
            A creature with this Trait becomes a conduit for the chaotic, fiery energy of the Surge. For the rest of the current Encounter, it gains the following features:
            Resistance to Fire damage.
            When the creature rolls to avoid exploding, it can choose PB creatures it can see to also roll the same amount of d12s.
            If any of the results on any of the dice rolled are a 1, all creatures that rolled take Fire damage equal to the result of this creature's roll,
            as everyone bursts into flame."""
    },
    "31": {
        "name": "Wild Surge Of Shattered Winter",
        "description": """A brutal wave of unnatural winter sweeps across the battlefield, as if the season itself has been torn open and spilled into the moment.
            Bitter winds claw at exposed skin, and crystalline frost creeps across armor, stone and soil alike. Creatures not immune to Cold damage:
            Cannot regain Hit Points.
            Cannot gain Temporary Hit Points.
            Have their movement Speed reduced by 10ft.
            Additionally, whenever a creature deals damage of a type other than Psychic, it may convert that damage to Cold.""",
        "echo of ascendance": """Winterbound Core.
            The glacial fury of the Surge fuses to your essence, turning your heartbeat into a steady drum of ice. For the rest of the current Encounter:
            You are Immune to Cold damage.
            Cold damage you deal ignores damage Resistances and Immunities.
            The first time you make a damage roll on your turn, you can add PBd8 Cold damage to the result.""",
        "echo of ruin": """Emberheart Veil.
            A stubborn spark pushes back against the oppressive chill, igniting warmth where none should exist. For the rest of the current Encounter:
            You are Immune to Cold damage.
            Your movement Speed increases by 10ft.
            You gain PBd4 Temporary Hit Points at the start of each of your turns.""",
        "worldshift trait": """Frostwrought.
            The creature's flesh crystallizes, its breath turning to white fog, and its soul aligns with the frozen gale surrounding it.
            For the rest of the current Encounter, it gains the following features:
            Immune to Cold damage.
            When a creature you can see within 30ft of you takes Cold damage, you can use your Reaction to reduce its movement Speed by 5 x PB ft until the end of its next turn.
            A creature whose movement Speed is reduced to 0 by this effect must succeed on a DC12 + PB Constitution Saving Throw or be Stunned until the end of its next turn."""
    },
    "32": {
        "name": "Wild Surge Of Aelith's Tempest",
        "description": """Jagged arcs of raw lightning tear across the battlefield, crackling with untamed energy.
            On Initiative count 20 each turn, each creature must succeed on a DC12 + PB Dexterity Saving Throw or take PBd4 Lightning damage.
            Creatures made of metal, or wearing armor made of metal, make this save at Disadvantage.""",
        "echo of ascendance": """Stormblade.
            You channel the fury of the storm into every strike. For the rest of the current Encounter:
            You gain Resistance to Lightning damage.
            You can choose to fail Dexterity Saving Throws to avoid Lightning damage.
            You become charged when you take Lightning damage. Once charged, the next damage roll you make deals an additional PBd12 Lightning damage, and the charge ends.""",
        "echo of ruin": """Thunderstep.
            Your body becomes a conduit of raw electricity. For the rest of the current Encounter:
            As a Bonus Action, you can teleport up to 30ft to an unoccupied space you can see. You vanish and appear in a blinding bolt of lightning.
            When you appear, creatures within 5ft of you must succeed on a DC12 + PB Dexterity Saving Throw or take PBd4 Lightning damage.""",
        "worldshift trait": """Living Storm.
            A creature with this Trait crackles with primal electric energy. For the rest of the current Encounter, it gains the following features:
            Resistance to Lightning and Thunder damage.
            As an Action, you emit a shattering, primal howl. Creatures within 60ft of you make a DC12 + PB Constitution Saving Throw.
            On a failed save, a creature takes PBd6 Thunder damage and is Deafened until the end of its next turn. If a creature fails this save by 5 or more,
            it is also Stunned until the end of its next turn. On a successful save, a creature takes half damage. (Recharge 6)"""
    },
    "33": {
        "name": "Wild Surge Of Slimebound",
        "description": """The battlefield becomes saturated with pulsating, sticky ooze.
            The ground is Difficult Terrain for all creatures except Oozes. Whenever a non-ooze creature dies, the slime absorbs the corpse, transforming it into a Gray Ooze.
            When this Wild Surge ends, transformed corpses return to normal.""",
        "echo of ascendance": """Electromorphic Composition.
            Wild Magic fuses with the ooze, allowing you to manipulate its energy. For the rest of the current Encounter:
            As Bonus Action, you can cast the Cantrip Shocking Grasp using Intelligence, Wisdom or Charisma for your spellcasting ability (choose when you get this Surge).
            You can target creatures within 30ft of you with melee spell attacks as if they are within 5ft, if touching the same source of ooze.
            When you target a creature with a melee spell attack that deals Lightning damage, you can target additional creatures equal to your PB-1 if you and
            your targets are touching the same source of ooze.""",
        "echo of ruin": """The Day I Became A Slime.
            The ooze transforms your body, making you a fluid and adaptable threat. For the rest of the current Encounter:
            You, along with your equipment, can move through spaces 1 inch wide without squeezing.
            You cannot be Grappled.
            You Resist Acid and Poison damage.
            You ignore Difficult Terrain created by oozes.""",
        "worldshift trait": """Mireborn Mutation.
            A creature with this Trait merges with the ooze itself. For the rest of the current Encounter, it gains the following features:
            It ignores Difficult Terrain created by oozes.
            It can climb Difficult Surfaces, including ceilings, without needing to make an Ability Check.
            If a creature touches or is touched by the ooze, it takes PBd4 Acid damage.
            It has Advantage on Saving Throws against spells and effects that would alter its form."""
    },
    "34": {
        "name": "Wild Surge Of Spiraling Cognition",
        "description": """A whirl of hyperactive mental energy floods the battlefield, turning every thought into a crackling spark.
            Ideas ricochet through the minds of all creatures, accelerating into a manic, disorienting storm of creativity and overload.
            Creatures with an Intelligence score of 18 or lower are Poisoned, overcome by the reeling pace of their increasingly addled minds.""",
        "echo of ascendance": """Concept Made Flesh.
            You draw the free-flowing mental energy into focus, giving substance to ideas that exist only in your mind. For the rest of the current Encounter:
            If your Intelligence score is lower than 19, it becomes 19.
            You know the spells Mirror Image and Major Image and can cast them as a Bonus Action without a spell slot or components.
            The save DC for these spells is 8 + Intelligence Modifier + PB.""",
        "echo of ruin": """Mind Anchored In Stillness.
            In the frenzy of unbound cognition, you find a quiet island of clarity that shields you from mental collapse. For the rest of the current Encounter:
            You are immune to the Poisoning effect of this Surge.
            You have Advantage on Intelligence, Wisdom and Charisma Saving Throws and on Constitution Saving Throws made to maintain Concentration.""",
        "worldshift trait": """Cognitive Breaker.
            A creature touched by this distortion of thought becomes a conduit of volatile insight and shimmering mental possibility.
            For the rest of the current Encounter, it gains the following features:
            Intelligence score becomes 19 if it is less than 19.
            It learns two spells from the Wizard spell list of spell level PB or lower (at GM discretion) and can cast those spells once each without a spell slot or components.
            It can concentrate on two spells at once."""
    },
    "35": {
        "name": "Wild Surge Of Thorned Wrath",
        "description": """Spiraling, barbed vines erupt from the soil, twisting into a dense and perilous undergrowth. The battlefield becomes a tangled maze of thorns and brambles.
            The ground is consumed by 10ft spiky plants that form a dense, hazardous jungle. The area they cover is Difficult Terrain, and creatures that move through it
            take PB-1 Piercing damage for every 5ft they move.""",
        "echo of ascendance": """Vine Lash.
            Wild Magic empowers you to wield the living thorns as a weapon. For the rest of the current Encounter:
            When you use the Attack action or cast a spell on your turn, you can cast Thorn Whip as a Bonus Action that turn.
            You choose your spellcasting modifier or +7 when you cast Thorn Whip in this way, whichever is higher.
            When you hit a creature with a melee spell Attack Roll, you can move that creature PB x 5ft directly toward or away from you.""",
        "echo of ruin": """Skyborne Escape.
            Amid the chaos of brambles, the Wild Magic elevates you above danger. For the rest of the current Encounter:
            You gain a Fly Speed equal to your Walking Speed and can Hover. If you already have a Fly Speed, it increases by 30ft.
            You have Advantage on Dexterity Saving Throws while airborne.""",
        "worldshift trait": """Verdant Juggernaut.
            A creature with this Trait is infused with the raw power of the earth. For the rest of the current Encounter, it gains the following features:
            It has a 30ft Burrow Speed but cannot end its turn below ground.
            It can Burrow through unworked earth and stone. While Burrowing in this way, it doesn't disturb the material it moves through.
            Once per turn, when it hits a creature with an Attack Roll, that creature is pushed PB x 5ft directly away from it."""
    },
    "36": {
        "name": "Wild Surge Of Torrential Wrath",
        "description": """A relentless downpour lashes the battlefield, turning the terrain into a torrent of chaos.
            All creatures resist Fire damage, nonmagical flames are extinguished and the ground becomes Difficult Terrain for any creature without a Swim Speed.
            In addition, Attack Rolls that deal Lightning damage on a hit have Advantage and creatures have Disadvantage on Saving Throws to avoid Lightning damage.""",
        "echo of ascendance": """Thunderborn Strike.
            The storm's energy surges through you, empowering your every blow. For the rest of the current Encounter:
            Your weapon attacks deal an additional 1d6 Lightning damage on a hit.
            Whenever you cast a spell that deals Acid, Cold, Fire, Poison or Thunder damage, you can change the damage type to Lightning.""",
        "echo of ruin": """Aquatic Ward.
            The torrential waters shield and invigorate you, turning danger into sanctuary. For the rest of the current Encounter:
            You have a Swim Speed equal to your Walking Speed.
            You resist Lightning and Cold damage.
            While it is raining, you can use your Swim Speed to move through the air. If the rain stops while you are airborne, you fall.""",
        "worldshift trait": """Tempest Warden.
            A creature with this Trait embodies the wrath of the storm. For the rest of the current Encounter, it gains the following features:
            It gains a Swim Speed equal to its Walking Speed.
            It is Immune to Cold and Lightning damage.
            Its Attack Rolls and spells deal an additional 1d6 Lightning damage.
            Once per turn, when it deals Lightning damage to a creature, all other creatures within 10ft of that creature take PB x 2 Lightning damage."""
    },
    "37": {
        "name": "Wild Surge Of Tumbling Horde",
        "description": """At the top of the battlefield, a chaotic swarm of small creatures plummets from above, smashing into the fray.
            On Initiative count 20, each creature below must succeed on a DC 12 + PB Dexterity Saving Throw or take PBd4 Bludgeoning damage and be knocked Prone
            as one of the falling creatures collides with them.""",
        "echo of ascendance": """Skybound Throw.
            The chaos raining from above bends to your will. For the rest of the current Encounter:
            When you take the Attack action on your turn, you can use one of your attacks to hurl a small object (or a fallen creature) toward a creature up to 60ft away.
            That creature must succeed on a DC 12 + PB Dexterity Saving Throw or take PBd10 Bludgeoning damage and fall Prone.""",
        "echo of ruin": """Fleetfoot Evasion.
            The peril above sharpens your reflexes. For the rest of the current Encounter:
            You have Advantage on Dexterity Saving Throws.
            Your AC increases by 2 if you aren't wearing armor. If you are wearing armor, it increases by 1.""",
        "worldshift trait": """Savage Instinct.
            A creature with this Trait becomes a predator amid the chaos of tumbling foes. For the rest of the current Encounter, it gains the following features:
            If a creature within 30ft of it died or fell to 0 Hit Points since the start of its previous turn, it has Advantage on all Attack Rolls and its movement Speed
            increases by PB x 5ft."""
    },
    "38": {
        "name": "Wild Surge Of Umbral Silence",
        "description": """A dense, spellborn shadow oozes outward and clings to every surface. Light collapses into it, swallowed whole,
            until the battlefield becomes a void of soft,pulsing black.
            All nonmagical illumination is extinguished, and no form of Darkvision can pierce this shade. Only creatures with senses beyond sight can reliably navigate the gloom.""",
        "echo of ascendance": """Midnight Perception.
            Wild Magic sharpens your instincts and opens a window into the darkest layers of reality. For the rest of the current Encounter:
            You can see in Darkness, both magical and nonmagical, to a range of 120ft.
            You have a +PB bonus to Damage Rolls when damaging a creature that can't see you.""",
        "echo of ruin": """Earthwake Companion.
            The oppressive shadow calls forth a grounding force. Subtle tremors ripple beneath you, revealing danger by touch rather than sight.
            For the rest of the current Encounter:
            You have Tremorsense out to 30ft.
            When a Blinded creature makes an Attack Roll against a creature within 30ft of you, you can use your Reaction to change the target of that attack
            to another creature within 5ft of the target, subtly shifting the earth at their feet to alter the trajectory of their strike.""",
        "worldshift trait": """Gloom-Stalker Form.
            A creature marked by this Trait merges with the eclipse-soaked magic, becoming a hunter molded from shadow.
            For the rest of the current Encounter, it gains the following features:
            It has Blindsight out to 60ft.
            When it makes an Attack Roll against a Blinded creature, it scores a Critical Hit on a result of 18, 19 or 20 on the d20.
            It can use a Bonus Action to teleport up to 60ft and then immediately take the Hide action. It can use this trait PB times per Long Rest.
            It has Disadvantage on Attack Rolls and Saving Throws while not in Dim Light or Darkness."""
    },
    "39": {
        "name": "Wild Surge Of Unbridled Power",
        "description": """Raw Wild Magic surges across the battlefield, striking with unstoppable kinetic force.
            All damage rolls deal an additional PB Force damage. The first time a creature is dealt Force damage on a turn,
            it must succeed on a DC12 + PB Strength Saving Throw or be pushed 10ft directly away from the source of the damage.""",
        "echo of ascendance": """Kinetic Infusion.
            The chaotic might of Wild Magic flows through your body. For the rest of the current Encounter:
            As a Bonus Action, you can cast Magic Missiles (1st level) without a spell slot or components.
            Creatures Immune to Force damage instead take half damage from your spells and attacks that deal Force damage.""",
        "echo of ruin": """Aegis Of Motion.
            The flowing energy of Wild Magic sharpens your reflexes. For the rest of the current Encounter:
            You have Advantage on Dexterity Saving Throws.
            Creatures have Disadvantage on Attack Rolls against you.""",
        "worldshift trait": """Kinetic Bastion.
            A creature empowered by this Trait becomes a living conduit of raw force. For the rest of the current Encounter, it gains the following features:
            Immune to Force damage.
            AC increases by 2 if it has dealt Force damage to a creature since the start of its last turn."""
    },
    "40": {
        "name": "Wild Surge Of Undying Might",
        "description": """Wild Magic of decay and unlife seeps across the battlefield, animating the fallen and twisting living flesh.
            All living creatures become Undead, resist Necrotic and Poison damage and cannot regain Hit Points until the Surge ends.""",
        "echo of ascendance": """Necrotic Command.
            Your connection to the energies of unlife allows you to bend corpses to your will. For the rest of the current Encounter:
            As a Bonus Action, you cause a number of corpses (skeletons) up to your PB to spring to unlife under your command.
            They follow any orders you give them (no action required) and take their turn immediately after yours. You can only control a number of
            Undead equal to your PB at any given time.""",
        "echo of ruin": """Sanctified Resistance.
            Wild Magic cannot corrupt you, and your presence repels undeath. For the rest of the current Encounter:
            You are immune to the effects of this Surge.
            Undead creatures have Disadvantage on Attack Rolls against you.
            Undead cannot willingly move within 5ft of you.""",
        "worldshift trait": """Decaying Monstrosity.
            A creature with this Trait is infused with relentless necrotic energy. For the rest of the current Encounter, it gains the following features:
            Its Intelligence and Charisma scores fall to 7 if they are higher.
            Once per turn, when it deals damage to an Undead creature, it gains PB Temporary Hit Points.
            It has Advantage on Strength and Constitution Saving Throws.
            If damage reduces it to 0 Hit Points, it must make a Constitution Saving Throw with a DC of 5 + half of the damage taken, unless the damage is
            Radiant or from a Critical Hit. On a success, it falls to 1 Hit Point."""
    },
}