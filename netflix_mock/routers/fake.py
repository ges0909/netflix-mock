import logging
from functools import lru_cache
from pathlib import Path
from pprint import pformat
from typing import Dict, Optional

import fastapi
import jsonref
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from jsf import JSF

from netflix_mock.utils.settings import Settings

logger = logging.getLogger(__name__)

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


@router.put(path="")
async def fake_put(path: str = None, status_code: str = "200"):
    settings = Settings()
    if spec := _load_open_api_spec(path=settings.er_if_open_api_spec):
        if path and path in spec["paths"]:
            schema = spec["paths"][path]["put"]["responses"][status_code]["schema"]
        else:
            schema = spec["paths"]["put"]["responses"][status_code]["schema"]
        logger.debug("schema=%s", pformat(schema))
        faker = JSF(schema=schema)
        response = faker.generate()
        logger.debug("faked=%s", pformat(response))
        return JSONResponse(content=response, status_code=int(status_code))


@router.delete(path="")
async def fake_delete(path: str = None, status_code: str = "204"):
    settings = Settings()
    if spec := _load_open_api_spec(path=settings.er_if_open_api_spec):
        if path and path in spec["paths"]:
            schema = spec["paths"][path]["delete"]["responses"][status_code]["schema"]
        else:
            schema = spec["paths"]["put"]["responses"][status_code]["schema"]
            logger.debug("schema=%s", pformat(schema))
        faker = JSF(schema=schema)
        response = faker.generate()
        logger.debug("faked=%s", pformat(response))
        return JSONResponse(content=response, status_code=int(status_code))
