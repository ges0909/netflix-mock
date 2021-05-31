import schemathesis

from netflix_mock.common.settings import Settings

Settings.Config.env_file = "../../dev.env"
Settings.Config.config_file = "../../dev.yaml"

from netflix_mock.app import app

schema = schemathesis.from_asgi(schema_path="/api/openapi.json", app=app)


@schema.parametrize()
def test_api(case):
    response = case.call_asgi()
    case.validate_response(response)
