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
    assert data["server"]["template"]["dir"]
    assert data["server"]["upload"]["dir"]
    assert data["server"]["video"]["dir"]
    assert data["server"]["video"]["chunk_size"]
    assert data["database"]["url"]
    assert data["database"]["logging"]
    assert data["api"]["username"]
    assert data["api"]["password"] == "**********"


def test_update(client, admin_user):
    response = client.post(
        url="/settings",
        json=dict(
            server=dict(
                port=1305,
                upload=dict(dir="..\\upload"),  # has to exists, otherwise validation error
            ),
        ),
        headers=dict(Authorization=admin_user),
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["server"]["port"] == 1305
    assert data["server"]["upload"]["dir"] == "..\\upload"


def test_validation(client, admin_user):
    response = client.post(
        url="/settings",
        json=dict(server=dict(port="NON-NUMERIC-PORT")),
        headers=dict(Authorization=admin_user),
    )
    assert response.status_code == status.HTTP_409_CONFLICT
