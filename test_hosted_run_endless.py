import json
from app import app, db
from models import User, Character, Run, HostedRun, SessionParticipant
from encounter_generator.encounter_logic import generate_run_for_mode
from flask_jwt_extended import create_access_token


def run_tests():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

        import uuid
        uid = uuid.uuid4().hex[:6]
        # 1. Create DM user and player user
        dm = User(username=f"DM_{uid}", security_answer_hash="dummy")
        dm.set_password("pass123")
        db.session.add(dm)

        player = User(username=f"Hero_{uid}", security_answer_hash="dummy")
        player.set_password("pass123")
        db.session.add(player)
        db.session.commit()

        # 2. Create Character for player
        char = Character(
            name="Valeros",
            user_id=player.id
        )
        char.set_data({
            "name": "Valeros",
            "class_name": "Fighter",
            "subclass": "Champion",
            "level": 1,
            "xp": 0,
            "gold": 50,
            "inventory": []
        })
        db.session.add(char)
        db.session.commit()

        # 3. Create Endless Trials Run
        endless_data = generate_run_for_mode("endless_trials")
        endless_data["settings"] = {"party_size": 4}  # party size 4 with 1 player = 3 surplus gold shares
        run_obj = Run(
            title_run=f"Spire_{uid}",
            user_id=dm.id,
            data=json.dumps(endless_data)
        )
        db.session.add(run_obj)
        db.session.commit()

        # 4. Create HostedRun session through the API
        client = app.test_client()
        dm_token = create_access_token(identity=str(dm.id))
        player_token = create_access_token(identity=str(player.id))
        res_create = client.post(
            "/api/host/create",
            headers={"Authorization": f"Bearer {dm_token}"},
            json={"run_id": run_obj.id}
        )
        assert res_create.status_code == 201, res_create.get_json()
        session = db.session.get(HostedRun, res_create.get_json()["session_id"])
        assert session.rations == 1.0
        print("PASS: Endless hosted run starts with 1 ration")

        # Add Player participant
        player_part = SessionParticipant(
            user_id=player.id,
            hosted_run_id=session.id,
            character_id=char.id,
            role="Ascendant"
        )
        db.session.add(player_part)
        db.session.commit()

        # TEST A: Non-DM cannot complete monster
        res_non_dm = client.post(
            f"/api/host/{session.id}/complete-encounter",
            headers={"Authorization": f"Bearer {player_token}"},
            json={"cycle": 1, "monster_index": 0}
        )
        assert res_non_dm.status_code == 403, f"Expected 403, got {res_non_dm.status_code}"
        print("PASS: Non-DM cannot complete monsters")

        # TEST B: DM completes monster 0 in Cycle 1
        monster_0 = endless_data["cycles"][0]["monsters"][0]
        expected_xp = monster_0.get("xp", 0)
        expected_gold = monster_0.get("gold", 0)
        has_item = "item" in monster_0 and monster_0["item"]

        res_complete = client.post(
            f"/api/host/{session.id}/complete-encounter",
            headers={"Authorization": f"Bearer {dm_token}"},
            json={"cycle": 1, "monster_index": 0}
        )
        assert res_complete.status_code == 200, f"Expected 200, got {res_complete.status_code}: {res_complete.get_json()}"
        complete_json = res_complete.get_json()
        assert complete_json["monster_id"] == "c1_m0"
        print("PASS: DM successfully completed monster c1_m0")

        # Verify database state after monster 0 completion
        db.session.expire_all()
        session_db = db.session.get(HostedRun, session.id)
        completed_list = json.loads(session_db.completed_encounters)
        assert "c1_m0" in completed_list, f"c1_m0 not in {completed_list}"

        char_db = db.session.get(Character, char.id)
        char_data = char_db.get_data()
        assert char_data["xp"] == expected_xp, f"Expected XP {expected_xp}, got {char_data['xp']}"
        assert char_data["gold"] == 50 + expected_gold, f"Expected Gold {50 + expected_gold}, got {char_data['gold']}"

        # Check surplus gold in vault: party size 4 - 1 connected player = 3 surplus shares
        vault_gold = json.loads(session_db.vault_gold)
        if expected_gold > 0:
            assert len(vault_gold) >= 1
            assert vault_gold[-1]["amount"] == expected_gold
            assert vault_gold[-1]["count"] == 3
            print(f"PASS: Surplus gold ({expected_gold} GP x3) correctly deposited to Vault")

        # Check item in party inventory (vault)
        party_inv = json.loads(session_db.party_inventory)
        if has_item:
            assert len(party_inv) >= 1
            assert party_inv[-1]["name"] == monster_0["item"]["name"]
            print(f"PASS: Monster loot item '{monster_0['item']['name']}' correctly added to Vault")

        # TEST C: Repeating the same monster returns already_completed
        res_repeat = client.post(
            f"/api/host/{session.id}/complete-encounter",
            headers={"Authorization": f"Bearer {dm_token}"},
            json={"cycle": 1, "monster_index": 0}
        )
        assert res_repeat.status_code == 200
        assert res_repeat.get_json().get("already_completed") is True
        print("PASS: Repeated completion returns already_completed")

        # TEST D: Claim item from vault
        if has_item:
            item_idx = len(party_inv) - 1
            res_claim = client.post(
                f"/api/host/{session.id}/claim-item",
                headers={"Authorization": f"Bearer {player_token}"},
                json={"item_index": item_idx}
            )
            assert res_claim.status_code == 200, f"Failed to claim item: {res_claim.get_json()}"
            char_data_updated = db.session.get(Character, char.id).get_data()
            assert any(it.get("name") == monster_0["item"]["name"] for it in char_data_updated.get("inventory", []))
            print("PASS: Player successfully claimed monster item from Vault")

        # TEST E: Claim gold share from vault
        if expected_gold > 0:
            res_claim_gold = client.post(
                f"/api/host/{session.id}/claim-gold",
                headers={"Authorization": f"Bearer {player_token}"},
                json={"share_index": 0}
            )
            assert res_claim_gold.status_code == 200, f"Failed to claim gold: {res_claim_gold.get_json()}"
            char_data_gold = db.session.get(Character, char.id).get_data()
            assert char_data_gold["gold"] == 50 + expected_gold + expected_gold
            print("PASS: Player successfully claimed surplus gold share from Vault")

        # TEST F: Archiving prematurely fails
        res_premature_archive = client.post(
            f"/api/host/{session.id}/complete",
            headers={"Authorization": f"Bearer {dm_token}"}
        )
        assert res_premature_archive.status_code == 400
        assert "All encounters must be completed" in res_premature_archive.get_json().get("error", "")
        print("PASS: Premature archiving correctly rejected")

        # TEST G: Cycle shops refresh rations to fixed values
        all_monsters = []
        for c in endless_data["cycles"]:
            for m_i, _ in enumerate(c.get("monsters", [])):
                all_monsters.append(f"c{c['cycle']}_m{m_i}")

        prior_cycle_monsters = []
        expected_shop_rations = {1: 1.0, 2: 2.0, 3: 2.0}
        for cycle in endless_data["cycles"][:3]:
            cycle_num = cycle["cycle"]
            monster_count = len(cycle["monsters"])
            completed_before_last = prior_cycle_monsters + [
                f"c{cycle_num}_m{i}" for i in range(monster_count - 1)
            ]
            session_db = db.session.get(HostedRun, session.id)
            session_db.completed_encounters = json.dumps(completed_before_last)
            session_db.rations = 77.5
            session_db.shop_state = None
            db.session.commit()

            last_index = monster_count - 1
            res_shop = client.post(
                f"/api/host/{session.id}/complete-encounter",
                headers={"Authorization": f"Bearer {dm_token}"},
                json={"cycle": cycle_num, "monster_index": last_index}
            )
            assert res_shop.status_code == 200, res_shop.get_json()
            assert res_shop.get_json()["shop_started"] is True
            db.session.expire_all()
            session_db = db.session.get(HostedRun, session.id)
            expected_rations = expected_shop_rations[cycle_num]
            assert session_db.rations == expected_rations
            shop_state = json.loads(session_db.shop_state)
            assert shop_state["cycle"] == cycle_num
            print(f"PASS: Cycle {cycle_num} shop resets rations to {expected_rations:g}")

            prior_cycle_monsters += [
                f"c{cycle_num}_m{i}" for i in range(monster_count)
            ]

        session_db = db.session.get(HostedRun, session.id)
        session_db.completed_encounters = json.dumps(all_monsters)
        db.session.commit()

        res_archive = client.post(
            f"/api/host/{session.id}/complete",
            headers={"Authorization": f"Bearer {dm_token}"}
        )
        assert res_archive.status_code == 200, f"Expected 200 on archive, got {res_archive.status_code}"
        assert res_archive.get_json().get("is_completed") is True
        assert db.session.get(HostedRun, session.id).is_completed is True
        print("PASS: Archiving succeeds once all monsters in Endless Trials are completed")

        # TEST H: Cannot complete monster on archived session
        res_post_archive = client.post(
            f"/api/host/{session.id}/complete-encounter",
            headers={"Authorization": f"Bearer {dm_token}"},
            json={"cycle": 1, "monster_index": 1}
        )
        assert res_post_archive.status_code == 400
        assert "completed and archived" in res_post_archive.get_json().get("error", "")
        print("PASS: Completed session rejects further monster completions")

        # TEST I: Regression check - standard Mortal Trials run encounter completion
        mortal_data = generate_run_for_mode("mortal_trials")
        mortal_run = Run(
            title_run=f"Mortal_{uid}",
            user_id=dm.id,
            data=json.dumps(mortal_data)
        )
        db.session.add(mortal_run)
        db.session.commit()

        mortal_session = HostedRun(
            invite_code=f"m_{uid}",
            dm_id=dm.id,
            run_id=mortal_run.id,
            party_inventory="[]",
            vault_gold="[]",
            completed_encounters="[]",
            rations=3.0
        )
        db.session.add(mortal_session)
        db.session.commit()

        dm_mortal_part = SessionParticipant(
            user_id=dm.id,
            hosted_run_id=mortal_session.id,
            role="DM"
        )
        player_mortal_part = SessionParticipant(
            user_id=player.id,
            hosted_run_id=mortal_session.id,
            character_id=char.id,
            role="Ascendant"
        )
        db.session.add_all([dm_mortal_part, player_mortal_part])
        db.session.commit()

        res_mortal_enc = client.post(
            f"/api/host/{mortal_session.id}/complete-encounter",
            headers={"Authorization": f"Bearer {dm_token}"},
            json={"encounter_num": "1"}
        )
        assert res_mortal_enc.status_code == 200, f"Expected 200 on mortal encounter completion, got {res_mortal_enc.status_code}"
        mortal_session_db = db.session.get(HostedRun, mortal_session.id)
        assert "1" in json.loads(mortal_session_db.completed_encounters)
        print("PASS: Standard Mortal Trials encounter completion works as expected")

        print("\n>>> ALL ENDLESS & MORTAL TRIALS TESTS PASSED! <<<")


if __name__ == "__main__":
    run_tests()
