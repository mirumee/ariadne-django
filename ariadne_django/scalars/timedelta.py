from datetime import timedelta
from typing import Union

from ariadne import ScalarType


timedelta_scalar = ScalarType("Timedelta")


@timedelta_scalar.serializer
def serialize_timedelta(value: timedelta) -> float:
    return value.total_seconds()


@timedelta_scalar.value_parser
def parse_timedelta_value(value: Union[int, float]) -> timedelta:
    return timedelta(seconds=value)
