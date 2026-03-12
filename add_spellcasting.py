import re

filepath = r"d:\rungenerator\D-D-Mortal-Trials-Run-Generator\frontend\src\components\CharacterSheet.js"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. State Variables
state_vars = """    const [activeFeatures, setActiveFeatures] = useState([]); // Array of IDs
    const [spellSlotsRules, setSpellSlotsRules] = useState(null);
    const [availableSpells, setAvailableSpells] = useState(null);
    const [showSpellOverlay, setShowSpellOverlay] = useState(false);"""
content = re.sub(r"    const \[activeFeatures, setActiveFeatures\] = useState\(\[\]\); // Array of IDs", state_vars, content)

# 2. Fetch spell slots
spell_slots_fetch = """        // Fetch armor rules
        fetch(`http://localhost:5000/api/rules/armor`)
            .then(res => res.json())
            .then(rules => setArmorRules(rules))
            .catch(err => console.error("Failed to load armor rules:", err));

        // Fetch spell slot rules
        fetch(`http://localhost:5000/api/rules/spell_slots`)
            .then(res => res.json())
            .then(rules => setSpellSlotsRules(rules))
            .catch(err => console.error("Failed to load spell slot rules:", err));"""
content = re.sub(r"        // Fetch armor rules\s+fetch\(`http://localhost:5000/api/rules/armor`\)\s+\.then\(res => res\.json\(\)\)\s+\.then\(rules => setArmorRules\(rules\)\)\s+\.catch\(err => console\.error\(\"Failed to load armor rules:\", err\)\);", spell_slots_fetch, content)

# 3. Fetch spells
spells_fetch = """                // Fetch class rules
                if (data.class?.name) {
                    fetch(`http://localhost:5000/api/classes/${data.class.name.toLowerCase()}`)
                        .then(res => res.json())
                        .then(rules => setClassRules(rules))
                        .catch(err => console.error("Failed to load class rules:", err));

                    fetch(`http://localhost:5000/api/spells/${data.class.name.toLowerCase()}`)
                        .then(res => res.json())
                        .then(spells => setAvailableSpells(spells))
                        .catch(err => console.error("Failed to load spells:", err));
                }"""
content = re.sub(r"                // Fetch class rules\s+if \(data\.class\?\.name\) \{\s+fetch\(`http://localhost:5000/api/classes/\$\{data\.class\.name\.toLowerCase\(\)\}`\)\s+\.then\(res => res\.json\(\)\)\s+\.then\(rules => setClassRules\(rules\)\)\s+\.catch\(err => console\.error\(\"Failed to load class rules:\", err\)\);\s+\}", spells_fetch, content)

# 4. Layout Constraints
layout_c = """    inventory: { minW: 12, maxW: 12, minH: 3, maxH: 20 },
    spellcasting: { minW: 6, maxW: 12, minH: 8, maxH: 30 },"""
content = re.sub(r"    inventory: \{ minW: 12, maxW: 12, minH: 3, maxH: 20 \},", layout_c, content)

# 5. Default Layouts
default_l = """            { i: "inventory", x: 0, y: 39, w: 12, h: 6, static: isLayoutLocked, ...LAYOUT_CONSTRAINTS.inventory },
            { i: "spellcasting", x: 0, y: 45, w: 12, h: 10, static: isLayoutLocked, ...LAYOUT_CONSTRAINTS.spellcasting },"""
content = re.sub(r"            \{ i: \"inventory\", x: 0, y: 39, w: 12, h: 6, static: isLayoutLocked, \.\.\.LAYOUT_CONSTRAINTS\.inventory \},", default_l, content)

# 6. Spellcasting Logic and Widget
spell_logic = """    const renderSpellcastingWidget = () => {
        if (!classRules?.spellcasting || !spellSlotsRules || !character) return null;

        const spellcasting = classRules.spellcasting;
        const ability = spellcasting.ability || "intelligence";
        const abilityScore = character.data.abilities[ability] || 10;
        const mod = calculateModifier(abilityScore);
        const saveDC = 8 + currentProficiencyBonus + mod;
        const attackBonus = currentProficiencyBonus + mod;

        const progression = spellcasting.progression; // full, half, third, pact_magic
        const slotsTable = spellSlotsRules[progression];
        let availableSlotsObj = {};
        if (slotsTable) {
            let maxSlotLevel = character.level;
            while (maxSlotLevel > 0 && !slotsTable[maxSlotLevel]) {
                maxSlotLevel--;
            }
            if (maxSlotLevel > 0) {
                availableSlotsObj = slotsTable[maxSlotLevel];
            }
        }

        const selectedSpells = character.data.spells || [];

        return (
            <div key="spellcasting" className="widget card spellcasting-widget">
                {!isLayoutLocked && <div className="widget-handle">⠿</div>}
                <div className="spellcasting-header">
                    <h3>Spellcasting</h3>
                    <button className="manage-spells-btn" onClick={() => setShowSpellOverlay(true)}>Manage Spells</button>
                </div>
                
                <div className="spell-stats-row">
                    <div className="spell-stat-box">
                        <span className="spell-stat-label">Ability</span>
                        <span className="spell-stat-val">{ability.slice(0, 3).toUpperCase()}</span>
                    </div>
                    <div className="spell-stat-box">
                        <span className="spell-stat-label">Save DC</span>
                        <span className="spell-stat-val">{saveDC}</span>
                    </div>
                    <div className="spell-stat-box">
                        <span className="spell-stat-label">Attack Bonus</span>
                        <span className="spell-stat-val">+{attackBonus}</span>
                    </div>
                </div>

                <div className="spell-slots-row">
                    {Object.keys(availableSlotsObj).map(level => (
                        <div key={level} className="spell-slot-box">
                            <span className="slot-lvl">Lv {level}</span>
                            <span className="slot-count">{availableSlotsObj[level]}</span>
                        </div>
                    ))}
                    {Object.keys(availableSlotsObj).length === 0 && <span className="no-slots-msg">No spell slots available yet.</span>}
                </div>

                <div className="prepared-spells-list scrollable">
                    { /* Group chosen spells by level to display them */ }
                    {["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"].map(level => {
                        const spellsAtLevel = availableSpells?.[level] || [];
                        const selectedAtLevel = spellsAtLevel.filter(s => selectedSpells.includes(s.name));
                        
                        if (selectedAtLevel.length === 0) return null;

                        return (
                            <div key={level} className="spell-level-group">
                                <h4>{level === "0" ? "Cantrips" : `Level ${level}`}</h4>
                                {selectedAtLevel.map(spell => (
                                    <div key={spell.name} className="prepared-spell-row">
                                        <span className="spell-name">{spell.name}</span>
                                        <span className="spell-school">{spell.school}</span>
                                    </div>
                                ))}
                            </div>
                        );
                    })}
                    {selectedSpells.length === 0 && <div className="no-spells-note">No spells selected. Click 'Manage Spells' to choose.</div>}
                </div>
            </div>
        );
    };

    const renderSpellOverlay = () => {
        if (!showSpellOverlay || !availableSpells) return null;

        const selectedSpells = character.data.spells || [];

        const toggleSpellSelection = (name) => {
            const current = [...selectedSpells];
            if (current.includes(name)) {
                // Remove
                const updated = current.filter(n => n !== name);
                saveCharacter({ spells: updated });
                // We update local character object optimally
                setCharacter(prev => ({...prev, data: {...prev.data, spells: updated}}));
            } else {
                // Add
                current.push(name);
                saveCharacter({ spells: current });
                setCharacter(prev => ({...prev, data: {...prev.data, spells: current}}));
            }
        };

        const spellcasting = classRules?.spellcasting;
        const progression = spellcasting?.progression; 
        const slotsTable = progression ? spellSlotsRules?.[progression] : null;

        // Find max spell level available for this character
        let maxAvailableSlot = 0;
        if (slotsTable) {
            let clvl = character.level;
            while (clvl > 0 && !slotsTable[clvl]) clvl--;
            if (clvl > 0) {
                const slots = slotsTable[clvl];
                maxAvailableSlot = Math.max(...Object.keys(slots).map(Number));
            }
        }
        // Always allow cantrips (0)
        
        return (
            <div className="spell-overlay">
                <div className="spell-overlay-content">
                    <div className="overlay-header">
                        <h2>Select Spells</h2>
                        <button className="close-btn" onClick={() => setShowSpellOverlay(false)}>✕</button>
                    </div>
                    <p className="overlay-hint">Filtering by your max available spell slot level (Cantrips to Level {maxAvailableSlot}). Spells chosen are saved automatically.</p>
                    <div className="spell-overlay-list">
                        {Object.keys(availableSpells).map(level => {
                            if (parseInt(level) > maxAvailableSlot && level !== "0") return null;
                            const spellsAtLevel = availableSpells[level];

                            return (
                                <div key={level} className="overlay-level-group">
                                    <h3>{level === "0" ? "Cantrips" : `Level ${level}`}</h3>
                                    <div className="spell-selection-grid">
                                        {spellsAtLevel.map(spell => {
                                            const isSelected = selectedSpells.includes(spell.name);
                                            return (
                                                <div 
                                                    key={spell.name} 
                                                    className={`spell-select-card ${isSelected ? 'selected' : ''}`}
                                                    onClick={() => toggleSpellSelection(spell.name)}
                                                >
                                                    <div className="spell-name">{spell.name}</div>
                                                    <div className="spell-school">{spell.school}</div>
                                                    {isSelected && <div className="spell-check">✓</div>}
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
        );
    };"""

content = re.sub(r"            \{showXpEditor && \(", spell_logic + "\n\n            {showXpEditor && (", content)

# Inject the call to render inside the ResponsiveGridLayout
content = re.sub(
    r"            </ResponsiveGridLayout>", 
    r"                {renderSpellcastingWidget()}\n            </ResponsiveGridLayout>\n            {renderSpellOverlay()}", 
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied successfully.")
