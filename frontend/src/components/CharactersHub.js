import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../styles/CharactersHub.css";
import UserProfilePill from "./UserProfilePill";

function CharactersHub() {
    const [characters, setCharacters] = useState([]);
    const [loading, setLoading] = useState(true);
    const { user, token } = useAuth();
    const navigate = useNavigate();

    // Fetch all characters from the API
    useEffect(() => {
        fetch("http://localhost:5000/api/characters", {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
            .then(res => res.json())
            .then(data => {
                setCharacters(data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Error fetching characters:", err);
                setLoading(false);
            });
    }, [token]);

    // Delete a character
    const deleteCharacter = (id, e) => {
        e.stopPropagation();
        if (!window.confirm("Are you sure you want to delete this character?")) return;

        fetch(`http://localhost:5000/api/characters/${id}`, {
            method: "DELETE",
            headers: {
                'Authorization': `Bearer ${token}`
            }
        }).then(() => {
            // Remove deleted character from state
            setCharacters(prev => prev.filter(char => char.id !== id));
        });
    };

    if (loading) return <div className="loading-screen">Invoking the Mortal Hub...</div>;

    return (
        <div className="hub-container">
            <header className="hub-header">
                <div className="hub-titles">
                    <h1>Characters Hub</h1>
                    <button className="create-button" onClick={() => navigate("/characters/create")}>
                        ✧ Create New Ascendant
                    </button>
                    <button className="create-button secondary-hub-btn" onClick={() => navigate("/")}>
                        <i className="fa-solid fa-house"></i> Home
                    </button>
                    {user?.is_admin && (
                        <button className="create-button admin-button" onClick={() => navigate("/admin")}>
                            ♚ Admin Dashboard
                        </button>
                    )}
                </div>

                <UserProfilePill />
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
                            {char.active_run_title && (
                                <div className="active-run-badge">
                                    <i className="fa-solid fa-dungeon"></i> {char.active_run_title}
                                </div>
                            )}
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