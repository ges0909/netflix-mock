from fastapi import status


def test_read_settings(client, basic_auth):
    response = client.get(
        url="/settings/",
        headers=dict(Authorization=basic_auth),
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "SERVER_PORT" in data
    assert "SERVER_LOG_LEVEL" in data
    assert "BASIC_AUTH_USERNAME" in data
    assert "BASIC_AUTH_PASSWORD" in data
    assert "DATABASE_URL" in data
    assert "DATABASE_LOGGING" in data
