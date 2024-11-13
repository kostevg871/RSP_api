import json
import pytest

import warnings

warnings.filterwarnings("ignore", category=PendingDeprecationWarning)


@pytest.mark.asyncio(loop_scope='session')
async def test_create(client, get_user_from_database):
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
    assert data_from_resp["roles"] == ["ROLE_PORTAL_USER"]

    users_from_db = await get_user_from_database(data_from_resp["user_id"])

    assert len(users_from_db) == 1

    user_from_db = dict(users_from_db[0])

    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert user_from_db["user_id"] == data_from_resp["user_id"]
    assert user_from_db["roles"] == ["ROLE_PORTAL_USER"]


@pytest.mark.asyncio(loop_scope='session')
async def test_create_user_duplicate_email_error(client, get_user_from_database):
    user_data = {
        "name": "Ivan",
        "email": "lol@kek.com",
        "password": "SamplePass1!",
    }
    user_data_same = {
        "name": "Petr",
        "email": "lol@kek.com",
        "password": "SamplePass1!",
    }

    # Создаем первого пользователя
    resp = client.post("/user/", content=json.dumps(user_data))
    data_from_resp = resp.json()

    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True

    # Получаем пользователя из БД
    users_from_db = await get_user_from_database(data_from_resp["user_id"])

    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])  # Инициализация переменной

    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert user_from_db["user_id"] == data_from_resp["user_id"]
    assert user_from_db["roles"] == ["ROLE_PORTAL_USER"]

    # Пытаемся создать пользователя с дублирующим email
    resp = client.post("/user/", content=json.dumps(user_data_same))

    assert resp.status_code == 503
    assert (
        'Пользователь c такой почтой уже существует!'
        in resp.json()["detail"]
    )
