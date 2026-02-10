import { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";

// Import CSS
require("../styles/CharacterSheet.css");

// Helper functions and constants
const calculateModifier = (score) => {
    return Math.floor((score - 10) / 2);
};

const proficiencyBonus = (level) => {
    if (level >= 17) return 6;
    if (level >= 13) return 5;
    if (level >= 9) return 4;
    if (level >= 5) return 3;
    return 2;
};

const CLASS_HIT_DICE = {
    "Barbarian": 12,
    "Bard": 8,
    "Cleric": 8,
    "Druid": 8,
    "Fighter": 10,
    "Monk": 8,
    "Paladin": 10,
    "Ranger": 10,
    "Rogue": 8,
    "Sorcerer": 6,
    "Warlock": 8,
    "Wizard": 6,
};

function CharacterSheet() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [character, setCharacter] = useState(null);
    const [loading, setLoading] = useState(true);
    const [skills, setSkills] = useState({}); // Renamed from skillProficiencies
    const [inspiration, setInspiration] = useState(false); // Renamed from heroicInspiration
    const [showMaxHpModifiers, setShowMaxHpModifiers] = useState(false); // Renamed from showModifierInput
    const [maxHpModifier, setMaxHpModifier] = useState(0); // Renamed from damageModInput
    const [inventoryItems, setInventoryItems] = useState([]); // Renamed from inventory
    const [gold, setGold] = useState(0);
    const [inventoryFilter, setInventoryFilter] = useState("All"); // Renamed from activeTab

    // New HP related states
    const [currentHp, setCurrentHp] = useState(0);
    const [baseMaxHp, setBaseMaxHp] = useState(0);
    const [originalMaxHp, setOriginalMaxHp] = useState(0);
    const [effectiveMaxHp, setEffectiveMaxHp] = useState(0);
    const [conModifier, setConModifier] = useState(0);

    useEffect(() => {
        fetch(`http://localhost:5000/api/characters/${id}`)
            .then(res => res.json())
            .then(data => {
                setCharacter(data);
                // Initialize state from fetched data (using backend snake_case keys if needed)
                setSkills(data.data.skillProficiencies || {}); // Use 'skills'
                setInspiration(data.data.heroicInspiration || false); // Use 'inspiration'
                setInventoryItems(data.data.inventory || []); // Use 'inventoryItems'
                setGold(data.data.gold || 0);

                // Initialize HP states
                const constitutionScore = data.data.abilities.constitution;
                const calculatedConModifier = calculateModifier(constitutionScore);
                setConModifier(calculatedConModifier);

                const initialBaseMaxHp = data.data.hp_max_base || 0;
                const initialOriginalMaxHp = data.data.hp_max_original || initialBaseMaxHp;
                const initialMaxHpModifier = data.data.hp_modifier || 0;
                const initialEffectiveMaxHp = initialBaseMaxHp + initialMaxHpModifier;

                setBaseMaxHp(initialBaseMaxHp);
                setOriginalMaxHp(initialOriginalMaxHp);
                setMaxHpModifier(initialMaxHpModifier);
                setEffectiveMaxHp(initialEffectiveMaxHp);
                setCurrentHp(data.data.hp_current || 0);

                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to load character:", err);
                setLoading(false);
            });
    }, [id]);

    // Effect to update effectiveMaxHp when baseMaxHp or maxHpModifier changes
    useEffect(() => {
        setEffectiveMaxHp(baseMaxHp + maxHpModifier);
    }, [baseMaxHp, maxHpModifier]);

    const saveCharacter = useCallback((updates) => {
        fetch(`http://localhost:5000/api/characters/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                data: updates
            })
        })
            .then(res => res.json())
            .then(data => {
                if (!data.success) {
                    console.error("Failed to save character updates");
                }
            })
            .catch(err => console.error("Error saving character:", err));
    }, [id]);

    // Effect to ensure currentHp doesn't exceed effectiveMaxHp
    useEffect(() => {
        if (loading) return;
        if (effectiveMaxHp > 0 && currentHp > effectiveMaxHp) {
            setCurrentHp(effectiveMaxHp);
            saveCharacter({ hp_current: effectiveMaxHp });
        }
    }, [currentHp, effectiveMaxHp, saveCharacter, loading]);


    if (loading) return <div>Loading...</div>
    if (!character) return <div>Error fetching character</div>;

    const ABILITY_SCORES = [ // Renamed from abilities
        { name: "Strength", key: "strength" },
        { name: "Dexterity", key: "dexterity" },
        { name: "Constitution", key: "constitution" },
        { name: "Intelligence", key: "intelligence" },
        { name: "Wisdom", key: "wisdom" },
        { name: "Charisma", key: "charisma" },
    ];

    const SKILL_LIST = [ // Renamed from SKILLS
        { name: "Acrobatics", key: "acrobatics", ability: "dexterity" },
        { name: "Animal Handling", key: "animal_handling", ability: "wisdom" },
        { name: "Arcana", key: "arcana", ability: "intelligence" },
        { name: "Athletics", key: "athletics", ability: "strength" },
        { name: "Deception", key: "deception", ability: "charisma" },
        { name: "History", key: "history", ability: "intelligence" },
        { name: "Insight", key: "insight", ability: "wisdom" },
        { name: "Intimidation", key: "intimidation", ability: "charisma" },
        { name: "Investigation", key: "investigation", ability: "intelligence" },
        { name: "Medicine", key: "medicine", ability: "wisdom" },
        { name: "Nature", key: "nature", ability: "intelligence" },
        { name: "Perception", key: "perception", ability: "wisdom" },
        { name: "Performance", key: "performance", ability: "charisma" },
        { name: "Persuasion", key: "persuasion", ability: "charisma" },
        { name: "Religion", key: "religion", ability: "intelligence" },
        { name: "Sleight Of Hand", key: "sleight_of_hand", ability: "dexterity" },
        { name: "Stealth", key: "stealth", ability: "dexterity" },
        { name: "Survival", key: "survival", ability: "wisdom" },
    ];

    const currentProficiencyBonus = proficiencyBonus(character.level);

    // Temporary hardcoded proficiencies (will come from class later)
    const proficientSaves = ["strength", "constitution"];

    const toggleSkillProficiency = (skillKey) => { // Renamed from toggleSkill
        setSkills(prev => {
            const newState = {
                ...prev,
                [skillKey]: !prev[skillKey]
            };
            saveCharacter({ skillProficiencies: newState });
            return newState;
        });
    };

    const updateCurrentHp = (value) => {
        let val = parseInt(value) || 0;
        val = Math.min(val, effectiveMaxHp);
        val = Math.max(val, 0);
        setCurrentHp(val);
        saveCharacter({ hp_current: val });
    };

    const updateMaxHpModifier = (value) => {
        let val = parseInt(value) || 0;
        // Clamp between -10 and +10
        val = Math.max(-10, Math.min(10, val));
        setMaxHpModifier(val);
        // Don't save immediately - wait for Apply
    };

    const applyMaxHpModifier = () => {
        if (maxHpModifier === 0) return;

        const newBaseMaxHp = baseMaxHp + maxHpModifier;
        setBaseMaxHp(newBaseMaxHp);
        saveCharacter({ hp_max_base: newBaseMaxHp });

        // Reset modifier to 0
        setMaxHpModifier(0);
    };

    const resetMaxHpModifier = () => {
        setMaxHpModifier(0);
    };

    const resetToOriginalMaxHp = () => {
        setBaseMaxHp(originalMaxHp);
        setMaxHpModifier(0);
        saveCharacter({ hp_max_base: originalMaxHp });
        setShowMaxHpModifiers(false);
    };

    const updateGoldAmount = (newGold) => { // Renamed from updateGold
        const val = parseInt(newGold) || 0;
        setGold(val);
        saveCharacter({ gold: val });
    };

    const removeItem = (itemToRemove) => { // Updated to take item object
        const newInventory = inventoryItems.filter(item => item !== itemToRemove);
        setInventoryItems(newInventory);
        saveCharacter({ inventory: newInventory });
    };

    // Group inventory items by category
    const groupedInventory = inventoryItems.reduce((acc, item) => {
        const category = item.category || "Other";
        if (!acc[category]) {
            acc[category] = [];
        }
        acc[category].push(item);
        return acc;
    }, { "All": inventoryItems });

    const displayedItems = groupedInventory[inventoryFilter] || [];


    return (
        <div className="character-sheet-container">
            <button onClick={() => navigate("/")} className="back-button">Back to Hub</button>

            <div className="sheet-header">
                <h2>{character.name} <span className="level-display">(Level {character.level})</span></h2>
                <div className="header-info">
                    <strong>{character.class.name}</strong>
                    <span className="header-separator">|</span>
                    <strong>{character.data.species}</strong>
                    <span className="header-separator">|</span>
                    <strong>{character.data.background}</strong>
                    <span className="header-separator">|</span>
                    <span>Hit Die: d{CLASS_HIT_DICE[character.class.name] || "?"}</span>
                    <span className="header-separator">|</span>
                    <span>Proficiency Bonus: +{currentProficiencyBonus}</span>
                </div>
            </div>

            {/* HP Management Section */}
            <div className="hp-section">
                <div className="hp-header">
                    <h2>Hit Points</h2>
                    <div className="constitution-display">
                        Constitution Modifier: <strong>{conModifier >= 0 ? "+" : ""}{conModifier}</strong>
                    </div>
                </div>

                <div className="hp-controls">
                    <div>
                        <label className="hp-label">CURRENT</label>
                        <input
                            type="number"
                            value={currentHp}
                            onChange={(e) => updateCurrentHp(e.target.value)}
                            className="hp-input"
                        />
                    </div>

                    <div className="hp-divider">/</div>

                    <div className="max-hp-container">
                        <label className="hp-label">MAX</label>
                        <div
                            className={`max-hp-display ${baseMaxHp > originalMaxHp ? "buffed" : baseMaxHp < originalMaxHp ? "damaged" : "normal"}`}
                            onClick={() => setShowMaxHpModifiers(!showMaxHpModifiers)}
                            title="Click to manage modifiers"
                        >
                            {effectiveMaxHp}
                        </div>

                        {showMaxHpModifiers && (
                            <div className="modifier-popup">
                                <span className="modifier-label">Modifier:</span>
                                <input
                                    type="number"
                                    min="-10"
                                    max="10"
                                    value={maxHpModifier}
                                    onChange={(e) => updateMaxHpModifier(e.target.value)}
                                    className="modifier-input"
                                />
                                <button
                                    onClick={applyMaxHpModifier}
                                    className="modifier-btn apply-btn"
                                    title="Apply modifier to base HP"
                                    disabled={maxHpModifier === 0}
                                >
                                    Apply
                                </button>
                                <button
                                    onClick={resetMaxHpModifier}
                                    className="modifier-btn reset-btn"
                                    title="Reset modifier to 0"
                                >
                                    Clear
                                </button>
                                <button
                                    onClick={resetToOriginalMaxHp}
                                    className="modifier-btn reset-original-btn"
                                    title="Reset to original Max HP"
                                    disabled={baseMaxHp === originalMaxHp}
                                >
                                    Reset
                                </button>
                                <button
                                    onClick={() => setShowMaxHpModifiers(false)}
                                    className="modifier-btn close-btn"
                                >
                                    ✕
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Heroic Inspiration */}
            <div className="inspiration-section">
                <h3 className="inspiration-title">Heroic Inspiration</h3>
                <button
                    onClick={() => {
                        setInspiration(prev => {
                            const newState = !prev;
                            saveCharacter({ heroicInspiration: newState });
                            return newState;
                        });
                    }}
                    className={`inspiration-btn ${inspiration ? "active" : "inactive"}`}
                >
                    {inspiration ? "🌟 Has Inspiration" : "⚪ No Inspiration"}
                </button>
            </div>

            {/* Ability Scores & Saving Throws */}
            <div className="abilities-saves-grid">
                <div className="list-section">
                    <h3>Ability Scores</h3>
                    <ul className="plain-list">
                        {ABILITY_SCORES.map(({ name, key }) => {
                            const score = character.data?.abilities?.[key] ?? 10;
                            const mod = calculateModifier(score);

                            return (
                                <li key={key}>
                                    <strong>{name}:</strong> {score}
                                    <span className="ability-modifier">
                                        ({mod >= 0 ? "+" : ""}{mod})
                                    </span>
                                </li>
                            );
                        })}
                    </ul>
                </div>

                <div className="list-section">
                    <h3>Saving Throws</h3>
                    <ul className="plain-list">
                        {ABILITY_SCORES.map(({ name, key }) => {
                            const score = character.data?.abilities?.[key] ?? 10;
                            const base = calculateModifier(score);
                            const isProficient = proficientSaves.includes(key); // Using the temporary proficientSaves
                            const total = base + (isProficient ? currentProficiencyBonus : 0);

                            return (
                                <li key={key}>
                                    <span className={`proficiency-indicator ${isProficient ? "proficient" : ""}`}>
                                        {isProficient ? "●" : "○"}
                                    </span>
                                    <strong>{name}:</strong> {total >= 0 ? "+" : ""}{total}
                                </li>
                            );
                        })}
                    </ul>
                </div>
            </div>

            {/* Skills */}
            <div className="list-section">
                <h3>Skills</h3>
                <ul className="plain-list skill-list">
                    {SKILL_LIST.map(skill => {
                        const isProficient = skills[skill.key] ?? false; // Use skill.key for proficiency lookup
                        const abilityScore = character.data.abilities[skill.ability];
                        const mod = calculateModifier(abilityScore);
                        const bonus = mod + (isProficient ? currentProficiencyBonus : 0);

                        return (
                            <li key={skill.key} className="skill-item">
                                <button
                                    onClick={() => toggleSkillProficiency(skill.key)}
                                    className={`skill-toggle ${isProficient ? "proficient" : "not-proficient"}`}
                                    title="Toggle Proficiency"
                                >
                                    {isProficient && "✓"}
                                </button>
                                <span className="skill-name">{skill.name}</span>
                                <span className="skill-ability">({skill.ability.slice(0, 3).toUpperCase()})</span>
                                <strong>{bonus >= 0 ? "+" : ""}{bonus}</strong>
                            </li>
                        );
                    })}
                </ul>
            </div>

            {/* Inventory & Gold */}
            <div className="inventory-section">
                <div className="inventory-header">
                    <h2>Inventory</h2>
                    <div className="gold-display">
                        <label className="gold-label">Gold Pieces (GP):</label>
                        <input
                            type="number"
                            value={gold}
                            onChange={(e) => updateGoldAmount(e.target.value)}
                            className="gold-input"
                        />
                    </div>
                </div>

                <div className="inventory-tabs">
                    {Object.keys(groupedInventory).map(category => (
                        <button
                            key={category}
                            onClick={() => setInventoryFilter(category)}
                            className={`inventory-tab ${inventoryFilter === category ? "active" : "inactive"}`}
                        >
                            {category} ({groupedInventory[category].length})
                        </button>
                    ))}
                </div>

                <ul className="inventory-list">
                    {displayedItems.length > 0 ? displayedItems.map((item, idx) => (
                        <li key={idx} className="inventory-item">
                            <div>
                                <strong>{item.name}</strong>
                                {item.quantity > 1 && <span className="item-quantity">x{item.quantity}</span>}
                                {inventoryFilter === "All" && (
                                    <span className="item-category-tag">
                                        {item.category || "Other"}
                                    </span>
                                )}
                            </div>
                            <button
                                onClick={() => removeItem(item)}
                                className="remove-item-btn"
                                title="Remove Item"
                            >
                                ✕
                            </button>
                        </li>
                    )) : (
                        <li className="empty-inventory-message">No items in this category.</li>
                    )}
                </ul>
            </div>
        </div>
    );
}

export default CharacterSheet;