from copy import deepcopy

import django.core.exceptions

from ariadne import get_error_extension

from ariadne_django.formatters.errors.utils.extract_original_error import extract_original_error
from ariadne_django.formatters.errors.utils.get_full_django_validation_error_details import (
    get_full_django_validation_error_details,
)


ERROR_MAP = [
    {
        "classes": (django.core.exceptions.PermissionDenied,),
        "code": "FORBIDDEN",
        "message": "Access forbidden",
        "details": {"non_field_errors": (["This request is understood, but is not able to be processed."])},
    },
    {
        "classes": (django.core.exceptions.ObjectDoesNotExist,),
        "code": "NOT_FOUND",
        "message": "Not found",
        "details": {
            "non_field_errors": (["An error occurred attempting to locate what you requested - no objects were found."])
        },
    },
    {
        "classes": (django.core.exceptions.ValidationError,),
        "code": "INVALID_INPUT",
        "message": "The information you provided is not acceptable.",
        "details": get_full_django_validation_error_details,
    },
    {
        "classes": (django.core.exceptions.MultipleObjectsReturned,),
        "code": "MANY_FOUND",
        "message": "Many found",
        "details": {
            "non_field_errors": (
                ["An error occurred attempting to locate what you requested - many objects were found."]
            )
        },
    },
    {
        "classes": (django.core.exceptions.ImproperlyConfigured, django.core.exceptions.SuspiciousOperation),
        "code": "INTERNAL_SERVER_ERROR",
        "message": "Internal server error",
        "details": {
            "non_field_errors": (["A server error occurred that prevented this request from being completed."])
        },
    },
]


def format_graphql_error(error, error_map=None, debug=False):
    """
    The GraphQL spec is silent on the subject of communicating server error messages to the client.
    A number of bad practices exist and there is no consensus on an appropriate best practice.
    As such, we offer yet another potential solution - one that can be either used out of the box
    or as a reference implementation.  Generally speaking, we want to carry as much of the original
    Django error messaging around as possible.

    Thanks and inspiration for the original implementation of this by Lexria were found in Ariadne documentation
    and based in https://koistya.medium.com/validation-and-user-errors-in-graphql-mutations-39ca79cd00bf
    Cпасибо Константин!
    """

    if error_map is None:
        error_map = ERROR_MAP

    formatted = deepcopy(error.formatted)
    original_error = extract_original_error(error)
    for row_dict in error_map:
        if isinstance(original_error, row_dict.get("classes", tuple())):
            formatted["message"] = row_dict.get("message", "Unknown error")
            formatted["code"] = row_dict.get("code", "UNKNOWN_ERROR")
            formatted["details"] = row_dict.get(
                "details",
                {"non_field_errors": "An unexpected error occurred that prevented this request from being completed."},
            )

            if callable(formatted["details"]):
                formatted["details"] = formatted["details"](original_error)

            break

    if debug:
        if "extensions" not in formatted:
            formatted["extensions"] = {}
            formatted["extensions"]["exception"] = get_error_extension(error)

    return formatted
