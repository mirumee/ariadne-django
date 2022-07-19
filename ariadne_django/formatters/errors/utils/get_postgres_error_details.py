import django.core.exceptions
from django.db import DatabaseError


try:
    import psycopg2  # pylint: disable=W0611
except ImportError as error:
    raise django.core.exceptions.ImproperlyConfigured("Cannot use this function without psycopg2.") from error

PG_DATA_VIOLATIONS_PREFIX = "22"
PG_INTEGRITY_VIOLATIONS_PREFIX = "23"
PG_INTEGRITY_UNIQUE_CONSTRAINT_VIOLATION = "23505"


def get_postgres_error_details(
    error: DatabaseError,
) -> dict:
    cause = getattr(error, "__cause__", None)
    error_code = getattr(cause, "pgcode", "")
    default_message = "A database error occurred that prevented this request from being completed."
    if not error_code:
        message = default_message
    elif error_code.startswith(PG_DATA_VIOLATIONS_PREFIX) or (
        error_code.startswith(PG_INTEGRITY_VIOLATIONS_PREFIX)
        and error_code not in [PG_INTEGRITY_UNIQUE_CONSTRAINT_VIOLATION]
    ):
        # Data exceptions - almost always invalid input that violates db rules.
        # Technically, this should not be on the end user...
        message = "The information you provided is not acceptable."
    elif error_code in [PG_INTEGRITY_UNIQUE_CONSTRAINT_VIOLATION]:
        message = "The item you are attempting to save already exists."
    else:
        message = default_message

    return {"non_field_errors": [message]}
