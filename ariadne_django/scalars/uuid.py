import uuid

from ariadne import ScalarType


uuid_scalar = ScalarType("UUID")


@uuid_scalar.value_parser
def parse_uuid_value(value):
    return uuid.UUID(value)


@uuid_scalar.serializer
def serialize_uuid(value):
    return str(value)
