from types import SimpleNamespace

from django.conf import settings
from django.test import RequestFactory

from ariadne import MutationType, QueryType, SubscriptionType, make_executable_schema, upload_scalar

import pytest
from graphql import ExecutionContext, ValidationRule


def pytest_configure():
    settings.configure(
        USE_TZ=True,
        TIME_ZONE="America/Chicago",
        INSTALLED_APPS=["ariadne_django"],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
            }
        ],
    )


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def graphql_resolve_info():
    def build_object(request_method, url, user):
        factory = RequestFactory()
        request = getattr(factory, request_method.lower())(url)
        request.user = user

        info = SimpleNamespace()
        info.context = {"request": request}
        return info

    return build_object


@pytest.fixture
def unauthenticated_user():
    user = SimpleNamespace()
    user.is_authenticated = False
    user.is_anonymous = True
    return user


@pytest.fixture
def authenticated_user():
    user = SimpleNamespace()
    user.is_authenticated = True
    user.is_anonymous = False
    return user


@pytest.fixture
def authenticated_user_with_permissions():
    def has_perms(*args, **kwargs):  # pylint: disable=unused-argument
        return True

    user = SimpleNamespace()
    user.is_authenticated = True
    user.is_anonymous = False
    user.has_perms = has_perms
    return user


@pytest.fixture
def authenticated_user_without_permissions():
    def has_perms(*args, **kwargs):  # pylint: disable=unused-argument
        return False

    user = SimpleNamespace()
    user.is_authenticated = True
    user.is_anonymous = False
    user.has_perms = has_perms
    return user


@pytest.fixture
def type_defs():
    return """
        scalar Upload
        type Query {
            hello(name: String): String
            status: Boolean
            testContext: String
            testRoot: String
            testError: Boolean
        }
        type Mutation {
            upload(file: Upload!): String
        }
        type Subscription {
            ping: String!
            resolverError: Boolean
            sourceError: Boolean
            testContext: String
            testRoot: String
        }
    """


def resolve_hello(*_, name):
    return "Hello, %s!" % name


def resolve_status(*_):
    return True


def resolve_test_context(_, info):
    return info.context.get("test")


def resolve_test_root(root, *_):
    return root.get("test")


def resolve_error(*_):
    raise Exception("Test exception")


@pytest.fixture
def resolvers():
    query = QueryType()
    query.set_field("hello", resolve_hello)
    query.set_field("status", resolve_status)
    query.set_field("testContext", resolve_test_context)
    query.set_field("testRoot", resolve_test_root)
    query.set_field("testError", resolve_error)
    return query


def resolve_upload(*_, file):
    if file is not None:
        return type(file).__name__
    return None


@pytest.fixture
def mutations():
    mutation = MutationType()
    mutation.set_field("upload", resolve_upload)
    return mutation


async def ping_generator(*_):
    yield {"ping": "pong"}


async def error_generator(*_):
    raise Exception("Test exception")
    yield 1  # pylint: disable=unreachable


async def test_context_generator(_, info):
    yield {"testContext": info.context.get("test")}


async def test_root_generator(root, *_):
    yield {"testRoot": root.get("test")}


@pytest.fixture
def subscriptions():
    subscription = SubscriptionType()
    subscription.set_source("ping", ping_generator)
    subscription.set_source("resolverError", ping_generator)
    subscription.set_field("resolverError", resolve_error)
    subscription.set_source("sourceError", error_generator)
    subscription.set_source("testContext", test_context_generator)
    subscription.set_source("testRoot", test_root_generator)
    return subscription


@pytest.fixture
def schema(type_defs, resolvers, mutations, subscriptions):
    return make_executable_schema(type_defs, [resolvers, mutations, subscriptions, upload_scalar])


@pytest.fixture
def validation_rule():
    class NoopRule(ValidationRule):
        pass

    return NoopRule


@pytest.fixture
def execution_context_class():
    class CustomExecutionContext(ExecutionContext):
        pass

    return CustomExecutionContext
