import schemathesis

schema = schemathesis.from_path(path="openapi.json")


@schema.parametrize(endpoint="/api")
def test_no_server_errors(case):
    """check that any data fitting the schema doesn't cause a server error"""
    # response = case.call()
    # case.validate_response(response)
    # assert response.status_code < 500
    case.call_and_validate()
