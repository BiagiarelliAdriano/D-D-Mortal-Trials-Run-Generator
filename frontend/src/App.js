import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [character, setCharacter] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:5000/api/characters/3")
      .then(res => res.json())
      .then(data => {
        setCharacter(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>
  if (!character) return <div>Erorr fetching character</div>;

  // Abilities are stored in character.data
  const abilities = [
    { name: "Strength", key: "strength" },
    { name: "Dexterity", key: "dexterity" },
    { name: "Constitution", key: "constitution" },
    { name: "Intelligence", key: "intelligence" },
    { name: "Wisdom", key: "wisdom" },
    { name: "Charisma", key: "charisma" },
  ];

  return (
    <div className="App">
      <h1>{character.name}</h1>
      <h2>Abilities</h2>
      <ul>
        {abilities.map(ability => (
          <li key={ability.key}>
            {ability.name}: {character.data[ability.key] || 0}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;