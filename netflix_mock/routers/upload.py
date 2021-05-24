import shutil
from typing import List

import fastapi
from fastapi import File, UploadFile

from netflix_mock.config import Config
from netflix_mock.schemas.success import Success

router = fastapi.APIRouter()

# single file


@router.post("/file/")
async def file_(file: bytes = File(...)):
    return {"file_size": len(file)}


@router.post("/uploadfile/")
async def upload_file(
    file: UploadFile = File(...),
):
    # contents = await file.read()
    config = Config()
    with open(config.upload_dir / file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return Success(detail=f"file '{file.filename}' uploaded")


# multiple files


@router.post("/files/")
async def files_(files: List[bytes] = File(...)):
    return [len(file) for file in files]


@router.post("/uploadfiles/")
async def upload_files(
    files: List[UploadFile] = File(...),
):
    config = Config()
    for file in files:
        with open(config.upload_dir / file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    file_names = [file.filename for file in files]
    return Success(detail=f"files {', '.join(file_names)} uploaded")
