import fastjsonschema
import jsonschema
import pytest

schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://syrocon.de/schemas/pytaf.json",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "datum": {
            "type": "string",
            "format": "date",
        },
    },
}


def test_jsonschema_date_validation():
    """doesn't work although 'jsonschema[format]' is installed"""
    jsonschema.validate(
        schema=schema,
        instance={
            "datum": "abc",
        },
    )


def test_fast_jsonschema_date_validation_failure():
    """works fine"""
    with pytest.raises(fastjsonschema.exceptions.JsonSchemaValueException):  # error: data.datum must be date
        fastjsonschema.validate(
            definition=schema,
            data={
                "datum": "abc",
            },
        )


def test_fast_jsonschema_date_validation_success():
    """works fine"""
    fastjsonschema.validate(
        definition=schema,
        data={
            "datum": "2021-09-09",
        },
    )
