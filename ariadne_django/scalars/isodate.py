from datetime import date, datetime
from typing import Any, Union

from django.utils import formats
from django.utils.translation import gettext_lazy as _

from ariadne import ScalarType

from ariadne_django.scalars.utils.parsers import parse_value


date_scalar = ScalarType("Date")
date_input_formats = formats.get_format_lazy("DATE_INPUT_FORMATS")


@date_scalar.serializer
def serialize_date(value: Union[date, datetime]) -> str:
    if isinstance(value, datetime):
        value = value.date()
    return value.isoformat()


@date_scalar.value_parser
def parse_date_value(value: Any) -> date:
    parsed_value = parse_value(value, date_input_formats)
    if not parsed_value:
        raise ValueError(_("Enter a valid date."))
    return parsed_value.date()
