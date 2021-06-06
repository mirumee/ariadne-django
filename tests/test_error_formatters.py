import django.core.exceptions

from graphql import GraphQLError

from ariadne_django.formatters.errors.simple import format_graphql_error
from ariadne_django.formatters.errors.utils.extract_original_error import extract_original_error
from ariadne_django.formatters.errors.utils.get_full_django_validation_error_details import (
    get_full_django_validation_error_details,
)


def test_extract_original_error_no_original_error():
    graphql_error = GraphQLError(message="Meow")
    extracted_error = extract_original_error(graphql_error)
    assert extracted_error == graphql_error


def test_extract_original_error_single_layer():
    original_error = django.core.exceptions.ValidationError("Woof")
    graphql_error = GraphQLError(message="Meow")
    graphql_error.original_error = original_error
    extracted_error = extract_original_error(graphql_error)
    assert extracted_error == original_error


def test_extract_original_error_many_layers():
    original_error = django.core.exceptions.PermissionDenied("Moo")
    intermediate_layer = GraphQLError(message="Oink")
    graphql_error = GraphQLError(message="Meow")
    intermediate_layer.original_error = original_error
    graphql_error.original_error = intermediate_layer
    extracted_error = extract_original_error(graphql_error)
    assert extracted_error == original_error


def test_get_full_django_validation_error_details_plain_message():
    error = django.core.exceptions.ValidationError("meow")
    error_details = get_full_django_validation_error_details(error)
    assert error_details == {"non_field_errors": ["meow"]}


def test_get_full_django_validation_error_details_list_of_messages():
    error = django.core.exceptions.ValidationError(["meow", "woof"])
    error_details = get_full_django_validation_error_details(error)
    assert error_details == {"non_field_errors": ["meow", "woof"]}


def test_get_full_django_validation_error_details_dictionary():
    error = django.core.exceptions.ValidationError({"cat": "meow", "dog": "woof"})
    error_details = get_full_django_validation_error_details(error)
    assert error_details == {"cat": ["meow"], "dog": ["woof"]}


def test_format_graphql_error_no_original_error():
    graphql_error = GraphQLError(message="Meow")
    formatted_error_messaging = format_graphql_error(graphql_error)
    assert formatted_error_messaging == {
        "message": "Meow",
        "locations": None,
        "path": None,
    }


def test_format_graphql_error_django_validation_error():
    graphql_error = GraphQLError(message="Meow")
    validation_error = django.core.exceptions.ValidationError({"cat": ["meow", "hiss"], "non_field_errors": ["oink"]})
    graphql_error.original_error = validation_error
    formatted_error_messaging = format_graphql_error(graphql_error)
    expected_value = {
        "message": "The information you provided is not acceptable.",
        "locations": None,
        "path": None,
        "code": "INVALID_INPUT",
        "details": {"cat": ["meow", "hiss"], "non_field_errors": ["oink"]},
    }
    assert formatted_error_messaging == expected_value


def test_format_graphql_error_object_does_not_exist_error():
    graphql_error = GraphQLError(message="Meow")
    graphql_error.original_error = django.core.exceptions.ObjectDoesNotExist()
    formatted_error_messaging = format_graphql_error(graphql_error)
    expected_value = {
        "message": "Not found",
        "locations": None,
        "path": None,
        "code": "NOT_FOUND",
        "details": {
            "non_field_errors": ["An error occurred attempting to locate what you requested - no objects were found."]
        },
    }
    assert formatted_error_messaging == expected_value


def test_format_graphql_error_django_permission_denied():
    graphql_error = GraphQLError(message="Meow")
    graphql_error.original_error = django.core.exceptions.PermissionDenied()
    formatted_error_messaging = format_graphql_error(graphql_error)
    expected_value = {
        "message": "Access forbidden",
        "locations": None,
        "path": None,
        "code": "FORBIDDEN",
        "details": {"non_field_errors": ["This request is understood, but is not able to be processed."]},
    }
    assert formatted_error_messaging == expected_value


def test_format_graphql_error_multiple_objects_error():
    graphql_error = GraphQLError(message="Meow")
    graphql_error.original_error = django.core.exceptions.MultipleObjectsReturned()
    formatted_error_messaging = format_graphql_error(graphql_error)
    expected_value = {
        "message": "Many found",
        "locations": None,
        "path": None,
        "code": "MANY_FOUND",
        "details": {
            "non_field_errors": ["An error occurred attempting to locate what you requested - many objects were found."]
        },
    }
    assert formatted_error_messaging == expected_value


def test_format_graphql_error_configuration_error():
    graphql_error = GraphQLError(message="Meow")
    graphql_error.original_error = django.core.exceptions.ImproperlyConfigured()
    formatted_error_messaging = format_graphql_error(graphql_error)
    expected_value = {
        "message": "Internal server error",
        "locations": None,
        "path": None,
        "code": "INTERNAL_SERVER_ERROR",
        "details": {"non_field_errors": ["A server error occurred that prevented this request from being completed."]},
    }
    assert formatted_error_messaging == expected_value


def test_format_graphql_error_custom_map():
    graphql_error = GraphQLError(message="Meow")
    graphql_error.original_error = django.core.exceptions.ImproperlyConfigured()

    custom_map = [
        {
            "classes": (django.core.exceptions.ImproperlyConfigured, django.core.exceptions.SuspiciousOperation),
            "code": "PIE",
            "message": "I like pie",
            "details": {"non_field_errors": (["pie > cake"])},
        }
    ]

    formatted_error_messaging = format_graphql_error(graphql_error, error_map=custom_map)
    expected_value = {
        "message": "I like pie",
        "locations": None,
        "path": None,
        "code": "PIE",
        "details": {"non_field_errors": ["pie > cake"]},
    }
    assert formatted_error_messaging == expected_value


def test_format_graphql_error_custom_map_processes_once():
    graphql_error = GraphQLError(message="Meow")
    graphql_error.original_error = django.core.exceptions.ImproperlyConfigured()

    custom_map = [
        {
            "classes": (django.core.exceptions.ImproperlyConfigured, django.core.exceptions.SuspiciousOperation),
            "code": "PIE",
            "message": "I like pie",
            "details": {"non_field_errors": (["pie > cake"])},
        },
        {
            "classes": (django.core.exceptions.ImproperlyConfigured, django.core.exceptions.SuspiciousOperation),
            "code": "CAKE",
            "message": "I like cake",
            "details": {"non_field_errors": (["cake > pie"])},
        },
    ]

    formatted_error_messaging = format_graphql_error(graphql_error, error_map=custom_map)
    expected_value = {
        "message": "I like pie",
        "locations": None,
        "path": None,
        "code": "PIE",
        "details": {"non_field_errors": ["pie > cake"]},
    }
    assert formatted_error_messaging == expected_value


def test_format_error_with_debug():
    graphql_error = GraphQLError(message="Meow")
    formatted_error_messaging = format_graphql_error(graphql_error, debug=True)
    assert formatted_error_messaging == {
        "message": "Meow",
        "locations": None,
        "path": None,
        "extensions": {"exception": None},
    }
