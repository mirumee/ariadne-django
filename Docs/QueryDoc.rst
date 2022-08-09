Query
-----

Queries require specifying the GraphQL schema and a Query type. For
example Lets have a model ``Document`` with a name field:

.. code:: python

   # models.py
   from django.db import models

   class Document(models.Model):
       name = models.CharField(max_length=50, null=False, blank=False)

       def __str__(self):
           return self.name

For the Query, we define a GraphQL schema and a Query type in
``type_defs`` where they Query contains the name of the Query
``getDocument`` with the input fields (id and name) followed by the
format of the return object ``[Document]``, which returns a list of
Documents. The return object can also be customized by adding an
additional schema type for tasks such as handling returning error
issues.

.. code:: python

   from ariadne import gql, QueryType
   from ariadne import make_executable_schema
   from core.schema import type_defs, query
   from django.db.models import Q


   type_defs = gql("""
      type Document {
           id:ID
           name: String!
      }

       type Query {
           getDocument(name:String, id:ID): [Document]
       }

   """)

   query = QueryType()

   @query.field("getDocument")
   def resolve_getDocument(*_, name=None, id=None,):
       if name:
           filter = Q(name__icontains=name)
           return Document.objects.filter(filter)
       if id:
           filter = Q(id__exact=id)
           return Document.objects.filter(filter)
       return Document.objects.all()

   schema = make_executable_schema(type_defs, query)

| The resolver is a function beginning with ``resolve_`` followed by the
  name of the query and the input fields.
| In this example, a filter is applied when name or id is present where
  the results will return the Document with the exact id entered or a
  list of ``Documents`` containing the entry in ``name``. If no values
  are entered, the query will get all objects. The filters are based on
  the Django Field lookups.

To modify the ordering of the results, the Query type and the queries in
the resolver can be modified where you can enter ``"name"`` for
ascending order by name and ``"-name"`` for descending.

.. code:: python

   type_defs = gql("""
      type Document {
           id:ID
           name: String!
      }

       type Query {
           getDocument(name:String, id:ID, order:String): [Document]
       }

   """)

   query = QueryType()

   @query.field("getDocument")
   def resolve_getDocument(*_, name=None, id=None, order=None):
       if name:
           filter = Q(name__icontains=name)
           return Document.objects.filter(filter).order_by(order)
       if id:
           filter = Q(id__exact=id)
           return Document.objects.filter(filter).order_by(order)
       return Document.objects.all().order_by(order)
