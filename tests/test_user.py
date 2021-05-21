import pytest
from faker import Faker
from fastapi import status

fake = Faker()

BASE_URL = "/api/users"


@pytest.fixture
def id_(client, basic_auth, user):
    response = client.post(
        headers=dict(Authorization=basic_auth),
        url=f"{BASE_URL}/",
        json=user,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    return data["id"]


def test_create_user(client, basic_auth, user):
    response = client.post(
        headers=dict(Authorization=basic_auth),
        url=f"{BASE_URL}/",
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
        url=f"{BASE_URL}/{id_}",
        json=dict(username=username, password=fake.pystr()),
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == id_
    assert data["username"] == username


def test_read_user_by_id(client, basic_auth, id_):
    response = client.get(
        headers=dict(Authorization=basic_auth),
        url=f"{BASE_URL}/{id_}",
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == id_
    assert "username" in data


def test_delete_user_by_id(client, basic_auth, id_):
    response = client.delete(
        headers=dict(Authorization=basic_auth),
        url=f"{BASE_URL}/{id_}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
