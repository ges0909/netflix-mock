from box import Box
from fastapi import status


def test_read_settings(client, admin_user):
    response = client.get(
        url="/settings",
        headers=dict(Authorization=admin_user),
    )
    assert response.status_code == status.HTTP_200_OK
    data = Box(response.json())
    assert data.server.port
    assert data.server.log_level
    assert data.server.upload_dir
    assert data.database.url
    assert data.database.logging
    assert data.mock.username
    assert not data.mock.password


def test_change_settings(client, admin_user):
    response = client.post(
        url="/settings",
        json=dict(server=dict(port=1305, upload_dir="/tmp")),
        headers=dict(Authorization=admin_user),
    )
    assert response.status_code == status.HTTP_200_OK
    data = Box(response.json())
    assert data.content.detail == "server_port, upload_dir changed sucessfully"
