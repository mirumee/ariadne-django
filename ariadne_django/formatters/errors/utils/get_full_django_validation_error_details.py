import django.core.exceptions


def get_full_django_validation_error_details(
    error: django.core.exceptions.ValidationError,
) -> dict:
    if getattr(error, "message_dict", None) is not None:
        result = error.message_dict
    elif getattr(error, "message", None) is not None:
        result = {"non_field_errors": [error.message]}
    else:
        result = {"non_field_errors": error.messages}
    return result
