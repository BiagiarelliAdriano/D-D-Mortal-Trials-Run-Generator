const normalizeName = (value) => String(value || '').toLowerCase().replace(/[^a-z0-9]/g, '');

const getCharacterClassEntries = (character, classRules, allClassRules) => {
    const classEntries = character?.data?.class_levels;
    if (Array.isArray(classEntries) && classEntries.length > 0) {
        return classEntries.map(entry => {
            const className = entry.class_name?.toLowerCase();
            return {
                entry,
                rules: allClassRules?.[className] ||
                    (normalizeName(classRules?.name) === normalizeName(className) ? classRules : null)
            };
        });
    }

    const className = character?.class?.name || character?.data?.class_name;
    if (className) {
        const normalizedName = className.toLowerCase();
        return [{
            entry: {
                class_name: className,
                level: character.level || character.data?.level || 1,
                subclass: character.data?.subclass
            },
            rules: allClassRules?.[normalizedName] ||
                (normalizeName(classRules?.name) === normalizeName(className) ? classRules : null)
        }];
    }

    return classRules ? [{
        entry: {
            class_name: classRules.name,
            level: character?.level || character?.data?.level || 1,
            subclass: character?.data?.subclass
        },
        rules: classRules
    }] : [];
};

const hasClassFeature = (character, classRules, allClassRules, matcher) => {
    const entries = getCharacterClassEntries(character, classRules, allClassRules);
    const knownClassNames = new Set(entries.map(({ entry }) => normalizeName(entry.class_name)));

    if (
        classRules &&
        !knownClassNames.has(normalizeName(classRules.name))
    ) {
        entries.push({
            entry: {
                class_name: classRules.name,
                level: character?.level || character?.data?.level || 1,
                subclass: character?.data?.subclass
            },
            rules: classRules
        });
    }

    return entries.some(({ entry, rules }) => {
        if (!rules) return false;

        const classLevel = Number(entry.level) || 1;
        const classFeatures = Object.entries(rules.features || {})
            .filter(([featureLevel]) => Number(featureLevel) <= classLevel)
            .flatMap(([, features]) => Array.isArray(features) ? features : []);
        if (classFeatures.some(matcher)) return true;

        const subclassName = entry.subclass?.toLowerCase().replace(/\s+/g, '_');
        const subclass = subclassName && rules.subclasses?.[subclassName];
        const subclassFeatures = Object.entries(subclass?.features || {})
            .filter(([featureLevel]) => Number(featureLevel) <= classLevel)
            .flatMap(([, features]) => Array.isArray(features) ? features : []);
        return subclassFeatures.some(matcher);
    });
};

const getArmorTraining = (character, classRules, allClassRules, ruleOptions) => {
    const training = new Set();
    const addTraining = (values) => {
        if (!Array.isArray(values)) return;
        values.forEach(value => {
            const normalized = normalizeName(value);
            ['light', 'medium', 'heavy'].forEach(type => {
                if (normalized === type || normalized === `${type}armor`) {
                    training.add(type);
                }
            });
        });
    };

    addTraining(character?.data?.proficiencies?.armor);
    getCharacterClassEntries(character, classRules, allClassRules).forEach(({ entry, rules }, index) => {
        addTraining(index === 0
            ? rules?.proficiencies?.armor
            : rules?.multiclass_proficiencies?.armor);
    });

    const featPools = [
        ...(ruleOptions?.origin || []),
        ...(ruleOptions?.general || []),
        ...(ruleOptions?.fighting_style || []),
        ...(ruleOptions?.epic_boon || [])
    ];
    const selectedFeatNames = Object.entries(character?.data?.featureChoices || {})
        .filter(([choiceId]) => choiceId.includes('feat_or_asi') || choiceId.includes('epic_boon'))
        .flatMap(([, choices]) => Array.isArray(choices) ? choices : [choices])
        .filter(choice => typeof choice === 'string');
    const backgroundFeat = character?.data?.choices?.background_feat;
    if (typeof backgroundFeat?.name === 'string') {
        selectedFeatNames.push(backgroundFeat.name);
    }

    const selectedFeats = new Set(selectedFeatNames.map(normalizeName));
    featPools
        .filter(feat => selectedFeats.has(normalizeName(feat.name || feat.id)))
        .forEach(feat => {
            const effects = Array.isArray(feat.effects) ? feat.effects.join(' ') : '';
            const featText = `${feat.description || ''} ${effects}`;
            const gainedTraining = featText.match(/gain training with (Light|Medium|Heavy) armor/i);
            if (gainedTraining) addTraining([gainedTraining[1]]);
        });

    return training;
};

const hasArmorTraining = (character, classRules, allClassRules, ruleOptions, required) => {
    const training = getArmorTraining(character, classRules, allClassRules, ruleOptions);
    if (required === 'light') return training.size > 0;
    if (required === 'medium') return training.has('medium') || training.has('heavy');
    return training.has('heavy');
};

export const checkFeatPrerequisites = (
    prerequisite,
    character,
    level = 1,
    classRules = null,
    allClassRules = null,
    ruleOptions = null
) => {
    if (!prerequisite || !character) return null;

    const hasSpellcasting = () => (
        !!(character.class?.spellcasting || classRules?.spellcasting) ||
        getCharacterClassEntries(character, classRules, allClassRules)
            .some(({ rules }) => !!rules?.spellcasting) ||
        hasClassFeature(character, classRules, allClassRules, feature => {
            const name = normalizeName(feature.name);
            const id = normalizeName(feature.id);
            return name.includes('spellcasting') ||
                name.includes('pactmagic') ||
                id.includes('spellcasting') ||
                id.includes('pactmagic');
        })
    );

    const hasFightingStyle = () => hasClassFeature(
        character,
        classRules,
        allClassRules,
        feature => normalizeName(feature.name).includes('fightingstyle') ||
            normalizeName(feature.id).includes('fightingstyle')
    );

    const checkSingle = (requirement) => {
        if (typeof requirement !== 'string') return null;

        const levelMatch = requirement.match(/Level\s+(\d+)\+?/i);
        if (levelMatch && level < parseInt(levelMatch[1], 10)) {
            return requirement;
        }

        const abilityMatch = requirement.match(
            /(Strength|Dexterity|Constitution|Intelligence|Wisdom|Charisma)\s+(\d+)/i
        );
        if (abilityMatch) {
            const ability = abilityMatch[1].toLowerCase();
            const requiredScore = parseInt(abilityMatch[2], 10);
            const currentScore = character.data?.abilities?.[ability] ?? 10;
            if (currentScore < requiredScore) return requirement;
        }

        const normalizedRequirement = requirement.toLowerCase();
        if (
            normalizedRequirement.includes('spellcasting feature') ||
            normalizedRequirement.includes('pact magic feature')
        ) {
            return hasSpellcasting() ? null : requirement;
        }

        if (normalizedRequirement.includes('fighting style feature')) {
            return hasFightingStyle() ? null : requirement;
        }

        const armorMatch = normalizedRequirement.match(/(light|medium|heavy) armor training/);
        if (armorMatch && !hasArmorTraining(
            character, classRules, allClassRules, ruleOptions, armorMatch[1]
        )) {
            return requirement;
        }

        return null;
    };

    if (typeof prerequisite === 'string') return checkSingle(prerequisite);

    if (Array.isArray(prerequisite)) {
        const failed = [];
        for (const requirement of prerequisite) {
            if (Array.isArray(requirement)) {
                const anyMet = requirement.some(item => !checkSingle(item));
                if (!anyMet) failed.push(`(${requirement.join(' or ')})`);
            } else {
                const error = checkSingle(requirement);
                if (error) failed.push(error);
            }
        }
        return failed.length > 0 ? failed.join(' and ') : null;
    }

    return null;
};
