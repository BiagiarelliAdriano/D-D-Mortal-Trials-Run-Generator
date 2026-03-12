import re

filepath = r"d:\rungenerator\D-D-Mortal-Trials-Run-Generator\frontend\src\components\CharacterSheet.js"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the function definitions
pattern = r"(    const renderSpellcastingWidget = \(\) => \{.+?    \};\n\n    const renderSpellOverlay = \(\) => \{.+?    \};\n\n)"
match = re.search(pattern, content, flags=re.DOTALL)
if match:
    functions = match.group(1)
    
    # Remove them from their current location
    content = content.replace(functions, "")
    
    # Insert them right before `if (loading) return`
    insert_pattern = r"(    if \(loading\) return <div className=\"loading-screen\">Invoking the Character Sheet...</div>;)"
    
    content = re.sub(insert_pattern, functions + r"\1", content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed syntax error.")
else:
    print("Pattern not found!")
