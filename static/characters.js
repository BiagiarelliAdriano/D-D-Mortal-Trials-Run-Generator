// Mode flags
let editMode = false;
let deleteMode = false;

// DOM elements
const listEl = document.getElementById("characterList");
const createBtn = document.getElementById("createCharacterBtn");
const editBtn = document.getElementById("editModeBtn");
const deleteBtn = document.getElementById("deleteModeBtn");

const modal = document.getElementById("characterModal");
const saveBtn = document.getElementById("saveCharacterBtn");
const cancelBtn = document.getElementById("cancelCharacterBtn");

let editingCharId = null; // Track which character is being edited

// Parse character data from container attributes
const charactersData = JSON.parse(listEl.dataset.characters || "[]").map(item => {
    return typeof item === "string" ? JSON.parse(item) : item;
});
const characterNames = JSON.parse(listEl.dataset.names || "[]");
const characterIds = JSON.parse(listEl.dataset.ids || "[]");

const characters = characterIds.map((id, index) => ({
    id,
    name: characterNames[index],
    data: charactersData[index]
}));

// Show/hide modal
function showModal() { modal.classList.remove("hidden"); }
function hideModal() {
    modal.classList.add("hidden");
    document.getElementById("charName").value = "";
    document.getElementById("charClass").value = "";
    document.getElementById("charSubclass").value = "";
    document.getElementById("charLevel").value = 1;
    editingCharId = null;
}

// Toggle modes
function toggleEditMode() { editMode = !editMode; deleteMode = false; renderCharacters(); }
function toggleDeleteMode() { deleteMode = !deleteMode; editMode = false; renderCharacters(); }

// Render characters dynamically
function renderCharacters() {
    listEl.innerHTML = "";

    characters.forEach(char => {
        const card = document.createElement("div");
        card.className = "character-card";
        card.dataset.id = char.id;

        card.innerHTML = `
            <h3>${char.name}</h3>
            <p><strong>Class:</strong> ${char.data.class_name}</p>
            <p><strong>Subclass:</strong> ${char.data.subclass}</p>
            <p><strong>Level:</strong> ${char.data.level}</p>
        `;

        if (editMode) {
            const pen = document.createElement("span");
            pen.className = "icon-edit";
            pen.innerHTML = "✏️";
            pen.onclick = () => editCharacter(char.id, char.name, char.data);
            card.appendChild(pen);
        }

        if (deleteMode) {
            const cross = document.createElement("span");
            cross.className = "icon-delete";
            cross.innerHTML = "❌";
            cross.onclick = () => deleteCharacter(char.id);
            card.appendChild(cross);
        }

        if (!editMode && !deleteMode) {
            card.onclick = () => window.open(`/characters/${char.id}`, "_blank");
        }

        listEl.appendChild(card);
    });
}

// Save or update character
function saveCharacter() {
    const name = document.getElementById("charName").value;
    const className = document.getElementById("charClass").value;
    const subclass = document.getElementById("charSubclass").value;
    const level = document.getElementById("charLevel").value;

    const formData = new FormData();
    formData.append("name", name);
    formData.append("class_name", className);
    formData.append("subclass", subclass);
    formData.append("level", level);

    if (editingCharId) {
        fetch(`/characters/${editingCharId}/edit`, {
            method: "POST",
            body: formData
        }).then(() => window.location.reload());
    } else {
        fetch("/characters/create", {
            method: "POST",
            body: formData
        }).then(() => window.location.reload());
    }

    hideModal();
}

// Prefill modal with data for editing
function editCharacter(charId, charName, charData) {
    document.getElementById("charName").value = charName;
    document.getElementById("charClass").value = charData.class_name;
    document.getElementById("charSubclass").value = charData.subclass;
    document.getElementById("charLevel").value = charData.level;

    editingCharId = charId;
    showModal();
}

// Delete character
function deleteCharacter(charId) {
    if (confirm("Are you sure you want to delete this character?")) {
        fetch(`/characters/${charId}/delete`, { method: "POST" })
            .then(() => window.location.reload());
    }
}

// Event listeners
createBtn.onclick = showModal;
editBtn.onclick = toggleEditMode;
deleteBtn.onclick = toggleDeleteMode;
cancelBtn.onclick = hideModal;
saveBtn.onclick = saveCharacter;

// Initial render
renderCharacters();
