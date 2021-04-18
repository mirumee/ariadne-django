from unittest.mock import Mock

from django.core.exceptions import PermissionDenied

import pytest

from ariadne_django.auth.decorators.login_required import login_required


def test_unauthenticated_user(unauthenticated_user, graphql_resolve_info):
    info = graphql_resolve_info("GET", "/graphql/", unauthenticated_user)
    wrapped_decorator = login_required()
    decorator = wrapped_decorator(lambda x: x)
    with pytest.raises(PermissionDenied):
        decorator((), info)


def test_authenticated_user(authenticated_user, graphql_resolve_info):
    info = graphql_resolve_info("GET", "/graphql/", authenticated_user)
    func = Mock()
    wrapped_decorator = login_required()
    decorator = wrapped_decorator(func)
    decorator((), info)
    assert func.called
