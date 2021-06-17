import logging
from functools import lru_cache
from pathlib import Path
from pprint import pformat
from typing import Dict, Optional

import fastapi
import jsonref
from fastapi import HTTPException, status
from jsf import JSF

from netflix_mock.settings import get_settings

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


def generate_response(method: str, path: str, status_code: str) -> Dict:
    settings = get_settings()
    if spec := _load_open_api_spec(path=settings.api.spec):
        if path and path in spec["paths"]:
            schema = spec["paths"][path][method]["responses"][status_code]["schema"]
        else:
            schema = spec["paths"][method]["responses"][status_code]["schema"]
        logger.debug("schema=%s", pformat(schema))
        faker = JSF(schema=schema)
        fake_response = faker.generate()
        logger.debug("faked=%s", pformat(fake_response))
        return fake_response
