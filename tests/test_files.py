from io import StringIO

from requests_toolbelt import MultipartEncoder
from fastapi import status

m = MultipartEncoder(
    fields={
        # "field": ("filename", open("test_files.py", "rb"), "text/plain"),
        "field": ("filename", StringIO("test content stream"), "text/plain"),
    }
)


def test_files(client):
    response = client.post(
        url="/files",
        data=m,
        headers={"Content-Type": "multipart/form-data"},
    )
    assert response.status_code == status.HTTP_200_OK


def test_files_upload():
    pass


def test_files_upload_multiple():
    pass
