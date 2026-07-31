import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import API_BASE_URL from "../config";

function CharacterForm() {
    const { id } = useParams();
    const isEditMode = Boolean(id);
    const navigate = useNavigate();
    const { token } = useAuth();

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
    const [isRandomizing, setIsRandomizing] = useState(false);
    const [isAutoRandomizing, setIsAutoRandomizing] = useState(false);
    const [formData, setFormData] = useState({
        name: "",
        class_name: "",
        subclass: "",
        species: "",
        species_variant: "",
        background: "",
        level: 1,
        starting_equipment_choice: "standard",
        size: ""
    });

    const [backgrounds, setBackgrounds] = useState([]);
    const [speciesData, setSpeciesData] = useState([]);
    const [feats, setFeats] = useState({ origin: [], general: [], fighting_style: [], epic_boon: [] });

    // Background Choice State
    const [bgChoices, setBgChoices] = useState({
        mode: "2_1", // '2_1' or '1_1_1'
        plus2: "",
        plus1: "",
        plus1_a: "",
        plus1_b: "",
        plus1_c: ""
    });

    const [uiToggles, setUiToggles] = useState({
        featExpanded: true,
        equipExpanded: false,
        classDetailsExpanded: true
    });

    // Class Choice State
    const [classDetails, setClassDetails] = useState(null);
    const [selectedSpeciesDetails, setSelectedSpeciesDetails] = useState(null);
    const [classSkills, setClassSkills] = useState([]);
    const [classEquipChoice, setClassEquipChoice] = useState(null);
    const [previewLevel, setPreviewLevel] = useState(1);

    useEffect(() => {
        fetch(`${API_BASE_URL}/api/backgrounds`)
            .then(res => res.json())
            .then(data => setBackgrounds(data))
            .catch(err => console.error("Failed to load backgrounds", err));

        fetch(`${API_BASE_URL}/api/species`)
            .then(res => res.json())
            .then(data => setSpeciesData(data))
            .catch(err => console.error("Failed to load species", err));

        fetch(`${API_BASE_URL}/api/feats`)
            .then(res => res.json())
            .then(data => setFeats(data))
            .catch(err => console.error("Failed to load feats", err));
    }, []);

    const classes = [
        "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
        "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer",
        "Warlock", "Wizard"
    ];


    useEffect(() => {
        if (!isEditMode) return;

        fetch(`${API_BASE_URL}/api/characters/${id}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
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

                if (data.class.name) {
                    fetch(`${API_BASE_URL}/api/classes/${data.class.name.toLowerCase()}`)
                        .then(res => res.json())
                        .then(classData => setClassDetails(classData))
                        .catch(err => console.error("Failed to load class details during edit", err));
                }

                if (data.data.species) {
                    fetch(`${API_BASE_URL}/api/species`)
                        .then(res => res.json())
                        .then(speciesList => {
                            const found = speciesList.find(s => s.name === data.data.species);
                            setSelectedSpeciesDetails(found);
                        })
                        .catch(err => console.error("Failed to load species details during edit", err));
                }

                setLoading(false);
            })
            .catch(() => setLoading(false));
    }, [id, isEditMode, token]);

    const handleClassSelect = (className) => {
        setFormData({ ...formData, class_name: className });
        setClassSkills([]); // Reset skill choices
        setClassEquipChoice(null); // Reset equipment choice
        setPreviewLevel(1); // Reset preview level

        // Fetch class details
        fetch(`${API_BASE_URL}/api/classes/${className.toLowerCase()}`)
            .then(res => res.json())
            .then(data => setClassDetails(data))
            .catch(err => console.error("Failed to load class details", err));
    };

    // Loading check moved down to avoid violating rules of hooks

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

    const randomizeStats = async () => {
        if (isRandomizing || initialRolledStats.length === 0) return;
        setIsRandomizing(true);

        // Reset first
        setAssignedStats({
            strength: null,
            dexterity: null,
            constitution: null,
            intelligence: null,
            wisdom: null,
            charisma: null,
        });
        setRolledStats(initialRolledStats);
        setSelectedRoll(null);

        // Wait a bit after reset
        await new Promise(resolve => setTimeout(resolve, 500));

        const abilities = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"];
        const shuffledAbilities = [...abilities].sort(() => Math.random() - 0.5);
        const statsPool = [...initialRolledStats];

        for (let i = 0; i < 6; i++) {
            const statName = shuffledAbilities[i];
            const roll = statsPool[i];

            setAssignedStats(prev => ({ ...prev, [statName]: roll.value }));
            setRolledStats(prev => prev.filter(r => r.id !== roll.id));

            if (i < 5) {
                await new Promise(resolve => setTimeout(resolve, 1500));
            }
        }

        setIsRandomizing(false);
    };

    // Helper: briefly flash the auto-just-picked CSS class on a DOM element
    const flashPicked = (selector) => {
        const el = typeof selector === 'string'
            ? document.querySelector(selector)
            : selector;
        if (!el) return;
        el.classList.remove('auto-just-picked');
        // Force reflow so re-adding the class restarts the animation
        void el.offsetWidth;
        el.classList.add('auto-just-picked');
        setTimeout(() => el.classList.remove('auto-just-picked'), 1100);
    };

    useEffect(() => {
        if (!isAutoRandomizing) return;
        
        const timeoutId = setTimeout(() => {
            if (step === 0) {
                if (!formData.class_name) {
                    const randomClass = classes[Math.floor(Math.random() * classes.length)];
                    handleClassSelect(randomClass);
                    setTimeout(() => flashPicked(`.selection-button[data-class="${randomClass}"]`), 150);
                } else if (classDetails && classDetails.name.toLowerCase() === formData.class_name.toLowerCase()) {
                    const requiredSkills = classDetails.proficiencies.skills.choose;
                    if (classSkills.length < requiredSkills) {
                        document.querySelector('.skill-picker-container')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        setTimeout(() => {
                            const options = [...classDetails.proficiencies.skills.options];
                            options.sort(() => 0.5 - Math.random());
                            const chosen = options.slice(0, requiredSkills);
                            setClassSkills(chosen);
                            // Flash each chosen skill button
                            setTimeout(() => {
                                chosen.forEach(skill => {
                                    const btns = document.querySelectorAll('.skill-item-button');
                                    btns.forEach(btn => {
                                        if (btn.textContent.trim() === skill) flashPicked(btn);
                                    });
                                });
                            }, 50);
                        }, 1000);
                    } else {
                        document.querySelector('.equipment-choice-section')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        setTimeout(() => {
                            const equipOptions = Object.keys(classDetails.starting_equipment);
                            const chosen = equipOptions[Math.floor(Math.random() * equipOptions.length)];
                            setClassEquipChoice(chosen);
                            setTimeout(() => flashPicked(`.equip-option-card[data-key="${chosen}"]`), 50);
                            setTimeout(() => setStep(1), 1100);
                        }, 1000);
                    }
                }
            } 
            else if (step === 1) {
                if (allStatsAssigned) {
                    setStep(2);
                } else {
                    const canRoll = rollCount < 2 || (rollCount === 2 && abilityTotal <= 69);
                    if (rolledStats.length === 0 || (canRoll && abilityTotal <= 69)) {
                        rollAbilities();
                    } else {
                        const abilities = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"];
                        const shuffledAbilities = [...abilities].sort(() => Math.random() - 0.5);
                        
                        setAssignedStats(prev => {
                            const newStats = { ...prev };
                            initialRolledStats.forEach((roll, i) => {
                                newStats[shuffledAbilities[i]] = roll.value;
                            });
                            return newStats;
                        });
                        setRolledStats([]);
                    }
                }
            }
            else if (step === 2) {
                if (!formData.species) {
                    const randomSpecies = speciesData[Math.floor(Math.random() * speciesData.length)];
                    setFormData(prev => ({ ...prev, species: randomSpecies.name, species_variant: "" }));
                    setSelectedSpeciesDetails(randomSpecies);
                    setTimeout(() => flashPicked(`.selection-button[data-species="${randomSpecies.name}"]`), 150);
                } else if (selectedSpeciesDetails) {
                    let updates = {};
                    const isSizeMissing = Array.isArray(selectedSpeciesDetails.size) && !formData.size;
                    const variations = selectedSpeciesDetails.variations || [];
                    const isVariantMissing = variations.length > 0 && !formData.species_variant;
                    
                    if (isSizeMissing) {
                        updates.size = selectedSpeciesDetails.size[Math.floor(Math.random() * selectedSpeciesDetails.size.length)];
                    }
                    if (isVariantMissing) {
                        updates.species_variant = variations[Math.floor(Math.random() * variations.length)];
                    }
                    
                    if (Object.keys(updates).length > 0) {
                        setFormData(prev => ({ ...prev, ...updates }));
                        setTimeout(() => {
                            if (updates.species_variant) flashPicked(`.species-variant-button[data-variant="${updates.species_variant}"]`);
                        }, 150);
                    } else {
                        setStep(3);
                    }
                }
            }
            else if (step === 3) {
                if (!formData.background) {
                    const randomBg = backgrounds[Math.floor(Math.random() * backgrounds.length)];
                    setFormData(prev => ({ ...prev, background: randomBg.name }));
                    setTimeout(() => flashPicked(`.background-button[data-bg="${randomBg.name}"]`), 150);
                } else if (!bgChoices.plus2 && !bgChoices.plus1_a) {
                    document.querySelector('.background-button.selected')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    
                    setTimeout(() => {
                        const is21 = Math.random() > 0.5;
                        const mode = is21 ? "2_1" : "1_1_1";
                        
                        if (mode === "2_1") {
                            const selectedBg = backgrounds.find(bg => bg.name === formData.background);
                            const availableAbilities = selectedBg?.ability_scores || ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"];
                            const shuffled = [...availableAbilities].sort(() => Math.random() - 0.5);
                            setBgChoices(prev => ({
                                ...prev,
                                mode: "2_1",
                                plus2: shuffled[0],
                                plus1: shuffled[1]
                            }));
                            setTimeout(() => {
                                flashPicked('.bg-bonus-select-plus2');
                                flashPicked('.bg-bonus-select-plus1');
                            }, 100);
                        } else {
                            setBgChoices(prev => ({
                                ...prev,
                                mode: "1_1_1"
                            }));
                        }
                    }, 1000);
                } else {
                    setStep(4);
                }
            }
            else if (step === 4) {
                setIsAutoRandomizing(false);
            }
        }, 1000);

        return () => clearTimeout(timeoutId);
    });

    if (loading) {
        return (
            <div className="character-form-container">
                <h1>{isEditMode ? "Edit Character" : "Create Character"}</h1>
                <div style={{ textAlign: "center", padding: "40px", color: "var(--text-dim)", fontStyle: "italic" }}>
                    Loading character data...
                </div>
            </div>
        );
    }

    const handleSubmit = () => {
        const url = isEditMode
            ? `${API_BASE_URL}/api/characters/${id}`
            : `${API_BASE_URL}/api/characters`;

        const payload = new FormData();
        payload.append("name", formData.name);
        payload.append("class_name", formData.class_name);
        payload.append("subclass", formData.subclass);
        payload.append("level", isEditMode ? formData.level : 1); // 🔥 Default to 1 for new, preserve for edit
        payload.append("species", formData.species);
        payload.append("species_variant", formData.species_variant);
        payload.append("background", formData.background);
        payload.append("starting_equipment_choice", formData.starting_equipment_choice);

        // Randomize size if species has options and none selected
        let finalSize = formData.size;
        if (!finalSize && selectedSpeciesDetails && Array.isArray(selectedSpeciesDetails.size)) {
            const sizes = selectedSpeciesDetails.size;
            finalSize = sizes[Math.floor(Math.random() * sizes.length)];
        }
        payload.append("size", finalSize || (selectedSpeciesDetails?.size || "Medium"));

        // Calculate boosted stats
        const boostedStats = { ...assignedStats };
        if (bgChoices.mode === "2_1") {
            if (bgChoices.plus2) boostedStats[bgChoices.plus2.toLowerCase()] += 2;
            if (bgChoices.plus1) boostedStats[bgChoices.plus1.toLowerCase()] += 1;
        } else {
            if (bgChoices.plus1_a) boostedStats[bgChoices.plus1_a.toLowerCase()] += 1;
            if (bgChoices.plus1_b) boostedStats[bgChoices.plus1_b.toLowerCase()] += 1;
            if (bgChoices.plus1_c) boostedStats[bgChoices.plus1_c.toLowerCase()] += 1;
        }

        payload.append("abilities", JSON.stringify(boostedStats));

        // Store background choices in a custom field for the sheet to see
        const selectedBg = backgrounds.find(bg => bg.name === formData.background);
        // Robust feat lookup
        let featData = null;
        if (selectedBg?.feat) {
            featData = feats.origin.find(f => f.name === selectedBg.feat);
            if (!featData) {
                // Try to find by partial match for variation feats like "Magic Initiate (Cleric)"
                featData = feats.origin.find(f => {
                    const baseName = f.name.split(' {')[0];
                    return selectedBg.feat.includes(baseName);
                });

                // If found, format description if it has variations
                if (featData && featData.name.includes("{variation}")) {
                    const variation = selectedBg.feat.match(/\(([^)]+)\)/)?.[1] || "";
                    featData = {
                        ...featData,
                        name: selectedBg.feat,
                        effects: featData.effects.map(e => e.replaceAll("{variation}", variation))
                    };
                }
            }
        }

        const choices = {
            background_bonus: bgChoices,
            background_feat: featData,
            background_skills: selectedBg?.skills || [],
            class_skills: classSkills,
            class_equipment_choice: classEquipChoice
        };
        payload.append("choices", JSON.stringify(choices));
        payload.append("class_starting_equipment_choice", classEquipChoice);

        // Ensure proficiencies include background skills AND class skills
        const proficiencies = formData.proficiencies || [];
        const bgSkills = (selectedBg?.skills || []).map(s => s.toLowerCase().replace(/\s+/g, '_'));
        const clsSkills = classSkills.map(s => s.toLowerCase().replace(/\s+/g, '_'));
        const combinedProficiencies = [...new Set([...proficiencies, ...bgSkills, ...clsSkills])];
        payload.append("proficiencies", JSON.stringify(combinedProficiencies));

        fetch(url, { 
            method: "POST", 
            body: payload,
            headers: { 'Authorization': `Bearer ${token}` }
        })
            .then(() => navigate("/characters"));
    };

    // Render steps
    const renderStep = () => {
        switch (step) {
            case 0:
                return (
                    <div className="step-container step-0">
                        <h2>Select your Class</h2>
                        <div className="class-selection-layout">
                            <div className="class-list-column">
                                <div className="button-group">
                                    {classes.map(c => (
                                        <button
                                            key={c}
                                            onClick={() => handleClassSelect(c)}
                                            data-class={c}
                                            className={`selection-button ${formData.class_name === c ? "selected" : ""}`}
                                        >
                                            {c}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div className="class-details-column">
                                {classDetails ? (
                                    <>
                                        <div className="class-details-header">
                                            <h3>{classDetails.name}</h3>
                                            <p>{classDetails.description}</p>
                                        </div>

                                        <div className="class-facts-grid">
                                            <div className="fact-item">
                                                <span className="fact-label">Hit Die</span>
                                                <span className="value-bubble">{classDetails.hit_die}</span>
                                            </div>
                                            <div className="fact-item">
                                                <span className="fact-label">Primary Ability</span>
                                                <span className="value-bubble">
                                                    {Array.isArray(classDetails.primary_ability)
                                                        ? classDetails.primary_ability.join(" & ")
                                                        : classDetails.primary_ability}
                                                </span>
                                            </div>
                                            <div className="fact-item">
                                                <span className="fact-label">Saving Throws</span>
                                                <span className="value-bubble">
                                                    {Array.isArray(classDetails.proficiencies.saving_throws)
                                                        ? classDetails.proficiencies.saving_throws.join(", ")
                                                        : classDetails.proficiencies.saving_throws}
                                                </span>
                                            </div>
                                        </div>

                                        <div className="bg-choice-section">
                                            <h4>Armor Proficiencies</h4>
                                            <div className="bg-skill-list">
                                                {(classDetails.proficiencies.armor || []).length > 0 ? (
                                                    classDetails.proficiencies.armor.map(a => <span key={a} className="bg-skill-tag">{a}</span>)
                                                ) : <span className="info-desc">None</span>}
                                            </div>

                                            <h4>Weapon Proficiencies</h4>
                                            <div className="bg-skill-list">
                                                {(classDetails.proficiencies.weapons || []).length > 0 ? (
                                                    classDetails.proficiencies.weapons.map(w => <span key={w} className="bg-skill-tag">{w}</span>)
                                                ) : <span className="info-desc">None</span>}
                                            </div>

                                            <h4>Tool Proficiencies</h4>
                                            <div className="bg-skill-list">
                                                {(classDetails.proficiencies.tools.granted || []).length > 0 ? (
                                                    classDetails.proficiencies.tools.granted.map(t => <span key={t} className="bg-skill-tag">{t}</span>)
                                                ) : <span className="info-desc">None</span>}
                                            </div>
                                        </div>

                                        <div className="skill-picker-container">
                                            <h4>Class Skills</h4>
                                            <p className="skill-count-hint">Choose {classDetails.proficiencies.skills.choose} from the list below:</p>
                                            <div className="skill-picker-grid">
                                                {classDetails.proficiencies.skills.options.map(skill => {
                                                    const isSelected = classSkills.includes(skill);
                                                    const canSelect = isSelected || classSkills.length < classDetails.proficiencies.skills.choose;
                                                    return (
                                                        <button
                                                            key={skill}
                                                            className={`skill-item-button ${isSelected ? "selected" : ""}`}
                                                            onClick={() => {
                                                                if (isSelected) {
                                                                    setClassSkills(classSkills.filter(s => s !== skill));
                                                                } else if (canSelect) {
                                                                    setClassSkills([...classSkills, skill]);
                                                                }
                                                            }}
                                                        >
                                                            {skill}
                                                        </button>
                                                    );
                                                })}
                                            </div>
                                        </div>

                                        <div className="equipment-choice-section">
                                            <h4>Starting Equipment</h4>
                                            <div className="equip-options-grid">
                                                {Object.entries(classDetails.starting_equipment).map(([key, option], idx) => (
                                                    <div
                                                        key={key}
                                                        data-key={key}
                                                        className={`equip-option-card ${classEquipChoice === key ? "selected" : ""}`}
                                                        onClick={() => setClassEquipChoice(key)}
                                                    >
                                                        <h5>Scenario {key.split("_")[1].toUpperCase()}</h5>
                                                        <div className="option-items">
                                                            {option.items && option.items.length > 0 ? (
                                                                option.items.map((it, i) => (
                                                                    <div key={i}>• {it}</div>
                                                                ))
                                                            ) : (
                                                                <div>Pure Gold</div>
                                                            )}
                                                            {option.gold > 0 && (
                                                                <div>• {option.gold} GP</div>
                                                            )}
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>

                                        <div className="level-preview-section">
                                            <h4>Feature Preview (Lvl {previewLevel})</h4>
                                            <div className="level-preview-nav">
                                                {Array.from({ length: 20 }, (_, i) => i + 1).map(lvl => (
                                                    <div
                                                        key={lvl}
                                                        className={`level-dot ${previewLevel === lvl ? "active" : ""}`}
                                                        onClick={() => setPreviewLevel(lvl)}
                                                    >
                                                        {lvl}
                                                    </div>
                                                ))}
                                            </div>
                                            <div className="feature-preview-list">
                                                {classDetails.features[previewLevel] && classDetails.features[previewLevel].length > 0 ? (
                                                    classDetails.features[previewLevel].map((feat, idx) => (
                                                        <div key={idx} className="feature-preview-card">
                                                            <h6>{feat.name}</h6>
                                                            <p>{feat.summary}</p>
                                                        </div>
                                                    ))
                                                ) : (
                                                    <p className="info-desc">No new base features at this level.</p>
                                                )}
                                            </div>
                                        </div>
                                    </>
                                ) : (
                                    <div className="background-prompt">Select a class to see details</div>
                                )}
                            </div>
                        </div>
                        {formData.class_name && (
                            <div className="navigation-buttons compact">
                                <button
                                    className="nav-button"
                                    onClick={() => setStep(1)}
                                    disabled={!classDetails || classSkills.length !== classDetails.proficiencies.skills.choose}
                                >
                                    Next: Ability Scores
                                </button>
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
                                <button className="dice-roll-button" onClick={rollAbilities} disabled={isRandomizing}>
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
                            {initialRolledStats.length > 0 && (
                                <button 
                                    className={`randomize-button ${isRandomizing ? 'loading' : ''}`} 
                                    onClick={randomizeStats} 
                                    disabled={isRandomizing}
                                >
                                    <span className="random-icon">{isRandomizing ? '⏳' : '✨'}</span> 
                                    {isRandomizing ? 'Randomizing...' : 'Randomize'}
                                </button>
                            )}
                        </div>

                        <h3>Rolled Numbers</h3>
                        <div className="rolled-stats-group">
                            {rolledStats.map(r => (
                                <button
                                    key={r.id}
                                    draggable={!isRandomizing}
                                    onDragStart={(e) => handleDragStart(e, r)}
                                    onDragEnd={handleDragEnd}
                                    onClick={() => !isRandomizing && setSelectedRoll(r)}
                                    className={`stat-button ${selectedRoll?.id === r.id ? "selected" : ""} ${isRandomizing ? "disabled" : ""}`}
                                    disabled={isRandomizing}
                                >
                                    {r.value}
                                </button>
                            ))}
                        </div>

                        <h3>Assign Stats</h3>
                        <div className="assigned-stats-grid">
                            {["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"].map(stat => {
                                const val = assignedStats[stat];
                                return (
                                    <button
                                        key={stat}
                                        title={stat.charAt(0).toUpperCase() + stat.slice(1)}
                                        onClick={() => !isRandomizing && assignStat(stat)}
                                        onDragOver={(e) => !isRandomizing && handleDragOver(e)}
                                        onDragEnter={() => !isRandomizing && handleDragEnter(stat)}
                                        onDragLeave={(e) => !isRandomizing && handleDragLeave(e)}
                                        onDrop={(e) => !isRandomizing && handleDrop(e, stat)}
                                        className={`assigned-stat-button ${val !== null ? "assigned" : ""
                                            } ${dragOverAbility === stat ? "drag-over" : ""} ${isRandomizing ? "disabled" : ""}`}
                                        disabled={isRandomizing}
                                    >
                                        <span className="stat-label">{stat.substring(0, 3).toUpperCase()}</span>
                                        <span className="stat-value">{val ?? "-"}</span>
                                    </button>
                                );
                            })}
                        </div>

                        <p><strong>Total = {abilityTotal}</strong></p>

                        <div className="navigation-buttons compact" style={{ marginTop: '15px' }}>
                            <button className="nav-button" onClick={() => setStep(0)} disabled={isRandomizing}>Back</button>
                            {/* Reset button only for new character */}
                            {!isEditMode && initialRolledStats.length > 0 && (
                                <button className="nav-button" onClick={resetStatAssignment} disabled={isRandomizing}>
                                    Reset Stats
                                </button>
                            )}
                            <button className="nav-button" disabled={!allStatsAssigned || isRandomizing} onClick={() => setStep(2)}>
                                Next
                            </button>
                        </div>
                    </div>
                );

            case 2:
                const speciesOptions = speciesData.map(s => s.name);
                const speciesVariants = selectedSpeciesDetails?.variations || [];
                const requiresVariant = speciesVariants.length > 0;

                return (
                    <div className="step-container step-2">
                        <h2>Select your Species</h2>
                        <div className="class-selection-layout">
                            <div className="class-list-column">
                                <div className="button-group">
                                    {speciesOptions.map(s => (
                                        <button
                                            key={s}
                                            data-species={s}
                                            onClick={() => {
                                                const details = speciesData.find(sd => sd.name === s);
                                                setFormData({
                                                    ...formData,
                                                    species: s,
                                                    species_variant: ""
                                                });
                                                setSelectedSpeciesDetails(details);
                                            }}
                                            className={`selection-button ${formData.species === s ? "selected" : ""}`}
                                        >
                                            {s}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div className="class-details-column">
                                {selectedSpeciesDetails ? (
                                    <>
                                        <div className="class-details-header">
                                            <h3>{selectedSpeciesDetails.name}</h3>
                                            <p className="species-summary-text">{selectedSpeciesDetails.summary}</p>
                                        </div>

                                        <div className="class-facts-grid">
                                            <div className="fact-item">
                                                <span className="fact-label">Creature Type</span>
                                                <span className="value-bubble">{selectedSpeciesDetails.creature_type}</span>
                                            </div>
                                            <div className="fact-item">
                                                <span className="fact-label">Size</span>
                                                <span className="value-bubble">
                                                    {Array.isArray(selectedSpeciesDetails.size)
                                                        ? (formData.size || selectedSpeciesDetails.size.join(" / "))
                                                        : selectedSpeciesDetails.size}
                                                </span>
                                            </div>
                                            <div className="fact-item">
                                                <span className="fact-label">Speed</span>
                                                <span className="value-bubble">{selectedSpeciesDetails.speed}</span>
                                            </div>
                                        </div>

                                        {Array.isArray(selectedSpeciesDetails.size) && (
                                            <div className="bg-choice-section">
                                                <h4>Select Size (Optional)</h4>
                                                <div className="skill-picker-grid">
                                                    {selectedSpeciesDetails.size.map(sz => (
                                                        <button
                                                            key={sz}
                                                            onClick={() => setFormData({ ...formData, size: formData.size === sz ? "" : sz })}
                                                            className={`skill-item-button ${formData.size === sz ? "selected" : ""}`}
                                                        >
                                                            {sz}
                                                        </button>
                                                    ))}
                                                </div>
                                            </div>
                                        )}

                                        {requiresVariant && (
                                            <div className="bg-choice-section">
                                                <h4>Select Heritage / Kindred</h4>
                                                <div className="skill-picker-grid">
                                                    {speciesVariants.map(v => (
                                                        <button
                                                            key={v}
                                                            onClick={() => setFormData({ ...formData, species_variant: v })}
                                                            className={`skill-item-button ${formData.species_variant === v ? "selected" : ""}`}
                                                        >
                                                            {v}
                                                        </button>
                                                    ))}
                                                </div>
                                            </div>
                                        )}

                                        <div className="level-preview-section">
                                            <h4>Species Traits</h4>
                                            {selectedSpeciesDetails.features.map(feature => (
                                                <div key={feature.id} className="feature-preview-card">
                                                    <h6>{feature.name}</h6>
                                                    <p>{feature.description}</p>
                                                    {feature.details && (
                                                        <div className="feature-details-mini">
                                                            {Object.entries(feature.details).map(([key, val]) => (
                                                                <span key={key} className="detail-tag">
                                                                    <strong>{key}:</strong> {typeof val === 'object' ? JSON.stringify(val) : val}
                                                                </span>
                                                            ))}
                                                        </div>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    </>
                                ) : (
                                    <div className="background-prompt">Select a species to see its traits and lore</div>
                                )}
                            </div>
                        </div>

                        {formData.species && (!requiresVariant || formData.species_variant) && (
                            <div className="navigation-buttons compact">
                                <button className="nav-button" onClick={() => setStep(1)}>Back</button>
                                <button className="nav-button" onClick={() => setStep(3)}>
                                    Next: Background
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
                                            data-bg={bg.name}
                                            onClick={() => setFormData({ ...formData, background: bg.name })}
                                            className={`background-button ${formData.background === bg.name ? "selected" : ""}`}
                                        >
                                            <strong>{bg.name}</strong>
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div className="equipment-details-column bg-choices-expanded">
                                {formData.background ? (
                                    <div className="bg-choices-container">
                                        {(() => {
                                            const selectedBg = backgrounds.find(bg => bg.name === formData.background);
                                            const standard = selectedBg?.starting_equipment?.standard;
                                            const goldOption = selectedBg?.starting_equipment?.gold_option || 50;
                                            const bgAbilities = selectedBg?.ability_scores || [];

                                            // Robust feat lookup for display
                                            let featData = null;
                                            if (selectedBg?.feat) {
                                                featData = feats.origin.find(f => f.name === selectedBg.feat);
                                                if (!featData) {
                                                    featData = feats.origin.find(f => {
                                                        const baseName = f.name.split(' {')[0];
                                                        return selectedBg.feat.includes(baseName);
                                                    });
                                                    if (featData && featData.name.includes("{variation}")) {
                                                        const variation = selectedBg.feat.match(/\(([^)]+)\)/)?.[1] || "";
                                                        featData = {
                                                            ...featData,
                                                            effects: featData.effects.map(e => e.replaceAll("{variation}", variation))
                                                        };
                                                    }
                                                }
                                            }

                                            return (
                                                <div className="bg-details-grid">
                                                    {/* 1. Stat Bonuses Section */}
                                                    <section className="bg-choice-section stat-bonuses">
                                                        <h4>Ability Score Bonuses</h4>
                                                        <div className="mode-toggle">
                                                            <button
                                                                className={`mode-btn ${bgChoices.mode === '2_1' ? 'active' : ''}`}
                                                                onClick={() => setBgChoices({ ...bgChoices, mode: '2_1' })}
                                                            >+2 / +1</button>
                                                            <button
                                                                className={`mode-btn ${bgChoices.mode === '1_1_1' ? 'active' : ''}`}
                                                                onClick={() => setBgChoices({ ...bgChoices, mode: '1_1_1' })}
                                                            >+1 / +1 / +1</button>
                                                        </div>

                                                        {bgChoices.mode === '2_1' ? (
                                                            <div className="bonus-pickers">
                                                                <div className="picker-row">
                                                                    <span>+2</span>
                                                                    <select className="bg-bonus-select-plus2" value={bgChoices.plus2} onChange={(e) => setBgChoices({ ...bgChoices, plus2: e.target.value })}>
                                                                        <option value="">Select Ability</option>
                                                                        {bgAbilities.map(a => <option key={a} value={a} disabled={a === bgChoices.plus1}>{a}</option>)}
                                                                    </select>
                                                                </div>
                                                                <div className="picker-row">
                                                                    <span>+1</span>
                                                                    <select className="bg-bonus-select-plus1" value={bgChoices.plus1} onChange={(e) => setBgChoices({ ...bgChoices, plus1: e.target.value })}>
                                                                        <option value="">Select Ability</option>
                                                                        {bgAbilities.map(a => <option key={a} value={a} disabled={a === bgChoices.plus2}>{a}</option>)}
                                                                    </select>
                                                                </div>
                                                            </div>
                                                        ) : (
                                                            <div className="bonus-pickers-111">
                                                                {bgAbilities.map(a => (
                                                                    <div key={a} className="fixed-bonus">
                                                                        <span>+1</span> <strong>{a}</strong>
                                                                    </div>
                                                                ))}
                                                                {/* Automatically set these stats in the bgChoices? 
                                                                    For 1_1_1 it's always the 3 listed stats. */}
                                                                {(() => {
                                                                    if (bgChoices.plus1_a !== bgAbilities[0]) {
                                                                        setBgChoices(prev => ({ ...prev, plus1_a: bgAbilities[0], plus1_b: bgAbilities[1], plus1_c: bgAbilities[2] }));
                                                                    }
                                                                    return null;
                                                                })()}
                                                            </div>
                                                        )}
                                                    </section>
                                                    <section className="bg-choice-section skill-proficiencies">
                                                        <h4>Skill Proficiencies</h4>
                                                        <div className="bg-skill-list">
                                                            {selectedBg?.skills?.map(skill => (
                                                                <span key={skill} className="bg-skill-tag">{skill}</span>
                                                            ))}
                                                        </div>
                                                    </section>

                                                    {/* 2. Origin Feat Section */}
                                                    <section className={`bg-choice-section origin-feat ${uiToggles.featExpanded ? 'expanded' : 'collapsed'}`}>
                                                        <div
                                                            className="section-header-toggle"
                                                            onClick={() => setUiToggles({ ...uiToggles, featExpanded: !uiToggles.featExpanded })}
                                                        >
                                                            <h4>Origin Feat: {selectedBg?.feat}</h4>
                                                            <span className="toggle-icon">{uiToggles.featExpanded ? '▼' : '▶'}</span>
                                                        </div>
                                                        {uiToggles.featExpanded && (
                                                            <div className="feat-effects-list">
                                                                {featData?.effects.map((eff, i) => (
                                                                    <p key={i}>{eff}</p>
                                                                ))}
                                                            </div>
                                                        )}
                                                    </section>

                                                    {/* 3. Equipment Choice Section */}
                                                    <section className="bg-choice-section equipment-select">
                                                        <h4>Starting Equipment</h4>
                                                        <div className="compact-equip-options">
                                                            <div className={`compact-option-wrapper ${formData.starting_equipment_choice === 'standard' ? 'selected' : ''}`}>
                                                                <label className="compact-label">
                                                                    <input
                                                                        type="radio"
                                                                        name="equipment"
                                                                        value="standard"
                                                                        checked={formData.starting_equipment_choice === "standard"}
                                                                        onChange={() => setFormData({ ...formData, starting_equipment_choice: "standard" })}
                                                                    />
                                                                    <span>Standard Package ({standard?.gold} GP + Items)</span>
                                                                </label>
                                                                <button
                                                                    className="expand-items-btn"
                                                                    onClick={(e) => {
                                                                        e.stopPropagation();
                                                                        setUiToggles({ ...uiToggles, equipExpanded: !uiToggles.equipExpanded });
                                                                    }}
                                                                >
                                                                    {uiToggles.equipExpanded ? 'Hide Items' : 'View Items'}
                                                                </button>
                                                            </div>

                                                            {uiToggles.equipExpanded && standard?.items && (
                                                                <div className="equipment-items-dropdown">
                                                                    <ul>
                                                                        {standard.items.map((item, idx) => (
                                                                            <li key={idx}>
                                                                                {item.name} {item.quantity > 1 && `(x${item.quantity})`}
                                                                            </li>
                                                                        ))}
                                                                    </ul>
                                                                </div>
                                                            )}

                                                            <label className={`compact-label ${formData.starting_equipment_choice === 'gold' ? 'active' : ''}`}>
                                                                <input
                                                                    type="radio"
                                                                    name="equipment"
                                                                    value="gold"
                                                                    checked={formData.starting_equipment_choice === "gold"}
                                                                    onChange={() => setFormData({ ...formData, starting_equipment_choice: "gold" })}
                                                                />
                                                                <span>Gold Only ({goldOption} GP)</span>
                                                            </label>
                                                        </div>
                                                    </section>
                                                </div>
                                            );
                                        })()}
                                    </div>
                                ) : (
                                    <div className="background-prompt">
                                        <p>Choose a background to customize your potential</p>
                                    </div>
                                )}
                            </div>
                        </div>

                        {formData.background && (
                            <div className="navigation-buttons compact">
                                <button className="nav-button" onClick={() => setStep(2)}>Back</button>
                                <button
                                    className="nav-button"
                                    disabled={
                                        bgChoices.mode === '2_1'
                                            ? (!bgChoices.plus2 || !bgChoices.plus1)
                                            : false // Mode 1_1_1 is auto-selected
                                    }
                                    onClick={() => setStep(4)}
                                >Next</button>
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
                                maxLength="30"
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
        <div className={`character-form-container ${isAutoRandomizing ? 'auto-randomizing' : ''}`}>
            <button 
                className={`global-randomize-btn ${isAutoRandomizing ? 'active' : ''}`}
                onClick={() => setIsAutoRandomizing(!isAutoRandomizing)}
            >
                {isAutoRandomizing ? "Stop Randomization 🛑" : "Randomize Character 🎲"}
            </button>
            <h1>{isEditMode ? "Edit Character" : "Create Character"}</h1>
            {renderStep()}
        </div>
    );
}

export default CharacterForm;