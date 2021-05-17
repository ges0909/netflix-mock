from fastapi import status


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.text
