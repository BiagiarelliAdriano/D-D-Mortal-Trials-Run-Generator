export function getSpeciesDamageType(species, variant) {
    if (typeof variant !== "string" || !variant) return null;

    const damageTypeRows = species?.features
        ?.find(feature => feature.id === "dragonborn_draconic_ancestry")
        ?.details?.["Damage Types"]?.rows;

    if (!Array.isArray(damageTypeRows)) return null;

    const selectedRow = damageTypeRows.find(
        row => Array.isArray(row) &&
            typeof row[0] === "string" &&
            row[0].toLowerCase() === variant.toLowerCase()
    );

    return typeof selectedRow?.[1] === "string" ? selectedRow[1] : null;
}

export function resolveSpeciesFeature(feature, species, variant) {
    const damageType = getSpeciesDamageType(species, variant) || "Draconic Ancestry";

    const resolveValue = value => {
        if (typeof value === "string") {
            return value.replaceAll("{damage_type}", damageType);
        }
        if (Array.isArray(value)) {
            return value.map(resolveValue);
        }
        if (value && typeof value === "object") {
            return Object.fromEntries(
                Object.entries(value).map(([key, nestedValue]) => [
                    key,
                    resolveValue(nestedValue),
                ])
            );
        }
        return value;
    };

    return resolveValue(feature);
}
