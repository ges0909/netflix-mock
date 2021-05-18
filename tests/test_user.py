from base64 import b64encode

import pytest
from faker import Faker
from fastapi import status

fake = Faker()


@pytest.fixture
def user():
    return dict(
        username=fake.pystr(),
        password=fake.pystr(),
    )


@pytest.fixture
def id_(client, basic_auth, user):
    response = client.post(
        headers=dict(Authorization=basic_auth),
        url="/users/",
        json=user,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    return data["id"]


def test_create_user(client, basic_auth, user):
    response = client.post(
        headers=dict(Authorization=basic_auth),
        url="/users/",
        json=user,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["id"] > 0
    assert "username" in data
    assert data["username"] == user["username"]


def test_update_user(client, basic_auth, id_):
    username = fake.pystr()
    response = client.put(
        headers=dict(Authorization=basic_auth),
        url=f"/users/{id_}",
        json=dict(username=username, password=fake.pystr()),
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == id_
    assert data["username"] == username


def test_read_user_by_id(client, basic_auth, id_):
    response = client.get(
        headers=dict(Authorization=basic_auth),
        url=f"/users/{id_}",
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == id_
    assert "username" in data


def test_delete_user_by_id(client, basic_auth, id_):
    response = client.delete(
        headers=dict(Authorization=basic_auth),
        url=f"/users/{id_}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_missing_auth(client, user):
    response = client.post(
        url="/users/",
        json=user,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Not authenticated"


@pytest.mark.parametrize(
    "basic_auth",
    [
        "Basic " + b64encode(b"WRONG:test").decode("ascii"),
        "Basic " + b64encode(b"test:WRONG").decode("ascii"),
    ],
)
def test_wrong_basic_auth(client, basic_auth, user):
    response = client.post(
        headers=dict(Authorization=basic_auth),
        url="/users/",
        json=user,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "Incorrect username or password"
