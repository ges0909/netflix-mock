import pytest
from fastapi import status


@pytest.mark.skip(reason='assert message["type"] == "http.response.start')
def test_home(client):
    response = client.get(path="")
    assert response.status_code == status.HTTP_200_OK
    assert response.text
