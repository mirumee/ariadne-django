from decimal import Decimal, InvalidOperation

from django.utils.formats import number_format, sanitize_separators

from ariadne import ScalarType


decimal_scalar = ScalarType("Decimal")


@decimal_scalar.serializer
def serialize_decimal(value: Decimal) -> str:
    return number_format(value)


@decimal_scalar.value_parser
def parse_decimal_value(value: str) -> Decimal:
    if not isinstance(value, str):
        raise InvalidOperation("Decimal must be a string")
    return Decimal(sanitize_separators(value))
