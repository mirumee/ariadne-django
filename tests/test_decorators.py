from unittest.mock import Mock

from django.core.exceptions import PermissionDenied

import pytest

from ariadne_django.auth.decorators import login_required, permission_required


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


def test_user_with_permissions_list(authenticated_user_with_permissions, graphql_resolve_info):
    info = graphql_resolve_info("GET", "/graphql/", authenticated_user_with_permissions)
    func = Mock()
    wrapped_decorator = permission_required(["meow"])
    decorator = wrapped_decorator(func)
    decorator((), info)
    assert func.called


def test_user_with_permissions_string(authenticated_user_with_permissions, graphql_resolve_info):
    info = graphql_resolve_info("GET", "/graphql/", authenticated_user_with_permissions)
    func = Mock()
    wrapped_decorator = permission_required("meow")
    decorator = wrapped_decorator(func)
    decorator((), info)
    assert func.called


def test_user_without_permissions(authenticated_user_without_permissions, graphql_resolve_info):
    info = graphql_resolve_info("GET", "/graphql/", authenticated_user_without_permissions)
    wrapped_decorator = permission_required(["meow"])
    decorator = wrapped_decorator(lambda x: x)
    with pytest.raises(PermissionDenied):
        decorator((), info)
