"""
Data tables for class-wide feature options and "menu" style selections.
"""

SORCERER_METAMAGIC = {
    "careful_spell": {
        "name": "Careful Spell",
        "cost": 1,
        "description": "When you cast a spell that forces other creatures to make a saving throw, you can protect some of those creatures from the spell's full force. To do so, spend 1 Sorcery Point and choose a number of those creatures up to your Charisma modifier (minimum of one creature). A chosen creature automatically succeeds on its saving throw against the spell, and it takes no damage if it would normally take half damage on a successful save."
    },
    "distant_spell": {
        "name": "Distant Spell",
        "cost": 1,
        "description": "When you cast a spell that has a range of at least 5ft, you can spend 1 Sorcery Point to double the spell's range. Or when you cast a spell that has a range of Touch, you can spend 1 Sorcery Point to make the spell's range 30ft."
    },
    "empowered_spell": {
        "name": "Empowered Spell",
        "cost": 1,
        "description": "When you roll damage for a spell, you can spend 1 Sorcery Point to reroll a number of the damage dice up to your Charisma modifier (minimum of one), and you must use the new rolls. You can use Empowered Spell even if you've already used a different Metamagic option during the casting of the spell."
    },
    "extended_spell": {
        "name": "Extended Spell",
        "cost": 1,
        "description": "When you cast a spell that has a duration of 1 minute or longer, you can spend 1 Sorcery Point to double its duration to a maximum duration of 24 hours. If the affected spell requires Concentration, you have Advantage on any saving throw you make to maintain that Concentration."
    },
    "heightened_spell": {
        "name": "Heightened Spell",
        "cost": 2,
        "description": "When you cast a spell that forces a creature to make a saving throw, you can spend 2 Sorcery Points to give one target of the spell Disadvantage on saves against the spell."
    },
    "quickened_spell": {
        "name": "Quickened Spell",
        "cost": 2,
        "description": "When you cast a spell that has a casting time of an action, you can spend 2 Sorcery Points to change the casting time to a Bonus Action for this casting. You can't modify a spell in this way if you've already cast a level 1+ spell on the current turn, nor can you cast a level 1+ spell on this turn after modifying a spell in this way."
    },
    "seeking_spell": {
        "name": "Seeking Spell",
        "cost": 1,
        "description": "If you make an attack roll for a spell and miss, you can spend 1 Sorcery Point to reroll the d20, and you must use the new roll. You can use Seeking Spell even if you've already used a different Metamagic option during the casting of the spell."
    },
    "subtle_spell": {
        "name": "Subtle Spell",
        "cost": 1,
        "description": "When you cast a spell, you can spend 1 Sorcery Point to cast it without any Verbal, Somatic, or Material components, except Material components that are consumed by the spell or that have a cost specified in the spell."
    },
    "transmuted_spell": {
        "name": "Transmuted Spell",
        "cost": 1,
        "description": "When you cast a spell that deals a type of damage from the following list, you can spend 1 Sorcery Point to change that damage type to one of the other listed types: Acid, Cold, Fire, Lightning, Poison, Thunder."
    },
    "twinned_spell": {
        "name": "Twinned Spell",
        "cost": 1,
        "description": "When you cast a spell that can be cast with a higher-level spell slot to target an additional creature, you can spend 1 Sorcery Point to increase the spell's effective level by 1."
    }
}

WARLOCK_ELDRITCH_INVOCATIONS = {
    "agonizing_blast": {
        "name": "Agonizing Blast",
        "prerequisite": "Level 2+ Warlock, a Warlock Cantrip That Deals Damage",
        "description": "Choose one of your known Warlock cantrips that deals damage. You can add your Charisma modifier to that spell's damage rolls. Repeatable: You can gain this invocation more than once. Each time you do so, choose a different eligible Cantrip."
    },
    "armor_of_shadows": {
        "name": "Armor Of Shadows",
        "description": "You can cast Mage Armor on yourself without expending a spell slot."
    },
    "ascendant_step": {
        "name": "Ascendant Step",
        "prerequisite": "Level 5+ Warlock",
        "description": "You can cast Levitate on yourself without expending a spell slot."
    },
    "devil_sight": {
        "name": "Devil's Sight",
        "prerequisite": "Level 2+ Warlock",
        "description": "You can see normally in Dim Light and Darkness, both magical and nonmagical, within 120ft of yourself."
    },
    "devouring_blade": {
        "name": "Devouring Blade",
        "prerequisite": "Level 12+ Warlock, Thirsting Blade Invocation",
        "description": "The Extra Attack of your Thirsting Blade invocation confers two extra attacks rather than one."
    },
    "eldritch_mind": {
        "name": "Eldritch Mind",
        "description": "You have Advantage on Constitution saving throws that you make to maintain Concentration."
    },
    "eldritch_smite": {
        "name": "Eldritch Smite",
        "prerequisite": "Level 5+ Warlock, Pact of the Blade Invocation",
        "description": "Once per turn when you hit a creature with your pact weapon, you can expend a Pact Magic spell slot to deal an extra 1d8 Force damage to the target, plus another 1d8 per level of the spell slot, and you can give the target the Prone condition if it is Huge or smaller."
    },
    "eldritch_spear": {
        "name": "Eldritch Spear",
        "prerequisite": "Level 2+ Warlock, a Warlock Cantrip That Deals Damage",
        "description": "Choose one of your known Warlock cantrips that deals damage and has a range of 10+ft. When you cast that spell, its range increases by a number of feet equal to 30 times your Warlock level. Repeatable: You can gain this invocation more than once. Each time you do so, choose a different eligible cantrip."
    },
    "fiendish_vigor": {
        "name": "Fiendish Vigor",
        "prerequisite": "Level 2+ Warlock",
        "description": "You can cast False Life on yourself without expending a spell slot. When you cast the spell with this feature, you don't roll the die for the Temporary Hit Points; you automatically get the highest number on the die."
    },
    "gaze_of_two_minds": {
        "name": "Gaze Of Two Minds",
        "prerequisite": "Level 5+ Warlock",
        "description": "You can use a Bonus Action to touch a willing creature and perceive through its senses until the end of your next turn. As long as the creature is on the same plane of existence as you, you can take a Bonus Action on subsequent turns to maintain this connection, extending the duration until the end of your next turn. The connection ends if you don't maintain it in this way. While perceiving through the other creature's senses, you benefit from any special senses possessed by that creature, and you can cast spells as if you were in your space or the other creature's space if the two of you are within 60ft of each other."
    },
    "gift_of_the_depths": {
        "name": "Gift Of The Depths",
        "prerequisite": "Level 5+ Warlock",
        "description": "You can breathe underwater, and you gain a Swim Speed equal to your Speed. You can also cast Water Breathing once without expending a spell slot. You regain the ability to cast it in this way again when you finish a Long Rest."
    },
    "gift_of_the_protectors": {
        "name": "Gift Of The Protectors",
        "prerequisite": "Level 9+ Warlock, Pact Of The Tome Invocation",
        "description": "A new page appears in your Book Of Shadows when you conjure it. With your permission, a creature can take an action to write its name on that page, which can contain a number of names equal to your Charisma modifier (minimum of one name). When any creature whose name is on the page is reduced to 0 Hit Points but not killed outright, the creature magically drops to 1 Hit Point instead. Once this magic is triggered, no creature can benefit from it until you finish a Long Rest. As a Magic action, you can erase a name on the page by touching it."
    },
    "investment_of_the_chain_master": {
        "name": "Investment Of The Chain Master",
        "prerequisite": "Level 5+ Warlock, Pact Of The Chain Invocation",
        "description": "When you cast Find Familiar, you infuse the summoned familiar with a measure of your eldritch power, granting the creature the following benefits. The familiar gains either a Fly Speed or a Swim Speed (your choice) of 40ft. As a Bonus Action, you can command the familiar to take the Attack action. Whenever the familiar deals Bludgeoning, Piercing or Slashing damage, you can make it deal Necrotic or Radiant damage instead. If the familiar forces a creature to make a saving throw, it uses your spell save DC. When the familiar takes damage, you can take a Reaction to grant it Resistance against that damage."
    },
    "lessons_of_the_first_ones": {
        "name": "Lessons Of The First Ones",
        "prerequisite": "Level 2+ Warlock",
        "description": "You have received knowledge from an elder entity of the multiverse, allowing you to gain one Origin feat of your choice. Repeatable: You can gain this invocation more than once. Each time you do so, choose a different Origin feat."
    },
    "lifedrinker": {
        "name": "Lifedrinker",
        "prerequisite": "Level 9+ Warlock, Pact Of The Blade Invocation",
        "description": "Once per turn when you hit a creature with your pact weapon, you can deal an extra 1d6 Necrotic, Psychic, or Radiant damage (your choice) to the creature, and you can expend one of your Hit Point Dice to roll it and regain a number of Hit Points equal to the roll plus your Constitution modifier (minimum of 1 Hit Point)."
    },
    "mask_of_many_faces": {
        "name": "Mask Of Many Faces",
        "prerequisite": "Level 2+ Warlock",
        "description": "You can cast Disguise Self without expending a spell slot."
    },
    "master_of_myriad_forms": {
        "name": "Master Of Myriad Forms",
        "prerequisite": "Level 5+ Warlock",
        "description": "You can cast Alter Self without expending a spell slot."
    },
    "misty_visions": {
        "name": "Misty Visions",
        "prerequisite": "Level 2+ Warlock",
        "description": "You can cast Silent Image without expending a spell slot."
    },
    "one_with_shadows": {
        "name": "One With Shadows",
        "prerequisite": "Level 5+ Warlock",
        "description": "While you're in an area of Dim Light or Darkness, you can cast Invisibility on yourself without expending a spell slot."
    },
    "otherworldly_leap": {
        "name": "Otherworldly Leap",
        "prerequisite": "Level 2+ Warlock",
        "description": "You can cast Jump on yourself without expending a spell slot."
    },
    "pact_of_the_blade": {
        "name": "Pact Of The Blade",
        "description": "As a Bonus Action, you can conjure a pact weapon in your hand, a Simple or Martial Melee weapon of your choice with which you bond, or create a bond with a magic weapon you touch; you can't bond with a magic weapon if someone else is attuned to it or another Warlock is bonded with it. Until the bond ends, you have proficiency with the weapon, and you can use it as a Spellcasting Focus. Whenever you attack with the bonded weapon, you can use your Charisma modifier for the attack and damage rolls instead of using Strength or Dexterity; and you can cause the weapon to deal Necrotic, Psychic, or Radiant damage or its normal damate type. Your bond with the weapon ends if you use this feature's Bonus Action again, if the weapon is more than 5ft away from you for 1 minute or more, or if you die. A conjured weapon disappears when the bond ends."
    },
    "pact_of_the_chain": {
        "name": "Pact Of The Chain",
        "description": "You learn the Find Familiar spell and can cast it as a Magic action without expending a spell slot. When you cast the spell, you choose one of the normal forms for your familiar or one of the following special forms: Imp, Pseudodragon, Quasit, Skeleton, Slaad Tadpole, Sphinx Of Wonder, Sprite, or Venomous Snake. Additionally, when you take the Attack action, you can forgo one of your own attacks to allow your familiar to make one attack of its own with its Reaction."
    },
    "pact_of_the_tome": {
        "name": "Pact Of The Tome",
        "description": "Stitching together strands of shadow, you conjure forth a book in your hand at the end of a Short or Long Rest. This Book Of Shadows (you determine its appearance) contains eldritch magic that only you can access, granting you the following benefits. The book disappears if you conjure another book with this feature or if you die. When the book appears, choose three cantrips, and choose two level 1 spells that have the Ritual tag. The spells can be from any class's spell list, and they must be spells you don't already have prepared. While the book is on your person, you have the chosen spells prepared, and they function as Warlock spells from you. You can use the book as a Spellcasting Focus."
    },
    "repelling_blast": {
        "name": "Repelling Blast",
        "prerequisite": "Level 2+ Warlock, a Warlock Cantrip That Deals Damage Via An Attack Roll",
        "description": "Choose one of your known Warlock cantrips that requires an attack roll. When you hit a Large or smaller creature with that cantrip, you can push the creature up to 10ft straight away from you. Repeatable: You can gain this invocation more than once. Each time you do so, choose a different eligible cantrip."
    },
    "thirsting_blade": {
        "name": "Thirsting Blade",
        "prerequisite": "Level 5+ Warlock, Pact Of The Blade Invocation",
        "description": "You gain the Extra Attack feature for your pact weapon only. With that weapon, you can attack twice with the weapon instead of once when you take the Attack action on your turn."
    },
    "visions_of_distant_realms": {
        "name": "Visions Of Distant Realms",
        "prerequisite": "Level 9+ Warlock",
        "description": "You can cast Arcane Eye without expending a spell slot."
    },
    "whispers_of_the_grave": {
        "name": "Whispers Of The Grave",
        "prerequisite": "Level 7+ Warlock",
        "description": "You can cast Speak with Dead without expending a spell slot."
    },
    "witch_sight": {
        "name": "Witch Sight",
        "prerequisite": "Level 15+ Warlock",
        "description": "You have Truesight with a range of 30ft."
    }
}
