import json
from functools import lru_cache
from pathlib import Path
from typing import Optional, Dict

import fastapi
import yaml
from jsf import JSF

from netflix_mock.settings import Settings

router = fastapi.APIRouter()


@lru_cache
def _load_spec(path: Path) -> Optional[Dict]:
    if path or path.exists():
        with open(path) as stream:
            if path.suffix == ".json":
                return json.load(stream)
            if path.suffix in (".yml", ".yaml"):
                return yaml.safe_load(stream)
    return None


@router.put("/")
async def fake_put(status: str):
    settings = Settings()
    if spec := _load_spec(path=settings.er_if):
        schema = spec["paths"]["put"]["responses"][status]["schema"]
        faker = JSF.from_json(str(schema))
        return faker.generate()
    return None
