import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function CharacterSheet() {
    const { id } = useParams();
    const [character, setCharacter] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`http://localhost:5000/api/characters/${id}`)
            .then(res => res.json())
            .then(data => {
                setCharacter(data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }, [id]);

    if (loading) return <div>Loading...</div>
    if (!character) return <div>Error fetching character</div>;

    const abilities = [
        { name: "Strength", key: "strength" },
        { name: "Dexterity", key: "dexterity" },
        { name: "Constitution", key: "constitution" },
        { name: "Intelligence", key: "intelligence" },
        { name: "Wisdom", key: "wisdom" },
        { name: "Charisma", key: "charisma" },
    ];

    function abilityModifier(score) {
        return Math.floor((score - 10) / 2);
    }

    function proficiencyBonus(level) {
        if (level >= 17) return 6;
        if (level >= 13) return 5;
        if (level >= 9) return 4;
        if (level >= 5) return 3;
        return 2;
    }

    const proficientSaves = ["strength", "constitution"];

    return (
        <div>
            <h1>{character.name}</h1>
            <h2>Proficiency Bonus: +{proficiencyBonus(character.level)}</h2>

            <h2>Abilities</h2>
            <ul>
                {abilities.map(a => (
                    <li key={a.key}>
                        {a.name}: {character.data.abilities[a.key]} (
                            {abilityModifier(character.data.abilities[a.key]) >= 0 ? "+" : ""}
                            {abilityModifier(character.data.abilities[a.key])})
                    </li>
                ))}
            </ul>

            <h2>Saving Throws</h2>
            <ul>
                {abilities.map(save => {
                    const base = abilityModifier(character.data.abilities[save.key]);
                    const total = base + (proficientSaves.includes(save.key)
                        ? proficiencyBonus(character.level)
                        : 0);

                    return (
                        <li key={save.key}>
                            {save.name}: {total >= 0 ? "+" : ""}{total}
                        </li>
                    );
                })}
            </ul>
        </div>
    );
}

export default CharacterSheet;