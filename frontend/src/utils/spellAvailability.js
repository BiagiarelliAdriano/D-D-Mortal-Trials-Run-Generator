const collectStringValues = (value, values) => {
    if (typeof value === 'string') {
        values.add(value.trim());
    } else if (Array.isArray(value)) {
        value.forEach(item => collectStringValues(item, values));
    } else if (value && typeof value === 'object') {
        Object.values(value).forEach(item => collectStringValues(item, values));
    }
};

export const getCharacterSpellSources = (characterData = {}) => {
    const sources = new Set();
    collectStringValues(characterData.species, sources);
    collectStringValues(characterData.species_variant, sources);
    collectStringValues(characterData.featureChoices, sources);
    collectStringValues(characterData.choices, sources);
    collectStringValues(characterData.feats, sources);
    return [...sources].filter(Boolean);
};

export const buildSpellAvailabilityQuery = (classEntry, classRules, characterData) => {
    const params = new URLSearchParams();
    const className = classEntry?.class_name?.toLowerCase();
    const subclassId = classEntry?.subclass?.toLowerCase();
    if (subclassId) {
        const subclassName = classRules?.subclasses?.[subclassId]?.name || subclassId.replace(/_/g, ' ');
        params.set('subclass', subclassName);
    }

    const characterSpells = characterData?.spells;
    const selectedSpells = Array.isArray(characterSpells)
        ? (!characterData?.class_levels?.length || characterData.class_levels.length <= 1 ? characterSpells : [])
        : characterSpells?.[className] || [];
    const selectedSpellNames = new Set(Array.isArray(selectedSpells) ? selectedSpells : []);
    if (className === 'wizard') {
        const wizardSpellbook = characterSpells?.wizard_spellbook;
        if (Array.isArray(wizardSpellbook)) {
            wizardSpellbook.forEach(name => selectedSpellNames.add(name));
        }
    }
    selectedSpellNames.forEach(name => params.append('selected', name));

    const spellSources = getCharacterSpellSources(characterData);
    const hasClassSpecificMagicInitiate = spellSources.some(source =>
        /^magic initiate \((?:artificer|barbarian|bard|cleric|druid|fighter|monk|paladin|ranger|rogue|sorcerer|warlock|wizard)\)$/i.test(source)
    );
    spellSources
        .filter(source => source.toLowerCase() !== 'magic initiate' || !hasClassSpecificMagicInitiate)
        .forEach(source => {
            params.append('source', source);
        });
    const query = params.toString();
    return query ? `?${query}` : '';
};
