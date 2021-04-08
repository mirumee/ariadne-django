[![Ariadne](https://ariadne_djangographql.org/img/logo-horizontal-sm.png)](https://ariadne_djangographql.org)

![Build Status](https://github.com/reset-button/ariadne_django/actions/workflows/tests.yml/badge.svg?branch=master)
[![Codecov](https://codecov.io/gh/reset-button/ariadne_django/branch/master/graph/badge.svg)](https://codecov.io/gh/reset-button/ariadne_django)


# Warning

We strongly recommend against using this in production until this warning is removed.  Converted/refactored code has not yet been fully tested.
This warning will be removed as part of the release process.

# Ariadne

Ariadne is a Python library for implementing [GraphQL](http://graphql.github.io/) servers.

- **Schema-first:** Ariadne enables Python developers to use schema-first approach to the API implementation. This is the leading approach used by the GraphQL community and supported by dozens of frontend and backend developer tools, examples, and learning resources. Ariadne makes all of this immediately available to your and other members of your team.
- **Simple:** Ariadne offers small, consistent and easy to memorize API that lets developers focus on business problems, not the boilerplate.
- **Open:** Ariadne was designed to be modular and open for customization. If you are missing or unhappy with something, extend or easily swap with your own.

Documentation is available [here](https://ariadnegraphql.org).

# ariadne_django

ariadne_django is designed to make integrating Ariadne with Django simpler.
This project splits the existing code from Ariadne's 0.12 release (with enthusiastic permission from Mirumee), decoupling the release of django-specific enhancements for Ariadne from the main ariadne release cycle.
This allows us to be responsive to the needs of both Django and Ariadne.

## Principles

This project is committed to maintaining Ariadne's schema-first approach.  We may offer tooling that simplifies the mapping of Django of models to schema types (or similar), but not require it's usage.
This project will not require Django REST Framework, but will provide features leveraging common DRF tools (e.g. serializers) that provide significant functionality and performance enhancements beyond Django Forms.

## Installation

### Add to project

Install via pip:

`python -m pip install ariadne_django`

### Add to settings

Add ariadne_django to your project's INSTALLED_APPS setting (usually located in settings.py):

```
INSTALLED_APPS = [
    ...
    "ariadne_django",
]
```

Ariadne app provides Django template for GraphQL Playground. Make sure that your Django project is configured to load templates from application directories. This can be done by checking if APP_DIRS option located in TEMPLATES setting is set to True:

```
TEMPLATES = [
    {
        ...,
        'APP_DIRS': True,
        ...
    },
]
```

### Create executable schema

Create a Python module somewhere in your project that will define the executable schema. It may be schema module living right next to your settings and urls:

```
# schema.py
from ariadne import QueryType, make_executable_schema

type_defs = """
    type Query {
        hello: String!
    }
"""

query = QueryType()

@query.field("hello")
def resolve_hello(*_):
    return "Hello world!"

schema = make_executable_schema(type_defs, query)
```

### Add your GraphQL View

Add a GraphQL view to your project's urls.py:

```
from ariadne_django.views import GraphQLView
from django.urls import path

from .schema import schema

urlpatterns = [
    ...
    path('graphql/', GraphQLView.as_view(schema=schema), name='graphql'),
]
```

GraphQLView.as_view() takes mostly the same options that graphql does, but with one difference:
- debug option is not available and it's set to the value of settings.DEBUG
- Django GraphQL view supports extra option specific to it: playground_options, a dict of GraphQL Playground options that should be used.


### Channels

Ariadne's ASGI application can be used together with Django Channels to implement asynchronous GraphQL API with features like subscriptions:

```
from ariadne.asgi import GraphQL
from channels.http import AsgiHandler
from channels.routing import URLRouter
from django.urls import path, re_path


schema = ...


application = URLRouter([
    path("graphql/", GraphQL(schema, debug=True)),
    re_path(r"", AsgiHandler),
])
```

At the moment Django ORM doesn't support asynchronous query execution and there is noticeable performance loss when using it for database access in asynchronous resolvers.

Use asynchronous ORM such as Gino for database queries in your resolvers.

## Upgrading from ariadne.contrib.django

Inside your project, replace all references to ariadne.contrib.django with ariadne_django.

```
find {path_to_your_project} -type f -name \*.py -exec sed -i 's/ariadne\.contrib\.django/ariadne_django/g' {} \;
```

## Local Development

1. Clone the project
1. Setup virtualenv
1. Make changes
1. Run tests, etc. locally
1. Create PR

# Appreciation

With sincere thanks to Mirumee, who crafted the original code of this module and ariadne with <3.
