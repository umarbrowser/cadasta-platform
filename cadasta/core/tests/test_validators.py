import pytest
from django.test import TestCase
from django.utils.translation import gettext as _
from ..validators import validate_json, JsonValidationError, sanitize_string


class ValidationTest(TestCase):
    def test_validate_valid(self):
        schema = {
            "$schema": "http://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
            "required": ["name"]
        }

        assert validate_json({'name': 'val'}, schema) is None

    def test_validate_anyof(self):
        schema = {
            "$schema": "http://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
            },
            "anyOf": [
                {"required": ["name"]},
                {"required": ["description"]},
            ]
        }

        with pytest.raises(JsonValidationError) as exc:
            assert validate_json({}, schema) is None

        assert exc.value.errors['name'] == (
            _("Please provide either name or description"))
        assert exc.value.errors['description'] == (
            _("Please provide either name or description"))

    def test_validate_invalid_required(self):
        schema = {
            "$schema": "http://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
            "required": ["name"]
        }

        with pytest.raises(JsonValidationError) as exc:
            validate_json({'some': 'val'}, schema)

        assert exc.value.errors['name'] == _("This field is required.")

    def test_validate_invalid_format(self):
        schema = {
            "$schema": "http://json-schema.org/schema#",
            "type": "object",
            "properties": {
                "email": {"type": "string", "format": "email"},
            },
        }

        with pytest.raises(JsonValidationError) as exc:
            validate_json({'email': 'blah'}, schema)

        assert (exc.value.errors['email'] ==
                _("'{value}' is not a '{type}'").format(value='blah',
                                                        type='email'))

    def test_is_sane(self):
        assert sanitize_string('text') is True
        assert sanitize_string('大家好') is True
        assert sanitize_string('ф') is True
        assert sanitize_string('Ξ') is True
        assert sanitize_string('ß') is True
        assert sanitize_string('œ') is True
        assert sanitize_string(':)') is True
        assert sanitize_string('İ') is True
        assert sanitize_string('עזרא ברש') is True
        assert sanitize_string('<text>') is False
        assert sanitize_string('<text>blah</text>') is False
        assert sanitize_string('\\text') is False
        assert sanitize_string('te\\xt') is False
        assert sanitize_string('text/') is False
        assert sanitize_string('text/other') is False
        assert sanitize_string('text;') is False
        assert sanitize_string('te; xt') is False
        assert sanitize_string('te;xt') is False
        assert sanitize_string('🍺') is False
        assert sanitize_string('te🍺xt') is False
