import { BrowserRouter, Routes, Route } from "react-router-dom";
import CharactersHub from "./components/CharactersHub";
import CharacterSheet from "./components/CharacterSheet";
import CharacterForm from "./components/CharacterForm";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CharactersHub />} />
        <Route path="/characters/:id" element={<CharacterSheet />} />
        <Route path="/characters/create" element={<CharacterForm />} />
        <Route path="/characters/:id/edit" element={<CharacterForm />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;