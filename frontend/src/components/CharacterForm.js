import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

function CharacterForm() {
    const { id } = useParams();
    const isEditMode = Boolean(id);
    const navigate = useNavigate();

    const [loading, setLoading] = useState(isEditMode);
    const [step, setStep] = useState(0);
    const [formData, setFormData] = useState({
        name: "",
        class_name: "",
        subclass: "",
        level: 1,
        abilities: {
            strength: 10,
            dexterity: 10,
            constitution: 10,
            intelligence: 10,
            wisdom: 10,
            charisma: 10,
        },
    });

    const classes = [
        "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
        "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer",
        "Warlock", "Wizard"
    ];

    // Fetch character if editing
    useEffect(() => {
        if (!isEditMode) return;

        fetch(`http://localhost:5000/api/characters/${id}`)
            .then(res => res.json())
            .then(data => {
                setFormData({
                    name: data.name,
                    class_name: data.class.name,
                    subclass: data.class.subclass || "",
                    level: data.level,
                    abilities: data.data.abilities,
                });
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to load character", err);
                setLoading(false);
            });
    }, [id, isEditMode]);

    if (loading) return <div>Loading character...</div>;

    // Utility to roll 4d6 drop lowest
    const rollAbility = () => {
        const rolls = Array.from({ length: 4 }, () => Math.floor(Math.random() * 6) + 1);
        rolls.sort((a, b) => a - b); // ascending
        rolls.shift(); // remove lowest
        return rolls.reduce((a, b) => a + b, 0);
    };

    const rollAbilities = () => {
        const scores = {
            strength: rollAbility(),
            dexterity: rollAbility(),
            constitution: rollAbility(),
            intelligence: rollAbility(),
            wisdom: rollAbility(),
            charisma: rollAbility(),
        };
        setFormData({ ...formData, abilities: scores });
    };

    // Handle saving to backend
    const handleSubmit = () => {
        const url = isEditMode
            ? `http://localhost:5000/characters/${id}/edit`
            : "http://localhost:5000/characters/create";

        const payload = new FormData();
        payload.append("name", formData.name);
        payload.append("class_name", formData.class_name);
        payload.append("subclass", formData.subclass);
        payload.append("level", formData.level);

        fetch(url, { method: "POST", body: payload })
            .then(() => navigate("/"))
            .catch(err => console.error("Failed to save character", err));
    };

    // Render steps
    const renderStep = () => {
        switch (step) {
            case 0: // Class selection
                return (
                    <div>
                        <h2>Select a Class</h2>
                        {classes.map(c => (
                            <button
                                key={c}
                                onClick={() => setFormData({ ...formData, class_name: c })}
                                style={{
                                    margin: "5px",
                                    backgroundColor: formData.class_name === c ? "lightgreen" : "white"
                                }}
                            >
                                {c}
                            </button>
                        ))}
                        {formData.class_name && (
                            <div style={{ marginTop: "20px" }}>
                                <button onClick={() => setStep(step + 1)}>Next</button>
                            </div>
                        )}
                    </div>
                );
            
            case 1: // Ability score rolling
                return (
                    <div>
                        <h2>Roll Ability Scores</h2>
                        <button onClick={rollAbilities}>Roll 4d6 Drop Lowest</button>
                        <ul>
                            {Object.entries(formData.abilities).map(([key, val]) => (
                                <li key={key}>
                                    {key.charAt(0).toUpperCase() + key.slice(1)}: {val}
                                </li>
                            ))}
                        </ul>
                        <button style={{ marginTop: "20px" }} onClick={() => setStep(step + 1)}>Next</button>
                    </div>
                );
            
            case 2: // Name and Level
                return (
                    <div>
                        <h2>Character Info</h2>
                        <label>
                            Name:
                            <input
                                type="text"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            />
                        </label>
                        <br />
                        <label>
                            Level:
                            <input
                                type="number"
                                min="1"
                                max="20"
                                value={formData.level}
                                onChange={(e) => setFormData({ ...formData, level: parseInt(e.target.value) })}
                            />
                        </label>
                        <div style={{ marginTop: "20px"}}>
                            <button onClick={() => setStep(step - 1)}>Back</button>
                            <button onClick={() => handleSubmit()} style={{ marginLeft: "10px" }}>Save Character</button>
                        </div>
                    </div>
                );
            
            default:
                return <div>Unknown step</div>;
        }
    };

    return (
        <div>
            <h1>{isEditMode ? "Edit Character" : "Create Character"}</h1>
            {renderStep()}
        </div>
    );
}

export default CharacterForm;