from datetime import datetime
from typing import Any

from django.forms.utils import from_current_timezone
from django.utils import formats
from django.utils.translation import gettext_lazy as _

from ariadne import ScalarType

from ariadne_django.scalars.utils.parsers import parse_value


datetime_input_formats = formats.get_format_lazy("DATETIME_INPUT_FORMATS")
datetime_scalar = ScalarType("DateTime")


@datetime_scalar.serializer
def serialize_datetime(value: datetime) -> str:
    return value.isoformat()


@datetime_scalar.value_parser
def parse_datetime_value(value: Any) -> datetime:
    parsed_value = parse_value(value, datetime_input_formats)
    if not parsed_value:
        raise ValueError(_("Enter a valid date/time."))
    return from_current_timezone(parsed_value)
