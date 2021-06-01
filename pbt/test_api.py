import schemathesis

from netflix_mock.common.settings import Settings

Settings.Config.env_file = "../dev.env"
Settings.Config.config_file = "../dev.yaml"

from netflix_mock.app import app

schema = schemathesis.from_wsgi(schema_path="/api/openapi.json", app=app)


@schema.parametrize(endpoint="/api")
def test_no_server_errors(case):
    """check that any data fitting the schema doesn't cause a server error"""
    # response = case.call()
    # case.validate_response(response)
    # assert response.status_code < 500
    case.call_and_validate()
