Limiting Access to Graphql Endpoint
-----------------------------------

To limit access to login users to the ``/graphql`` endpoint import the
``login_required`` decorator and wrap the path for the url pattern.

.. code:: python

   #url.py
   from django.contrib.auth.decorators import login_required

   urlpatterns = [
       path("graphql/", login_required(GraphQLView.as_view(schema=schema))),
   ]

Limit access to user fields
---------------------------

To limit access to user objects, ``info`` in the resolver function can
be called to get the user context data.

.. code:: python

   #resolvers.py

   query = QueryType()
   @query.field("Books")
       def resolve_books(_, info):
       return Book.objects.filter(user=info.context.user)
