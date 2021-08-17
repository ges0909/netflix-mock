import pytest
from fastapi import status


@pytest.mark.parametrize(
    ["path"],
    [
        ("/a",),
        ("/a/b",),
        ("/a/b/c",),
    ],
)
def test_get(client, api_user, path: str):
    response = client.get(
        headers=dict(Authorization=api_user),
        url=path,
    )
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["detail"] == path
