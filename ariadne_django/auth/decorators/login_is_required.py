from django.core.exceptions import PermissionDenied


def login_required():
    def wrapped_decorator(func):
        def wrapped(cls, info, *args, **kwargs):
            user = info.context["request"].user
            if not user.is_authenticated:
                raise PermissionDenied()
            return func(cls, info, *args, **kwargs)

        return wrapped

    return wrapped_decorator
