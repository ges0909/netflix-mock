from fastapi import status


def test_fake(client):
    response = client.put("/fake/?status=201")
    assert response.status_code == status.HTTP_200_OK
