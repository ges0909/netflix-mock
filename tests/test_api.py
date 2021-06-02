from pathlib import Path

import schemathesis

from netflix_mock.common.settings import Settings

Settings.Config.env_file = Path(__file__).parent / ".." / "dev.env"
Settings.Config.config_file = Path(__file__).parent / ".." / "dev.yaml"

from netflix_mock.app import app

schema = schemathesis.from_asgi(schema_path="/api/openapi.json", app=app)


@schema.parametrize(endpoint="/api/users")
def test_users(case):
    response = case.call_asgi()
    case.validate_response(response)


@schema.parametrize(endpoint="/settings")
def test_settings(case):
    response = case.call_asgi()
    case.validate_response(response)
