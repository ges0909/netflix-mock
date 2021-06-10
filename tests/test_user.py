import pytest
from faker import Faker
from fastapi import status

fake = Faker()

BASE_URL = "/api/users"


@pytest.fixture
def id_(client, api_user, user_data):
    response = client.post(
        headers=dict(Authorization=api_user),
        url=f"{BASE_URL}",
        json=user_data,
    )
    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    return data["id"]


def test_create_user(client, api_user, user_data):
    response = client.post(
        headers=dict(Authorization=api_user),
        url=f"{BASE_URL}",
        json=user_data,
    )
    data = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert data["id"] > 0
    assert data["username"] == user_data["username"]
    assert "password" not in data
    assert data["email"] == user_data["email"]
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]


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
