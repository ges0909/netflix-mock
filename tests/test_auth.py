from base64 import b64encode

import pytest
from fastapi import status

BASE_URL = "/api/users"


def test_missing_auth(client, user):
    response = client.post(
        url=f"{BASE_URL}",
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
        url=f"{BASE_URL}",
        json=user,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    data = response.json()
    assert data["detail"] == "incorrect username or password"
