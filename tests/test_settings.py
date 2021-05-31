from fastapi import status


def test_read(client, admin_user):
    response = client.get(
        url="/settings",
        headers=dict(Authorization=admin_user),
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["server"]["port"]
    assert data["server"]["log_level"]
    assert data["server"]["upload_dir"]
    assert data["database"]["url"]
    assert data["database"]["logging"]
    assert data["mock"]["username"]
    assert "password" not in data["mock"]


def test_update(client, admin_user):
    response = client.post(
        url="/settings",
        json=dict(server=dict(port="1305", upload_dir="/tmp")),
        headers=dict(Authorization=admin_user),
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["detail"] == "settings changed"
    response = client.get(
        url="/settings",
        headers=dict(Authorization=admin_user),
    )
    data = response.json()
    assert data["server"]["port"] == 1305
    assert data["server"]["upload_dir"] == "\\tmp"


def test_validation(client, admin_user):
    response = client.post(
        url="/settings",
        json=dict(server=dict(port="NON-NUMERIC-PORT")),
        headers=dict(Authorization=admin_user),
    )
    assert response.status_code == status.HTTP_409_CONFLICT
