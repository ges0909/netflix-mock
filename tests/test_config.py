from fastapi import status


def test_read_settings(test_client, basic_auth):
    response = test_client.get(
        headers=dict(Authorization=basic_auth),
        url="/config",
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "PORT" in data
    assert "DATABASE_URL" in data
    assert "BASIC_AUTH_USERNAME" in data
    assert "BASIC_AUTH_PASSWORD" in data
