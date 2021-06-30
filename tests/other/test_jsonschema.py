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
        "zeit": {
            "type": "string",
            "format": "time",
        },
        "datumzeit": {
            "type": "string",
            "format": "datetime",
        },
    },
}


# -- jsonschema


def test_jsonschema_date_validation_success():
    jsonschema.validate(
        schema=schema,
        instance={
            "datum": "2021-09-09",
            "zeit": "12:00:00",
            "datumzeit": "12:00:00T12:00:00",
        },
        format_checker=jsonschema.FormatChecker(),
    )


def test_jsonschema_date_validation_failure():
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(
            schema=schema,
            instance={
                "datum": "abc",
            },
            format_checker=jsonschema.FormatChecker(),
        )


# -- fastjsonschema


schema2 = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://syrocon.de/schemas/pytaf.json",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "datum": {
            "type": "string",
            "format": "date",
        }
    },
}


def test_fast_jsonschema_date_validation_success():
    """works fine"""
    fastjsonschema.validate(
        definition=schema2,
        data={
            "datum": "2021-09-09",
        },
    )


def test_fast_jsonschema_date_validation_failure():
    """works fine"""
    with pytest.raises(fastjsonschema.exceptions.JsonSchemaValueException):  # raises 'data.datum must be date'
        fastjsonschema.validate(
            definition=schema2,
            data={
                "datum": "abc",
            },
        )
