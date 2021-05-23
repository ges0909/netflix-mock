import shutil
from typing import List

import fastapi
from fastapi import File, UploadFile, Depends

from netflix_mock.schemas.success import Success
from netflix_mock.settings import get_settings

router = fastapi.APIRouter()


@router.post("/file/")
async def file_(file: bytes = File(...)):
    return {"file_size": len(file)}


@router.post("/uploadfile/")
async def upload_file(
    file: UploadFile = File(...),
    settings=Depends(get_settings),
):
    # contents = await file.read()
    with open(settings.upload_dir / file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return Success(detail=f"file '{file.filename}' uploaded")


# multiple files


@router.post("/files/")
async def files_(file: List[bytes] = File(...)):
    return {"file_size": len(file)}


@router.post("/uploadfiles/")
async def upload_files(
    files: List[UploadFile] = File(...),
    settings=Depends(get_settings),
):
    for file in files:
        with open(settings.upload_dir / file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    file_names = [file.filename for file in files]
    return Success(detail=f"files {', '.join(file_names)} uploaded")
