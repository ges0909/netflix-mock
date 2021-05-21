from fastapi import status


def test_read_settings(client, basic_auth):
    response = client.get(
        headers=dict(Authorization=basic_auth),
        url="/settings/",
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "SERVER_PORT" in data
    assert "DATABASE_URL" in data
    assert "BASIC_AUTH_USERNAME" in data
    assert "BASIC_AUTH_PASSWORD" in data
