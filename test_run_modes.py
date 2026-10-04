from encounter_generator.generator import generate_divine_blessing
from encounter_generator.encounter_logic import (
    ENDLESS_CYCLE_ENCOUNTERS,
    build_endless_trials_run,
    generate_run_for_mode,
)


def test_endless_blessing_only_for_endless_trials():
    blessing = generate_divine_blessing("endless_trials")
    assert blessing["name"] == "Endless"


def test_mortal_trials_blessing_never_uses_endless_blessing():
    for _ in range(40):
        blessing = generate_divine_blessing("mortal_trials")
        assert blessing["name"] != "Endless"


def test_endless_trials_run_has_cycle_structure():
    run = generate_run_for_mode("endless_trials")
    assert run["mode"] == "The Endless Trials"
    assert len(run["cycles"]) == 4
    assert all(len(cycle["monsters"]) > 0 for cycle in run["cycles"])


def test_endless_trials_preserves_encounter_cr_order_and_rewards():
    run = build_endless_trials_run()

    for cycle_number, cycle in enumerate(run["cycles"], start=1):
        monsters = cycle["monsters"]
        cursor = 0

        for encounter_number, encounter in enumerate(
            ENDLESS_CYCLE_ENCOUNTERS[cycle_number],
            start=1,
        ):
            cr_sequence, xp, gold, rarities = encounter[:4]
            group = monsters[cursor:cursor + len(cr_sequence)]
            cursor += len(cr_sequence)

            assert [monster["encounter_number"] for monster in group] == [encounter_number] * len(group)
            assert all(
                monster["cr"] in (set(cr) if isinstance(cr, tuple) else {cr})
                for monster, cr in zip(group, cr_sequence)
            )
            assert all(monster.get("xp") == xp and monster.get("gold") == gold for monster in group)
            assert all(
                monster.get("item", {}).get("rarity") in rarities
                for monster in group
            ) if rarities else all("item" not in monster for monster in group)

        assert cursor == len(monsters)


def test_endless_shops_use_standard_run_shop_rewards():
    run = build_endless_trials_run()

    assert [cycle["shop"]["total_gold"] for cycle in run["cycles"][:3]] == [600, 6200, 58000]
    assert all(cycle["shop"]["rest"] == "Long Rest" for cycle in run["cycles"][:3])
    assert run["cycles"][3]["shop"] is None


def test_cycle_two_encounter_nine_has_two_very_rare_item_options():
    run = build_endless_trials_run()
    encounter_nine = [
        monster
        for monster in run["cycles"][1]["monsters"]
        if monster["encounter_number"] == 9
    ]
    assert len(encounter_nine) == 4
    assert all(monster["item"]["rarity"] == "very rare" for monster in encounter_nine)
    assert all(len(monster["item"]["name"].split(" / ")) == 2 for monster in encounter_nine)
    assert all("encounter_reward_options" not in monster for monster in encounter_nine)
