from functools import lru_cache
from pathlib import Path
from typing import Optional, Dict

import fastapi
import jsonref
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from jsf import JSF

from netflix_mock.settings import Settings

router = fastapi.APIRouter()


@lru_cache
def _load_open_api_spec(path: Path) -> Optional[Dict]:
    if not path:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"open api spec. file path missing",
        )
    if not path.exists():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"open api spec. '{path}' not found",
        )
    if path.suffix != ".json":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"open api spec. '{path}' must be in json format, suffix '{path.suffix}' is not allowed",
        )
    with open(path) as stream:
        return jsonref.load(stream)


@router.put("/")
async def fake_put(path: str = None, status_code: str = "200"):
    settings = Settings()
    if spec := _load_open_api_spec(path=settings.er_if_open_api_spec):
        if path and path in spec["paths"]:
            schema = spec["paths"][path]["put"]["responses"][status_code]["schema"]
        else:
            schema = spec["paths"]["put"]["responses"][status_code]["schema"]
        faker = JSF(schema=schema)
        response = faker.generate(n=1)
        return JSONResponse(content=response, status_code=int(status_code))


@router.delete("/")
async def fake_delete(path: str = None, status_code: str = "204"):
    settings = Settings()
    if spec := _load_open_api_spec(path=settings.er_if_open_api_spec):
        if path and path in spec["paths"]:
            schema = spec["paths"][path]["delete"]["responses"][status_code]["schema"]
        else:
            schema = spec["paths"]["put"]["responses"][status_code]["schema"]
        faker = JSF(schema=schema)
        response = faker.generate(n=1)
        return JSONResponse(content=response, status_code=int(status_code))