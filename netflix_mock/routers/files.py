from typing import List

import fastapi
from fastapi import File, UploadFile

router = fastapi.APIRouter()


@router.post("/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@router.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename}


@router.post("/upload/multiple")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {
        "filenames": [file.filename for file in files],
    }
