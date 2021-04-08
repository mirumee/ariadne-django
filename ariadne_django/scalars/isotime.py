from datetime import time
from typing import Any

from django.utils import formats
from django.utils.translation import gettext_lazy as _

from ariadne import ScalarType

from ariadne_django.scalars.utils.parsers import parse_value


time_input_formats = formats.get_format_lazy("TIME_INPUT_FORMATS")
time_scalar = ScalarType("Time")


@time_scalar.serializer
def serialize_time(value: time) -> str:
    return value.isoformat()


@time_scalar.value_parser
def parse_time_value(value: Any) -> time:
    parsed_value = parse_value(value, time_input_formats)
    if not parsed_value:
        raise ValueError(_("Enter a valid time."))
    return parsed_value.time()
