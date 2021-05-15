# pylint: disable=comparison-with-callable,protected-access
import uuid
from decimal import Decimal, InvalidOperation

from django.utils import timezone

import pytest
from simplejson import JSONDecodeError

from ariadne_django.scalars import (
    date_scalar,
    datetime_scalar,
    decimal_scalar,
    json_scalar,
    parse_date_value,
    parse_datetime_value,
    parse_decimal_value,
    parse_json_value,
    parse_time_value,
    parse_uuid_value,
    serialize_date,
    serialize_datetime,
    serialize_decimal,
    serialize_json,
    serialize_time,
    serialize_uuid,
    time_scalar,
    uuid_scalar,
)
from ariadne_django.scalars.timedelta import serialize_timedelta, parse_timedelta_value, timedelta_scalar


@pytest.fixture
def datetime():
    return timezone.now()


@pytest.fixture
def date(datetime):
    return datetime.date()


@pytest.fixture
def time(datetime):
    return datetime.time()


@pytest.fixture
def timedelta():
    return timezone.timedelta(days=1)


def test_date_serializer_serializes_datetime(datetime, date):
    assert serialize_date(datetime) == date.isoformat()


def test_date_serializer_serializes_date(date):
    assert serialize_date(date) == date.isoformat()


def test_decimal_serializer_serializes_decimal():
    assert serialize_decimal(Decimal("5.0")) == "5.0"


def test_json_serializer_serializes_json():
    assert serialize_json({"cat": "meow"}) == '{"cat": "meow"}'


def test_uuid_serializer_serializes_uuid():
    uuid_str = "e6cbf26a-327f-4fd6-9d28-25738a47e303"
    assert serialize_uuid(uuid.UUID(uuid_str)) == uuid_str


def test_date_parser_returns_valid_date_from_datetime_iso8601_str(datetime, date):
    assert parse_date_value(datetime.isoformat()) == date


def test_date_parser_returns_valid_date_from_date_iso8601_str(date):
    assert parse_date_value(date.isoformat()) == date


def test_date_parser_returns_valid_date_from_other_date_str(date):
    assert parse_date_value(date.strftime("%m/%d/%Y")) == date


def test_date_parser_raises_value_error_on_invalid_data():
    with pytest.raises(ValueError):
        parse_date_value("nothing")


def test_datetime_serializer_serializes_datetime(datetime):
    assert serialize_datetime(datetime) == datetime.isoformat()


def test_datetime_serializer_serializes_date(datetime, date):
    assert serialize_datetime(date) == datetime.date().isoformat()


def test_datetime_parser_returns_valid_date_from_datetime_iso8601_str(datetime):
    assert parse_datetime_value(datetime.isoformat()) == datetime


def test_datetime_parser_returns_valid_date_from_date_iso8601_str(date):
    # time data is lost when datetime scalar receives date
    assert parse_datetime_value(date.isoformat()).date() == date


def test_datetime_parser_returns_valid_date_from_other_date_str(date):
    # time data is lost when datetime scalar receives date
    assert parse_datetime_value(date.strftime("%m/%d/%Y")).date() == date


def test_datetime_parser_raises_value_error_on_invalid_data():
    with pytest.raises(ValueError):
        parse_datetime_value("nothing")


def test_decimal_parser_parses_string():
    assert parse_decimal_value("5.0") == Decimal("5.0")


def test_decimal_parser_raises_invalid_operation_on_invalid_coerceable_type():
    with pytest.raises(InvalidOperation):
        parse_decimal_value(5)


def test_decimal_parser_raises_invalid_operation_on_invalid_data():
    with pytest.raises(InvalidOperation):
        parse_decimal_value("meow")


def test_json_parser_parses_string():
    assert parse_json_value('{"cat": "meow"}') == {"cat": "meow"}


def test_json_parser_raises_invalid_operation_on_invalid_data():
    with pytest.raises(JSONDecodeError):
        parse_json_value("meow")


def test_uuid_parser_parses_uuid_string():
    uuid_str = "bb7efd70-b1cd-11ea-a5af-0242ac130006"
    assert parse_uuid_value(uuid_str) == uuid.UUID(uuid_str)


def test_uuid_parser_raises_value_error_on_invalid_data():
    with pytest.raises(ValueError):
        parse_uuid_value("nothing")


def test_time_serializer_serializes_time(time):
    assert serialize_time(time) == time.isoformat()


def test_timedelta_serializer_serializes_timedelta(timedelta):
    assert timedelta.total_seconds() == serialize_timedelta(timedelta)


def test_time_parser_returns_valid_time_from_datetime_iso8601_str(datetime, time):
    assert parse_time_value(datetime.isoformat()) == time


def test_time_parser_returns_valid_time_from_time_iso8601_str(time):
    assert parse_time_value(time.isoformat()) == time


def test_time_parser_returns_valid_time_from_other_time_str(time):
    assert parse_time_value(time.strftime("%H:%M:%S.%f")) == time


def test_time_parser_raises_value_error_on_invalid_data():
    with pytest.raises(ValueError):
        parse_time_value("nothing")


def test_timedelta_parser_parses_int(timedelta):
    assert parse_timedelta_value(int(timedelta.total_seconds())) == timedelta


def test_timedelta_parser_parses_float(timedelta):
    assert parse_timedelta_value(timedelta.total_seconds()) == timedelta


def test_date_scalar_has_serializer_set():
    assert date_scalar._serialize == serialize_date


def test_date_scalar_has_value_parser_set():
    assert date_scalar._parse_value == parse_date_value


def test_datetime_scalar_has_serializer_set():
    assert datetime_scalar._serialize == serialize_datetime


def test_datetime_scalar_has_value_parser_set():
    assert datetime_scalar._parse_value == parse_datetime_value


def test_time_scalar_has_serializer_set():
    assert time_scalar._serialize == serialize_time


def test_time_scalar_has_value_parser_set():
    assert time_scalar._parse_value == parse_time_value


def test_timedelta_scalar_has_serializer_set():
    assert timedelta_scalar._serialize == serialize_timedelta


def test_timedelta_scalar_has_value_parser_set():
    assert timedelta_scalar._parse_value == parse_timedelta_value


def test_decimal_scalar_has_serializer_set():
    assert decimal_scalar._serialize == serialize_decimal


def test_decimal_scalar_has_value_parser_set():
    assert decimal_scalar._parse_value == parse_decimal_value


def test_json_scalar_has_serializer_set():
    assert json_scalar._serialize == serialize_json


def test_json_scalar_has_value_parser_set():
    assert json_scalar._parse_value == parse_json_value


def test_uuid_scalar_has_serializer_set():
    assert uuid_scalar._serialize == serialize_uuid


def test_uuid_scalar_has_value_parser_set():
    assert uuid_scalar._parse_value == parse_uuid_value
