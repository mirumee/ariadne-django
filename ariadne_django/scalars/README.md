# Scalars

ariadne_django provides custom scalar types that can be used throughout the application.

## Use

You can use scalars in any schema definitions:

```python
from ariadne_django.scalars import date_scalar, datetime_scalar

type_defs = """
    scalar Date
    scalar DateTime

    type Query {
        hello: String
    }
"""
```

Make sure to also include the definition of your scalars in the call to make_executable_schema

```python
schema = make_executable_schema(type_defs, [date_scalar, datetime_scalar, ...])
```

## Date, Datetime, Time Scalars

For convenience ariadne_django also provides:
- Date, DateTime, and Time scalar implementations that can be used to represent Django dates and datetimes in form understood by JS date and time handling libraries like Moment.js.
- Decimal for python's decimal.Decimal implementation (and Django's DecimalField)
- UUID scalar allow for interactions with uuid.UUID objects, which are often used for UUIDFields
- JSON scalar for JSON Fields

## Other types

We welcome contributions of new scalar types!
