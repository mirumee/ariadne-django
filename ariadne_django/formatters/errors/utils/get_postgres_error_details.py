import django.core.exceptions
from django.db import DatabaseError


try:
    import psycopg2
except ImportError as error:
    raise django.core.exceptions.ImproperlyConfigured("Cannot use this function without psycopg2.") from error


def get_postgres_error_details(
    error: DatabaseError,
) -> dict:
    error_code = getattr(getattr(error, "__cause__", None), "pgcode", None)
    default_message = "A database error occurred that prevented this request from being completed."
    if not error_code:
        message = default_message
    elif error_code.startswith("22") or (error_code.startswith("23") and error_code not in ["23505"]):
        # Data exceptions - almost always invalid input that violates db rules.
        # Technically, this should not be on the end user...
        message = "The information you provided is not acceptable."
    elif error_code in ["23505"]:
        message = "The item you are attempting to save already exists."
    else:
        message = default_message

    return {"non_field_errors": [message]}
