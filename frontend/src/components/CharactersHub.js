import { useEffect, useState, useMemo, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../styles/CharactersHub.css";
import UserProfilePill from "./UserProfilePill";
import BackToTop from "./common/BackToTop";

function CharactersHub() {
    const [characters, setCharacters] = useState([]);
    const [loading, setLoading] = useState(true);
    const { token, user } = useAuth();
    const navigate = useNavigate();

    // Fetch function for polling
    const fetchCharacters = useCallback(() => {
        fetch("http://localhost:5000/api/characters", {
            headers: { 'Authorization': `Bearer ${token}` }
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

    // Initial fetch and polling setup
    useEffect(() => {
        fetchCharacters();
        const interval = setInterval(fetchCharacters, 5000); // Polling every 5s
        return () => clearInterval(interval);
    }, [fetchCharacters]);

    // Partition and Sort characters
    const { myCharacters, communityCharacters } = useMemo(() => {
        const mine = characters.filter(c => c.user_id === user?.id);
        const community = characters.filter(c => c.user_id !== user?.id);

        // Sort community characters by owner_username then name
        community.sort((a, b) => {
            const ownerCmp = a.owner_username.localeCompare(b.owner_username);
            if (ownerCmp !== 0) return ownerCmp;
            return a.name.localeCompare(b.name);
        });

        return { myCharacters: mine, communityCharacters: community };
    }, [characters, user]);

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
            fetchCharacters();
        });
    };

    const renderCharacterCard = (char, showAttribution) => (
        <div
            key={char.id}
            className="character-card"
            onClick={() => navigate(`/characters/${char.id}`)}
        >
            <div className="card-header">
                <h3>{char.name}</h3>
            </div>
            <div className="card-info">
                <div className="card-stats-row">
                    <span className="level-tag">Lvl {char.level}</span>
                    <span>{char.class_name}</span>
                </div>
                <div className="card-species-row">
                    <span>{char.species_variant ? `${char.species_variant} ` : ""}{char.species || "Unknown Species"}</span>
                    {showAttribution && (
                        <span className="owner-tag" title={`Created by ${char.owner_username}`}>
                            By: {char.owner_username}
                        </span>
                    )}
                </div>
            </div>
            {char.active_run_title && (
                <div className="active-run-badge">
                    <i className="fa-solid fa-dungeon"></i> {char.active_run_title}
                </div>
            )}
            <div className="card-actions">
                {(!char.is_private || char.user_id === user?.id || user?.is_admin) ? (
                    <button
                        className="action-btn btn-view"
                        onClick={(e) => {
                            e.stopPropagation();
                            window.open(`/characters/${char.id}`, "_blank");
                        }}
                    >
                        👁 View
                    </button>
                ) : (
                    <button
                        className="action-btn btn-private"
                        disabled
                        onClick={(e) => e.stopPropagation()}
                    >
                        🔒 Private
                    </button>
                )}

                {(char.user_id === user?.id || user?.is_admin) && (
                    <button
                        className="action-btn btn-edit"
                        onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/characters/${char.id}/edit`);
                        }}
                    >
                        ✎ Edit
                    </button>
                )}
                
                {(char.user_id === user?.id || user?.is_admin) && (
                    <button
                        className="action-btn btn-delete"
                        onClick={(e) => deleteCharacter(char.id, e)}
                    >
                        🗑 Delete
                    </button>
                )}
            </div>
        </div>
    );

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
                </div>

                <UserProfilePill />
            </header>

            <div className="hub-sections">
                {/* Section 1: My Characters */}
                <section className="hub-section">
                    <h2 className="hub-section-title">✧ Your Chosen Ascendants ✧</h2>
                    <div className="character-grid">
                        {myCharacters.length === 0 ? (
                            <div className="empty-state">
                                <p>You have not yet raised an ascendant to the challenge.</p>
                                <button className="action-btn btn-view" onClick={() => navigate("/characters/create")}>
                                    Begin Your Journey
                                </button>
                            </div>
                        ) : (
                            myCharacters.map(char => renderCharacterCard(char, false))
                        )}
                    </div>
                </section>

                {/* Section 2: Community Characters */}
                <section className="hub-section community-section">
                    <h2 className="hub-section-title">✧ Community Halls ✧</h2>
                    <div className="character-grid">
                        {communityCharacters.length === 0 ? (
                            <div className="empty-state">
                                <p>No other ascendants are currently resting in the halls.</p>
                            </div>
                        ) : (
                            communityCharacters.map(char => renderCharacterCard(char, true))
                        )}
                    </div>
                </section>
            </div>
            <BackToTop />
        </div>
    );
}

export default CharactersHub;