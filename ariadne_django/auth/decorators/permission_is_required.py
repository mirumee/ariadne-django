from django.core.exceptions import PermissionDenied


def permission_required(required_permission):
    def wrapped_decorator(func):
        def wrapped(cls, info, *args, **kwargs):
            perms = (required_permission,) if isinstance(required_permission, str) else required_permission
            user = info.context["request"].user
            if not user.has_perms(perms):
                raise PermissionDenied()
            return func(cls, info, *args, **kwargs)

        return wrapped

    return wrapped_decorator
