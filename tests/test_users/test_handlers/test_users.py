import json
import pytest


@pytest.mark.asyncio(loop_scope='module')
async def test_register(client, get_user_from_database):
    user_data = {
        "name": "Nikolai",
        "email": "lol@kek.com",
        "password": "SamplePass1!",
    }
    resp = client.post("/user/", content=json.dumps(user_data))

    assert resp.status_code == 200

    data_from_resp = resp.json()

    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True

    # users_from_db = await get_user_from_database(data_from_resp["user_id"])
    # assert len(users_from_db) == 1
    # user_from_db = dict(users_from_db[0])

    # assert user_from_db["name"] == user_data["name"]
    # assert user_from_db["email"] == user_data["email"]
    # assert user_from_db["is_active"] is True
    # assert str(user_from_db["user_id"]) == data_from_resp["user_id"]
