import re
from django.utils.translation import ugettext as _

from jsonschema import Draft4Validator, FormatChecker
from .exceptions import JsonValidationError


def validate_json(value, schema):
    v = Draft4Validator(schema, format_checker=FormatChecker())
    errors = sorted(v.iter_errors(value), key=lambda e: e.path)

    message_dict = {}
    for e in errors:
        if e.validator == 'anyOf':
            fields = [
                f.message.split(' ')[0].replace('\'', '') for f in e.context
            ]

            for f in fields:
                message_dict[f] = _("Please provide either {}").format(
                    _(" or ").join(fields))

        elif e.validator == 'required':
            field = e.message.split(' ')[0].replace('\'', '')
            message_dict[field] = _("This field is required.")
        else:
            field = '.'.join([str(el) for el in e.path])
            message_dict[field] = e.message

    if message_dict:
        raise JsonValidationError(message_dict)


pattern = re.compile(u'.*[<>;\\\/'
                     u'\U0001F300-\U0001F64F\U0001F680-\U0001F6FF'
                     u'\u2600-\u26FF\u2700-\u27BF].*')


def sanitize_string(value):
    if not value:
        return True

    return not pattern.match(value)
