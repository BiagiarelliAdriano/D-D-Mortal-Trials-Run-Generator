import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

function CharacterForm() {
    const { id } = useParams();
    const isEditMode = Boolean(id);
    const navigate = useNavigate();

    // Import CSS
    require("../styles/CharacterForm.css");

    const [loading, setLoading] = useState(isEditMode);
    const [step, setStep] = useState(0);

    const [rollCount, setRollCount] = useState(0);
    const [selectedRoll, setSelectedRoll] = useState(null);

    const [rolledStats, setRolledStats] = useState([]);
    const [initialRolledStats, setInitialRolledStats] = useState([]);

    const [assignedStats, setAssignedStats] = useState({
        strength: null,
        dexterity: null,
        constitution: null,
        intelligence: null,
        wisdom: null,
        charisma: null,
    });

    // Drag-and-drop state
    const [draggedRoll, setDraggedRoll] = useState(null);
    const [dragOverAbility, setDragOverAbility] = useState(null);

    const [formData, setFormData] = useState({
        name: "",
        class_name: "",
        subclass: "",
        species: "",
        species_variant: "",
        background: "",
        level: 1,
        starting_equipment_choice: "standard"
    });

    const [backgrounds, setBackgrounds] = useState([]);

    useEffect(() => {
        fetch("http://localhost:5000/api/backgrounds")
            .then(res => res.json())
            .then(data => setBackgrounds(data))
            .catch(err => console.error("Failed to load backgrounds", err));
    }, []);

    const classes = [
        "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
        "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer",
        "Warlock", "Wizard"
    ];

    const speciesOptions = {
        Aasimar: [],
        Dragonborn: ["Black", "Blue", "Brass", "Bronze", "Copper", "Gold", "Green", "Red", "Silver", "White"],
        Dwarf: [],
        Elf: ["Drow", "High", "Wood"],
        Gnome: ["Forest", "Rock"],
        Goliath: ["Cloud", "Fire", "Frost", "Hill", "Stone", "Storm"],
        Halfling: [],
        Human: [],
        Orc: [],
        Tiefling: ["Abyssal", "Chthonic", "Infernal"],
    };

    useEffect(() => {
        if (!isEditMode) return;

        fetch(`http://localhost:5000/api/characters/${id}`)
            .then(res => res.json())
            .then(data => {
                setFormData({
                    name: data.name,
                    class_name: data.class.name,
                    subclass: data.class.subclass || "",
                    species: data.data.species || "",
                    species_variant: data.data.species_variant || "",
                    background: data.data.background || "",
                    level: data.level,
                });

                if (data.data.abilities) {
                    setAssignedStats(data.data.abilities);
                }

                setLoading(false);
            })
            .catch(() => setLoading(false));
    }, [id, isEditMode]);

    if (loading) return <div>Loading character...</div>;

    const rollAbility = () => {
        const rolls = Array.from({ length: 4 }, () => Math.floor(Math.random() * 6) + 1);
        rolls.sort((a, b) => a - b);
        rolls.shift();
        return rolls.reduce((a, b) => a + b, 0);
    };

    const abilityTotal =
        rolledStats.reduce((sum, r) => sum + r.value, 0) +
        Object.values(assignedStats).filter(v => v !== null).reduce((a, b) => a + b, 0);

    const rollAbilities = () => {
        const canRoll =
            rollCount < 2 ||
            (rollCount === 2 && abilityTotal <= 69);

        if (!canRoll) return;

        const newRolls = Array.from({ length: 6 }, () => ({
            id: crypto.randomUUID(),
            value: rollAbility()
        }));

        setRolledStats(newRolls);
        setInitialRolledStats(newRolls); // 🔐 backup

        setAssignedStats({
            strength: null,
            dexterity: null,
            constitution: null,
            intelligence: null,
            wisdom: null,
            charisma: null,
        });

        setSelectedRoll(null);
        setRollCount(prev => prev + 1);
    };

    const assignStat = (stat, roll = null) => {
        const rollToAssign = roll || selectedRoll;
        if (!rollToAssign) return;

        setAssignedStats(prev => {
            const currentValue = prev[stat];

            setRolledStats(prevRolls => {
                const remaining = prevRolls.filter(r => r.id !== rollToAssign.id);

                if (currentValue !== null) {
                    return [
                        ...remaining,
                        { id: crypto.randomUUID(), value: currentValue }
                    ];
                }

                return remaining;
            });

            return { ...prev, [stat]: rollToAssign.value };
        });

        setSelectedRoll(null);
    };

    // Drag-and-drop handlers
    const handleDragStart = (e, roll) => {
        setDraggedRoll(roll);
        e.dataTransfer.effectAllowed = 'move';
        // Add a slight delay to allow the drag image to be created
        setTimeout(() => {
            e.target.classList.add('dragging');
        }, 0);
    };

    const handleDragEnd = (e) => {
        e.target.classList.remove('dragging');
        setDraggedRoll(null);
        setDragOverAbility(null);
    };

    const handleDragOver = (e) => {
        e.preventDefault(); // Necessary to allow drop
        e.dataTransfer.dropEffect = 'move';
    };

    const handleDragEnter = (stat) => {
        if (dragOverAbility !== stat) {
            setDragOverAbility(stat);
        }
    };

    const handleDragLeave = (e) => {
        // Only clear if we are leaving the button and NOT entering a child of that button
        const related = e.relatedTarget;
        if (related && e.currentTarget.contains(related)) return;
        setDragOverAbility(null);
    };

    const handleDrop = (e, stat) => {
        e.preventDefault();
        setDragOverAbility(null);
        if (draggedRoll) {
            assignStat(stat, draggedRoll);
        }
    };

    const allStatsAssigned = Object.values(assignedStats).every(v => v !== null);

    const resetStatAssignment = () => {
        setRolledStats(initialRolledStats);
        setAssignedStats({
            strength: null,
            dexterity: null,
            constitution: null,
            intelligence: null,
            wisdom: null,
            charisma: null,
        });
        setSelectedRoll(null);
    };

    const handleSubmit = () => {
        const url = isEditMode
            ? `http://localhost:5000/api/characters/${id}`
            : "http://localhost:5000/api/characters";

        const payload = new FormData();
        payload.append("name", formData.name);
        payload.append("class_name", formData.class_name);
        payload.append("subclass", formData.subclass);
        payload.append("level", isEditMode ? formData.level : 1); // 🔥 Default to 1 for new, preserve for edit
        payload.append("species", formData.species);
        payload.append("species_variant", formData.species_variant);
        payload.append("background", formData.background);
        payload.append("starting_equipment_choice", formData.starting_equipment_choice);
        payload.append("abilities", JSON.stringify(assignedStats));

        fetch(url, { method: "POST", body: payload })
            .then(() => navigate("/"));
    };

    // Render steps
    const renderStep = () => {
        switch (step) {
            case 0:
                return (
                    <div className="step-container step-0">
                        <h2>Select a Class</h2>
                        <div className="button-group">
                            {classes.map(c => (
                                <button
                                    key={c}
                                    onClick={() => setFormData({ ...formData, class_name: c })}
                                    className={`selection-button ${formData.class_name === c ? "selected" : ""}`}
                                >
                                    {c}
                                </button>
                            ))}
                        </div>
                        {formData.class_name && (
                            <div className="navigation-buttons">
                                <button className="nav-button" onClick={() => setStep(1)}>Next</button>
                            </div>
                        )}
                    </div>
                );

            case 1:
                const canRoll =
                    rollCount < 2 ||
                    (rollCount === 2 && abilityTotal <= 69);

                return (
                    <div className="step-container step-1">
                        <h2>Roll & Assign Ability Scores</h2>

                        <div className="dice-rolling-section">
                            {canRoll ? (
                                <button className="dice-roll-button" onClick={rollAbilities}>
                                    <span className="dice-icon">🎲</span> Roll 4d6 Drop Lowest
                                </button>
                            ) : (
                                <div className="roll-limit-msg">Rolling complete or limit reached</div>
                            )}

                            <p className="roll-count-display">
                                Rolls used: <strong>{rollCount} / 2</strong>
                                {rollCount === 2 && abilityTotal <= 69 && (
                                    <span className="bonus-reroll"> (+1 bonus reroll available)</span>
                                )}
                            </p>
                        </div>

                        <h3>Rolled Numbers</h3>
                        <div className="button-group">
                            {rolledStats.map(r => (
                                <button
                                    key={r.id}
                                    draggable={true}
                                    onDragStart={(e) => handleDragStart(e, r)}
                                    onDragEnd={handleDragEnd}
                                    onClick={() => setSelectedRoll(r)}
                                    className={`stat-button ${selectedRoll?.id === r.id ? "selected" : ""}`}
                                >
                                    {r.value}
                                </button>
                            ))}
                        </div>

                        <h3>Assign Stats</h3>
                        <div className="assigned-stats-grid">
                            {["strength", "intelligence", "dexterity", "wisdom", "constitution", "charisma"].map(stat => {
                                const val = assignedStats[stat];
                                return (
                                    <button
                                        key={stat}
                                        onClick={() => assignStat(stat)}
                                        onDragOver={handleDragOver}
                                        onDragEnter={() => handleDragEnter(stat)}
                                        onDragLeave={(e) => handleDragLeave(e)}
                                        onDrop={(e) => handleDrop(e, stat)}
                                        className={`assigned-stat-button ${val !== null ? "assigned" : ""
                                            } ${dragOverAbility === stat ? "drag-over" : ""
                                            }`}
                                    >
                                        <span className="stat-label">{stat.toUpperCase()}</span>
                                        <span className="stat-value">{val ?? "-"}</span>
                                    </button>
                                );
                            })}
                        </div>

                        <p><strong>Total = {abilityTotal}</strong></p>

                        <div className="navigation-buttons">
                            <button className="nav-button" onClick={() => setStep(0)}>Back</button>
                            {/* Reset button only for new character */}
                            {!isEditMode && initialRolledStats.length > 0 && (
                                <button className="nav-button" onClick={resetStatAssignment}>
                                    Reset Stats
                                </button>
                            )}
                            <button className="nav-button" disabled={!allStatsAssigned} onClick={() => setStep(2)}>
                                Next
                            </button>
                        </div>
                    </div>
                );

            case 2:
                const variants = speciesOptions[formData.species] || [];
                const requiresVariant = variants.length > 0;

                return (
                    <div className="step-container step-2">
                        <h2>Select a Species</h2>

                        <div className="button-group">
                            {Object.keys(speciesOptions).map(s => (
                                <button
                                    key={s}
                                    onClick={() =>
                                        setFormData({
                                            ...formData,
                                            species: s,
                                            species_variant: ""
                                        })
                                    }
                                    className={`selection-button ${formData.species === s ? "selected" : ""}`}
                                >
                                    {s}
                                </button>
                            ))}
                        </div>

                        {requiresVariant && (
                            <>
                                <h3>Choose Variant</h3>
                                <div className="button-group">
                                    {variants.map(v => (
                                        <button
                                            key={v}
                                            onClick={() =>
                                                setFormData({ ...formData, species_variant: v })
                                            }
                                            className={`selection-button ${formData.species_variant === v ? "selected" : ""}`}
                                        >
                                            {v}
                                        </button>
                                    ))}
                                </div>
                            </>
                        )}

                        {formData.species && (!requiresVariant || formData.species_variant) && (
                            <div className="navigation-buttons">
                                <button className="nav-button" onClick={() => setStep(1)}>Back</button>
                                <button className="nav-button" onClick={() => setStep(3)}>
                                    Next
                                </button>
                            </div>
                        )}
                    </div>
                );

            case 3:
                return (
                    <div className="step-container step-3">
                        <div className="background-selection-header">
                            <h2>Select a Background</h2>
                        </div>
                        <div className="background-equipment-layout">
                            <div className="background-list-column">
                                <div className="background-grid">
                                    {backgrounds.map(bg => (
                                        <button
                                            key={bg.name}
                                            onClick={() => setFormData({ ...formData, background: bg.name })}
                                            className={`background-button ${formData.background === bg.name ? "selected" : ""}`}
                                        >
                                            <strong>{bg.name}</strong>
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div className="equipment-details-column">
                                {formData.background ? (
                                    <div className="equipment-choice-container">
                                        <h3>Starting Equipment Choice</h3>
                                        {(() => {
                                            const selectedBg = backgrounds.find(bg => bg.name === formData.background);
                                            const standard = selectedBg?.starting_equipment?.standard;
                                            const goldOption = selectedBg?.starting_equipment?.gold_option || 50;

                                            return (
                                                <div className="equipment-options">
                                                    <label className="equipment-label">
                                                        <input
                                                            type="radio"
                                                            name="equipment"
                                                            value="standard"
                                                            checked={formData.starting_equipment_choice === "standard"}
                                                            onChange={() => setFormData({ ...formData, starting_equipment_choice: "standard" })}
                                                            className="equipment-radio"
                                                        />
                                                        <span className="equipment-details">
                                                            <strong>Standard Equipment</strong>
                                                            {standard ? (
                                                                <div className="equipment-list-container">
                                                                    <div><strong>Gold:</strong> {standard.gold} GP</div>
                                                                    <div style={{ marginTop: "4px" }}><strong>Items:</strong></div>
                                                                    <ul className="equipment-list-scroll">
                                                                        {standard.items.map((item, idx) => (
                                                                            <li key={idx}>
                                                                                {item.name} {item.quantity > 1 && `(x${item.quantity})`}
                                                                            </li>
                                                                        ))}
                                                                    </ul>
                                                                </div>
                                                            ) : (
                                                                <div className="gold-option-text">Class/Background items + small gold amount.</div>
                                                            )}
                                                        </span>
                                                    </label>

                                                    <label className="equipment-label">
                                                        <input
                                                            type="radio"
                                                            name="equipment"
                                                            value="gold"
                                                            checked={formData.starting_equipment_choice === "gold"}
                                                            onChange={() => setFormData({ ...formData, starting_equipment_choice: "gold" })}
                                                            className="equipment-radio"
                                                        />
                                                        <span className="equipment-details">
                                                            <strong>Gold Only</strong><br />
                                                            <span className="gold-option-text">
                                                                {goldOption} GP
                                                            </span>
                                                        </span>
                                                    </label>
                                                </div>
                                            );
                                        })()}
                                    </div>
                                ) : (
                                    <div className="background-prompt">
                                        <p>Select a background to see equipment options</p>
                                    </div>
                                )}
                            </div>
                        </div>

                        {formData.background && (
                            <div className="navigation-buttons compact">
                                <button className="nav-button" onClick={() => setStep(2)}>Back</button>
                                <button className="nav-button" onClick={() => setStep(4)}>Next</button>
                            </div>
                        )}
                    </div>
                );

            case 4:
                return (
                    <div className="step-container step-4">
                        <h2>Final Details</h2>

                        <div className="form-group">
                            <label>Character Name</label>
                            <input
                                type="text"
                                placeholder="Enter Ascendant name..."
                                value={formData.name}
                                onChange={(e) =>
                                    setFormData({ ...formData, name: e.target.value })
                                }
                            />
                        </div>

                        <div className="level-info-card">
                            <span className="info-label">Start Level</span>
                            <span className="info-value">1</span>
                            <span className="info-desc">All new characters begin their journey at level 1.</span>
                        </div>

                        <div className="navigation-buttons">
                            <button className="nav-button" onClick={() => setStep(3)}>Back</button>
                            <button className="nav-button" disabled={!formData.name} onClick={handleSubmit}>
                                Save Character
                            </button>
                        </div>
                    </div>
                );

            default:
                return null;
        }
    };

    return (
        <div className="character-form-container">
            <h1>{isEditMode ? "Edit Character" : "Create Character"}</h1>
            {renderStep()}
        </div>
    );
}

export default CharacterForm;