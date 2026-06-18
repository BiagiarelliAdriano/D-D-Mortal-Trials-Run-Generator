const FEATURE_BEHAVIORS = {
    activatable: {
        description: "Can be toggled on/off",
        type: "state"
    },

    uses: {
        description: "Has limited uses per rest",
        type: "resource"
    },

    advantage: {
        description: "Grants advantage to specific checks",
        type: "modifier"
    },

    damage_bonus: {
        description: "Adds bonus damage when conditons are met",
        type: "modifier"
    },

    resistance: {
        description: "Grants damage resistances while active",
        type: "defense"
    }
};

const BEHAVIOR_RESOLVERS = {
    activatable: (feature) => ({
        activatable: true
    }),

    uses: (feature, level) => {
        const usesData = feature.details?.uses;
        if (!usesData) return {};

        let value = null;

        for (const [range, v] of Object.entries(usesData)) {
            const [min, max] = range.split("-").map(Number);

            if (level >= min && level <= max) {
                value = v;
                break;
            }
        }

        return { maxUses: value };
    },

    advantage: (feature) => {
        const raw = feature.details?.Advantages;
        return {
            advantage: raw || null
        };
    },

    damage_bonus: (feature) => {
        const raw = feature.details?.["Rage Damage"];
        return {
            damageBonusTable: raw || null
        };
    },

    resistance: (feature) => {
        const raw = feature.details?.Resistances;
        return {
            resistances: typeof raw === "string" ? raw.split(", "): raw
        };
    }
};

export const resolveFeatureBehaviors = (feature, level = 1) => {
    if (!feature?.behaviors) return {};

    return feature.behaviors.reduce((acc, key) => {
        const fn = BEHAVIOR_RESOLVERS[key];
        if (!fn) return acc;

        return {
            ...acc,
            ...fn(feature, level)
        };
    }, {});
};

export default FEATURE_BEHAVIORS;