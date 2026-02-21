import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/CharactersHub.css";

function CharactersHub() {
    const [characters, setCharacters] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    // Fetch all characters from the API
    useEffect(() => {
        fetch("http://localhost:5000/api/characters")
            .then(res => res.json())
            .then(data => {
                setCharacters(data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Error fetching characters:", err);
                setLoading(false);
            });
    }, []);

    // Delete a character
    const deleteCharacter = (id, e) => {
        e.stopPropagation();
        if (!window.confirm("Are you sure you want to delete this character?")) return;

        fetch(`http://localhost:5000/api/characters/${id}`, {
            method: "DELETE"
        }).then(() => {
            // Remove deleted character from state
            setCharacters(prev => prev.filter(char => char.id !== id));
        });
    };

    if (loading) return <div className="loading-screen">Invoking the Mortal Hub...</div>;

    return (
        <div className="hub-container">
            <header className="hub-header">
                <h1>Characters Hub</h1>
                <button className="create-button" onClick={() => navigate("/characters/create")}>
                    ✧ Create New Ascendant
                </button>
            </header>

            <div className="character-grid">
                {characters.length === 0 ? (
                    <div className="empty-state">
                        <p>No ascendant have yet risen to the challenge.</p>
                        <button className="action-btn btn-view" onClick={() => navigate("/characters/create")}>
                            Begin Your Journey
                        </button>
                    </div>
                ) : (
                    characters.map(char => (
                        <div
                            key={char.id}
                            className="character-card"
                            onClick={() => navigate(`/characters/${char.id}`)}
                        >
                            <div className="card-header">
                                <h3>{char.name}</h3>
                            </div>
                            <div className="card-info">
                                <div>
                                    <span className="level-tag">Lvl {char.level}</span>
                                    <span>{char.class_name}</span>
                                </div>
                                <span>{char.species_variant ? `${char.species_variant} ` : ""}{char.species || "Unknown Species"}</span>
                            </div>
                            <div className="card-actions">
                                <button
                                    className="action-btn btn-view"
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        window.open(`/characters/${char.id}`, "_blank");
                                    }}
                                >
                                    👁 View
                                </button>
                                <button
                                    className="action-btn btn-edit"
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        navigate(`/characters/${char.id}/edit`);
                                    }}
                                >
                                    ✎ Edit
                                </button>
                                <button
                                    className="action-btn btn-delete"
                                    onClick={(e) => deleteCharacter(char.id, e)}
                                >
                                    🗑 Delete
                                </button>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}

export default CharactersHub;