"""
Find class names and locate where subclass-related entries appear in classes.py.
"""
with open('encounter_generator/data/rules/classes.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find lines that contain specific markers
for i, line in enumerate(lines, 1):
    # Find class dict openings
    if '= {' in line and any(c in line for c in ['BARBARIAN', 'BARD', 'CLERIC', 'DRUID', 'FIGHTER', 'MONK', 'PALADIN', 'RANGER', 'ROGUE', 'SORCERER', 'WARLOCK', 'WIZARD']):
        print(f'L{i}: {line.rstrip()}')
    # Find the level-3 features blocks
    if '"id":' in line and ('subclass' in line.lower() or 'Subclass' in line):
        print(f'L{i}: {line.rstrip()}')
    # Find lines with "note" and "features at various levels"  
    if 'features at' in line.lower() or 'various levels' in line.lower():
        print(f'L{i}: {line.rstrip()}')
    # Find "choose" with options for subclasses
    if '"options":' in line and i > 100:
        stripped = line.strip()
        if len(stripped) < 200:
            print(f'L{i}: {line.rstrip()}')
