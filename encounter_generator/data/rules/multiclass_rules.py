# multiclass_rules.py

def check_multiclass_prerequisites(character_data, target_class, classes):
    """
    Checks 2024 D&D multiclass prerequisites.

    A character needs 13+ in:
    - the primary ability requirement of every existing class
    - the primary ability requirement of the new class

    Classes with multiple primary abilities use OR logic.
    Example:
    Fighter = Strength OR Dexterity
    """

    abilities = character_data.get("abilities", {})

    required_groups = []


    def add_class_requirement(class_rules):
        if not class_rules:
            return

        primary = class_rules.get("primary_ability")

        if not primary:
            return

        # Supports:
        # "Strength"
        # ["Strength", "Dexterity"]

        if isinstance(primary, list):
            required_groups.append(
                [ability.lower() for ability in primary]
            )
        else:
            required_groups.append(
                [primary.lower()]
            )


    # Existing classes
    class_levels = character_data.get("class_levels", [])

    for cls in class_levels:
        class_name = cls.get("class_name")

        class_rules = classes.get(class_name.lower())

        add_class_requirement(class_rules)


    # New multiclass class
    target_rules = classes.get(target_class.lower())

    add_class_requirement(target_rules)



    failed = []


    # Check each requirement group
    for group in required_groups:

        # At least one ability must be 13+
        meets_requirement = False

        available_scores = []

        for ability in group:
            score = abilities.get(ability, 0)

            available_scores.append(
                f"{ability.capitalize()} {score}"
            )

            if score >= 13:
                meets_requirement = True


        if not meets_requirement:

            if len(group) > 1:
                failed.append(
                    f"{' or '.join([a.capitalize() for a in group])} 13 required "
                    f"(Current: {', '.join(available_scores)})"
                )
            else:
                failed.append(
                    f"{group[0].capitalize()} 13 required "
                    f"(Current: {available_scores[0].split()[-1]})"
                )


    if failed:
        return {
            "allowed": False,
            "reason": failed
        }


    return {
        "allowed": True,
        "reason": None
    }