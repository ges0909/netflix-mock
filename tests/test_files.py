from io import StringIO

from fastapi import status


def test_files(client):
    response = client.post(
        url="/files/",
        files={
            "file": ("file1.txt", StringIO("test content stream"), "text/plain"),
        },
        # headers={"Content-Type": "multipart/form-data"}, # https://github.com/tiangolo/fastapi/issues/1772
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "file_size" in data


def test_files_upload(client):
    response = client.post(
        url="/files/upload/",
        files={
            "file": ("file1.txt", StringIO("test content stream"), "text/plain"),
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "filename" in data


def test_files_upload_multiple(client):
    response = client.post(
        url="/files/multiple/",
        files={
            "files": ("file1.txt", StringIO("test content stream"), "text/plain"),
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "filenames" in data
    assert data["filenames"] == ["file1.txt", "file2.txt", "file3.txt"]
