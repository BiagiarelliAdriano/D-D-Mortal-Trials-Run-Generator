import { useEffect, useState } from "react";

function CharactersHub() {
    const [characters, setCharacters] = useState([]);
    const [loading, setLoading] = useState(true);

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
    const deleteCharacter = (id) => {
        if (!window.confirm("Are you sure you want to delete this character?")) return;

        fetch(`http://localhost:5000/api/characters/${id}`, {
            method: "DELETE"
        }).then(() => {
            // Remove deleted character from state
            setCharacters(prev => prev.filter(char => char.id !== id));
        });
    };

    if (loading) return <div>Loading characters...</div>
    if (!characters.length) return <div>No characters found.</div>

    return (
        <div>
            <h1>Characters Hub</h1>
            <ul>
                {characters.map(char => (
                    <li key={char.id} style={{ marginBottom: "10px" }}>
                        <strong>{char.name}</strong> - {char.class_name} (Level {char.level})
                        <div style={{ display: "inline-block", marginLeft: "10px"}}>
                            <button onClick={() => window.open(`/characters/${char.id}`, "_blank")}>
                                View
                            </button>
                            <button onClick={() => window.location.href = `/characters/${char.id}/edit`}>
                                Edit
                            </button>
                            <button onClick={() => deleteCharacter(char.id)}>
                                Delete
                            </button>
                        </div>
                    </li>
                ))}
            </ul>
            <button onClick={() => window.location.href = "/characters/create"}>
                + Create New Character
            </button>
        </div>
    );
}

export default CharactersHub;