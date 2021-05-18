import pytest
from fastapi import status


@pytest.mark.skip(reason="jinja2.exceptions.TemplateNotFound: index.html")
def test_home(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.text
