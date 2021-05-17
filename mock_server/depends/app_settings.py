from functools import lru_cache

from mock_server.settings import Settings


@lru_cache()
def app_settings() -> Settings:
    from main import app_root

    return Settings(_env_file=app_root / "dev.env")
