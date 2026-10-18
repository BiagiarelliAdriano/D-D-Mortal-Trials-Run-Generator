import { getSpeciesDamageType, resolveSpeciesFeature } from "./species";

const dragonborn = {
    features: [
        {
            id: "dragonborn_draconic_ancestry",
            details: {
                "Damage Types": {
                    headers: ["Dragon", "Damage Type"],
                    rows: [
                        ["Black", "Acid"],
                        ["Blue", "Lightning"],
                        ["Green", "Poison"],
                        ["Silver", "Cold"],
                    ],
                },
            },
        },
    ],
};

test("returns the selected Dragonborn ancestry damage type", () => {
    expect(getSpeciesDamageType(dragonborn, "Blue")).toBe("Lightning");
    expect(getSpeciesDamageType(dragonborn, "green")).toBe("Poison");
});

test("returns null when no matching ancestry damage type exists", () => {
    expect(getSpeciesDamageType(dragonborn, "")).toBeNull();
    expect(getSpeciesDamageType(dragonborn, "Gold")).toBeNull();
});

test("resolves ancestry damage type in feature descriptions and detail values", () => {
    const feature = {
        description: "You have Resistance to {damage_type} damage.",
        details: { "Damage Type": "{damage_type}" },
    };

    expect(resolveSpeciesFeature(feature, dragonborn, "Blue")).toEqual({
        description: "You have Resistance to Lightning damage.",
        details: { "Damage Type": "Lightning" },
    });
    expect(resolveSpeciesFeature(feature, dragonborn, "")).toEqual({
        description: "You have Resistance to Draconic Ancestry damage.",
        details: { "Damage Type": "Draconic Ancestry" },
    });
});
