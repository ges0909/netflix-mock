import shutil
from typing import List

import fastapi
from fastapi import File, UploadFile

from netflix_mock.schemas.success import Success
from netflix_mock.settings import get_settings

router = fastapi.APIRouter()

# single file


@router.post(path="/file")
async def file_(file: bytes = File(...)):
    return {"file_size": len(file)}


@router.post(path="/uploadfile")
async def upload_file(
    file: UploadFile = File(...),
):
    # contents = await file.read()
    settings = get_settings()
    with open(settings.server.upload.dir / file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return Success(detail=f"file '{file.filename}' uploaded")


# multiple files


@router.post(path="/files")
async def files_(files: List[bytes] = File(...)):
    return [len(file) for file in files]


@router.post(path="/uploadfiles")
async def upload_files(
    files: List[UploadFile] = File(...),
):
    settings = get_settings()
    for file in files:
        with open(settings.server.upload.dir / file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    file_names = [file.filename for file in files]
    return Success(detail=f"files {', '.join(file_names)} uploaded")
