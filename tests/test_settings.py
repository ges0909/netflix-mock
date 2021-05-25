from fastapi import status


def test_read_settings(client, admin_user):
    response = client.get(
        url="/settings",
        headers=dict(Authorization=admin_user),
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "server_port" in data
    assert "server_log_level" in data
    assert "database_url" in data
    assert "database_logging" in data
    assert "mock_username" in data

    assert "mock_password" not in data
    assert "admin_username" not in data
    assert "admin_password" not in data


def test_change_settings(client, admin_user):
    response = client.post(
        url="/settings",
        json=dict(server_port=1305, upload_dir="/tmp"),
        headers=dict(Authorization=admin_user),
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["detail"] == "server_port, upload_dir changed sucessfully"
