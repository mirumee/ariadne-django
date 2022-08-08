Types
-----

The table below shows the Django field types with each equivalent
default GraphQL field types.

+-----------------------+-----------------------+------------------------+
| Field Type            | GraphQL Types         | Django Field           |
+=======================+=======================+========================+
| ID                    | ID                    | AutoField              |
+-----------------------+-----------------------+------------------------+
| String                | String                | CharField, TextField,  |
|                       |                       | EmailField,            |
|                       |                       | FilePathField,         |
|                       |                       | SlugField              |
+-----------------------+-----------------------+------------------------+
| Integer               | Int                   | IntegerField,          |
|                       |                       | AutoField,             |
|                       |                       | PositiveBigIntegerField|
|                       |                       | PositiveIntegerField,  |
|                       |                       | Posit                  |
|                       |                       | iveSmallIntegerField,  |
|                       |                       | SmallIntegerField      |
+-----------------------+-----------------------+------------------------+
| Float                 | Float                 | FloatField             |
+-----------------------+-----------------------+------------------------+
| Boolean               | Boolean               | Boolean                |
+-----------------------+-----------------------+------------------------+

Built in Scalar types
~~~~~~~~~~~~~~~~~~~~~

For the following fields, Ariadne Django has built in Scalars:

=========== ================ ============= =============
Field Type  Import name      GraphQL Types Django Field
=========== ================ ============= =============
Decimals    decimal_scalar   Decimal       DecimalField
Date        date_scalar      Date          DateField
DateTime    datetime_scalar  DateTime      DateTimeField
Time        time_scalar      Time          TimeField
Time        timedelta_scalar Timedelta     DurationField
JSON Fields json_scalar      JSON          JSONField
Unique ID   uuid_scalar      UUID          UUIDField
=========== ================ ============= =============

When these scalars are used they must be imported from
``ariadne_django.scalars`` and included in your
``make_executable_schema``. In the example below the ``date_scalar``
and ``datetime_scalar`` are used in the ``type_defs`` file.

.. code:: python

   #types.py
   type_defs = gql("""

   type Person {
       id:  ID
       name: String!
       birth: Date
      }

   type Document {
       id:  ID
       name: String!
       createdtime: DateTime
      }

   type Query {
      People(id:ID, name:String):[Person]
      Documents(id:ID, name:String): [Document]

     }
   """)

.. code:: python

   #schema.py
   from ariadne import make_executable_schema
   from .schema import query, mutation
   from .types import type_defs
   from ariadne_django.scalar import date_scalar, datetime_scalar


   schema = make_executable_schema(
       type_defs,
       query,
       mutation,
       # Built in Scalars
       date_scalar,
       datetime_scalar,
   )


--------------

Choice Fields
-------------

Choice fields that use strings can be represented using
`Enums <https://ariadne.readthedocs.io/en/0.3.0/enums.html>`__ that are declared in the ``type_defs``. These are represented as Strings in graphQL types

.. code:: python

    enum Issue {
        Open
        Pending
        Completed
      }



For IntegerChoice fields where they are represented in Django as:

.. code:: python

    #models.py
    class Issue(models.IntegerChoices):
        Open = 1
        Pending = 2
        Completed = 3

    class Forum(models.Model):
        user =  models.CharField(max_length=100, null=True, blank=True)
        issue = models.IntegerField(choices=Issue.choices,
                                       blank=True, null=True)


The enum should be declared in the ``type_defs``, mapped to a class, and added into the ``make_executable_schema``:

.. code:: python

    import enum
    from ariadne import EnumType

    type_defs = gql("""
    enum Issue {
        Open
        Pending
        Completed
      }

    type Forum {
        id:  ID
        name: String
        issue: Issue
       }

    """)



    class Issue(enum.IntEnum):
        Open = 1
        Pending= 2
        Completed = 3

    issue_enum = EnumType("Issue", Issue)

    schema = make_executable_schema(type_defs, query, mutation, issue_enum)


--------------

Relationship fields
-------------------

| For fields such as ``ForeignKey`` and ``OneToOneField`` can be
  referenced using the model:
| *Note that the input types require input types in the relationship
  fields.*

.. code:: python
   type Author {
       id:  ID
       name: String!
      }

   type Blog {
       id:  ID
       name: String
       author: Author
      }

   input AuthorInput {
       id:  ID
       name: String!
      }

   input BlogInput {
       id:  ID
       name: String
       author: AuthorInput
      }

For ``ManytoManyFields`` the brackets are used around the model:

.. code:: python

   type Pet {
       id:  ID
       name: String
      }

   type Owner {
       id:  ID
       name: String
       pet: [Pet]
      }
