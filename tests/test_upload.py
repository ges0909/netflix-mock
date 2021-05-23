from io import StringIO

import pytest
from fastapi import status


def test_file(client):
    file_name = "file.txt"
    file_content = "test content"
    response = client.post(
        url="/file/",
        files={
            "file": (file_name, StringIO(file_content), "text/plain"),
        },
        # headers={"Content-Type": "multipart/form-data"}, # https://github.com/tiangolo/fastapi/issues/1772
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "file_size" in data


def test_upload_file(client, tmp_path):
    file_name = "file.txt"
    file_content = "test content"
    response = client.post(
        url="/uploadfile/",
        files={
            "file": (file_name, StringIO(file_content), "text/plain"),
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "detail" in data
    assert data["detail"] == f"file '{file_name}' uploaded"
    file_uploaded = tmp_path / file_name
    assert file_uploaded.exists()
    with open(file_uploaded, "r") as stream:
        content = stream.read()
    assert content == file_content


@pytest.mark.skip(reason="not implemenetd")
def test_files(client):
    pass


def test_upload_files(client, tmp_path):
    file_names = ["file1.txt", "file2.txt", "file3.txt"]
    response = client.post(
        url="/uploadfiles/",
        files=(
            ("files", ("file1.txt", StringIO("test content"), "text/plain")),
            ("files", ("file2.txt", StringIO("test content"), "text/plain")),
            ("files", ("file3.txt", StringIO("test content"), "text/plain")),
        ),
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "detail" in data
    assert data["detail"] == f"files {', '.join(file_names)} uploaded"
    assert all([(tmp_path / name).exists() for name in file_names])


files = (
    (
        ("files", ("test.txt", StringIO("test content"))),
        ("files", ("test2.txt", StringIO("test content"))),
    ),
)
