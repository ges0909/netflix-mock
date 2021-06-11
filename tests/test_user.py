import pytest
from faker import Faker
from fastapi import status

fake = Faker()

BASE_URL = "/api/users"


@pytest.fixture
def id_(client, api_user, fake_user):
    response = client.post(
        headers=dict(Authorization=api_user),
        url=f"{BASE_URL}",
        json=fake_user,
    )
    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    return data["id"]


def test_create_user(client, api_user, fake_user):
    response = client.post(
        headers=dict(Authorization=api_user),
        url=f"{BASE_URL}",
        json=fake_user,
    )
    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert data["id"] > 0
    assert data["username"] == fake_user["username"]
    assert "password" not in data
    assert data["email"] == fake_user["email"]
    assert data["first_name"] == fake_user["first_name"]
    assert data["last_name"] == fake_user["last_name"]


def test_update_user(client, api_user, id_):
    response = client.put(
        headers=dict(Authorization=api_user),
        url=f"{BASE_URL}/{id_}",
        json=dict(password=fake.pystr(min_chars=8, max_chars=16)),
    )
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == id_
    assert "password" not in data


def test_read_user_by_id(client, api_user, id_):
    response = client.get(
        headers=dict(Authorization=api_user),
        url=f"{BASE_URL}/{id_}",
    )
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == id_
    assert "username" in data


def test_delete_user_by_id(client, api_user, id_):
    response = client.delete(
        headers=dict(Authorization=api_user),
        url=f"{BASE_URL}/{id_}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
