## Types

The table below shows the Django field types with each equivalent default GraphQL field types.

| Field Type | GraphQL Types | Django Field |
| --- | --- | --- |
| ID | ID | AutoField |
| String | String | CharField, TextField, EmailField, FilePathField, SlugField |
| Integer | Int | IntegerField, AutoField, PositiveBigIntegerField, PositiveIntegerField, PositiveSmallIntegerField, SmallIntegerField |
| Float | Float | FloatField |
| Boolean | Boolean | Boolean |

### Built in Scalar types

For the following fields, Ariadne Django has built in Scalars:

| Field Type | Import name | GraphQL Types | Django Field |
| --- | --- | --- | --- |
| Decimals | decimal\_scalar | Decimal | DecimalField |
| Date | date\_scalar | Date | DateField |
| DateTime | datetime\_scalar | DateTime | DateTimeField |
| Time | time\_scalar | Time | TimeField |
| Time | timedelta\_scalar | Timedelta | DurationField |
| JSON Fields | json\_scalar | JSON | JSONField |
| Unique ID | uuid\_scalar | UUID | UUIDField |

When these scalars are used they must be imported from `ariadne_django.scalars` and included in your `make_executable_schema`. In the example below the `date\_scalar` and `datetime\_scalar` are used in the `type_defs` file.

```python
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
```

```python
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
```

## Choice Fields

Choice fields that use strings can be represented using [Enums](https://ariadne.readthedocs.io/en/0.3.0/enums.html)

For Integer Choice fields...

---

## Relationship fields

For fields such as `ForeignKey` and `OneToOneField` can be referenced using the model:  
_Note that the input types require input types in the relationship fields._

```graphql
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
```

For `ManytoManyFields` the brackets are used around the model:

```graphql
type Pet {
    id:  ID
    name: String
   }

type Owner {
    id:  ID
    name: String
    pet: [Pet]
   }
```
