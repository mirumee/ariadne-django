import json
from typing import Any

from ariadne import ScalarType


json_scalar = ScalarType("JSON")


@json_scalar.serializer
def serialize_json(value: Any) -> str:
    return json.dumps(value)


@json_scalar.value_parser
def parse_json_value(value: str) -> Any:
    return json.loads(value)
