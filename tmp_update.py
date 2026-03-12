import re

file_path = r"d:\rungenerator\D-D-Mortal-Trials-Run-Generator\encounter_generator\data\spells.py"

target_class = "Wizard"

spells_list = {
    "Acid Splash", "Blade Ward", "Chill Touch", "Dancing Lights", "Elementalism", "Fire Bolt", "Friends", "Light", "Mage Hand", "Mending", "Message", "Mind Sliver", "Minor Illusion", "Poison Spray", "Prestidigitation", "Ray Of Frost", "Shocking Grasp", "Thunderclap", "Toll The Dead", "True Strike", "Alarm", "Burning Hands", "Charm Person", "Chromatic Orb", "Color Spray", "Comprehend Languages", "Detect Magic", "Disguise Self", "Expeditious Retreat", "False Life", "Feather Fall", "Find Familiar", "Fog Cloud", "Grease", "Ice Knife", "Identify", "Illusory Script", "Jump", "Longstrider", "Mage Armor", "Magic Missile", "Protection From Evil And Good", "Ray Of Sickness", "Shield", "Silent Image", "Sleep", "Tasha's Hideous Laughter", "Tenser's Floating Disk", "Thunderwave", "Unseen Servant", "Witch Bolt", "Alter Self", "Arcane Lock", "Arcane Vigor", "Augury", "Blindness/Deafness", "Blur", "Cloud Of Daggers", "Continual Flame", "Crown Of Madness", "Darkness", "Darkvision", "Detect Thoughts", "Dragon's Breath", "Enhance Ability", "Enlarge/Reduce", "Flaming Sphere", "Gentle Repose", "Gust Of Wind", "Hold Person", "Invisibility", "Knock", "Levitate", "Locate Object", "Magic Mouth", "Magic Weapon", "Melf's Acid Arrow", "Mind Spike", "Mirror Image", "Misty Step", "Nystul's Magic Aura", "Phantasmal Force", "Ray Of Enfeeblement", "Rope Trick", "Scorching Ray", "See Invisibility", "Shatter", "Spider Climb", "Suggestion", "Web", "Animate Dead", "Bestow Curse", "Blink", "Clairvoyance", "Counterspell", "Dispel Magic", "Fear", "Feign Death", "Fireball", "Fly", "Gaseous Form", "Glyph Of Warding", "Haste", "Hypnotic Pattern", "Leomund's Tiny Hut", "Lightning Bolt", "Magic Circle", "Major Image", "Nondetection", "Phantom Steed", "Protection From Energy", "Remove Curse", "Sending", "Sleet Storm", "Slow", "Speak With Dead", "Stinking Cloud", "Summon Fey", "Summon Undead", "Tongues", "Vampiric Touch", "Water Breathing", "Arcane Eye", "Banishment", "Blight", "Charm Monster", "Confusion", "Conjure Minor Elementals", "Control Water", "Dimension Door", "Divination", "Evard's Black Tentacles", "Fabricate", "Fire Shield", "Greater Invisibility", "Hallucinatory Terrain", "Ice Storm", "Leomund's Secret Chest", "Locate Creature", "Mordenkainen's Faithful Hound", "Mordenkainen's Private Sanctum", "Otiluke's Resilient Sphere", "Phantasmal Killer", "Polymorph", "Stone Shape", "Stoneskin", "Summon Aberration", "Summon Construct", "Summon Elemental", "Vitriolic Sphere", "Wall Of Fire", "Animate Objects", "Bigby's Hand", "Circle Of Power", "Cloudkill", "Cone Of Cold", "Conjure Elemental", "Contact Other Plane", "Creation", "Dominate Person", "Dream", "Geas", "Hold Monster", "Jallarzi's Storm Of Radiance", "Legend Lore", "Mislead", "Modify Memory", "Passwall", "Planar Binding", "Rary's Telepathic Bond", "Scrying", "Seeming", "Steel Wind Strike", "Summon Dragon", "Synaptic Static", "Telekinesis", "Teleportation Circle", "Wall Of Force", "Wall Of Stone", "Yolande's Regal Presence", "Arcane Gate", "Chain Lightning", "Circle Of Death", "Contingency", "Create Undead", "Disintegrate", "Drawmij's Instant Summons", "Eyebite", "Flesh To Stone", "Globe Of Invulnerability", "Guards And Wards", "Magic Jar", "Mass Suggestion", "Move Earth", "Otiluke's Freezing Sphere", "Otto's Irresistable Dance", "Programmed Illusion", "Summon Fiend", "Sunbeam", "Tasha's Bubblinb Cauldron", "True Seeing", "Wall Of Ice", "Delayed Blast Fireball", "Etherealness", "Finger Of Death", "Forcecage", "Mirage Arcane", "Mordenkainen's Magnificent Mansion", "Mordenkainen's Sword", "Plane Shift", "Prismatic Spray", "Project Image", "Reverse Gravity", "Sequester", "Simulacrum", "Symbol", "Teleport", "Antimagic Field", "Antipathy/Sympathy", "Befuddlement", "Clone", "Control Weather", "Demiplane", "Dominate Monster", "Incendiary Cloud", "Maze", "Mind Blank", "Power Word Stun", "Sunburst", "Telepathy", "Astral Projection", "Foresight", "Gate", "Imprisonment", "Meteor Swarm", "Power Word Kill", "Priismatic Wall", "Shapechange", "Time Stop", "True Polymorph", "Weird"
}

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'(\s*\{\s*\n\s*"name":\s*"([^"]+)",)(.*?)(?=\n\s*\}(?:,|\n|\]))', re.DOTALL)

def replacer(match):
    header = match.group(1)
    name = match.group(2)
    body = match.group(3)
    
    if name in spells_list:
        if '"classes":' in body or "'classes':" in body:
            def class_replacer(m):
                full_match = m.group(0)
                classes_str = m.group(1).strip()
                if f'"{target_class}"' not in classes_str and f"'{target_class}'" not in classes_str:
                    if not classes_str:
                        return f'"classes": ["{target_class}"]'
                    elif classes_str.endswith(','):
                        return f'"classes": [{classes_str} "{target_class}"]'
                    else:
                        return f'"classes": [{classes_str}, "{target_class}"]'
                return full_match
            body = re.sub(r'"classes":\s*\[(.*?)\]', class_replacer, body, count=1, flags=re.DOTALL)
        else:
            # Insert after "school"
            body = re.sub(r'("school":\s*"[^"]+")', r'\1,\n            "classes": ["' + target_class + '"]', body, count=1)

    return header + body

new_content = pattern.sub(replacer, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Updated spells for {target_class}!")
