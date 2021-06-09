#########################
Installing ariadne_django
#########################

You must have :code:`python` and :code:`pip` installed on your system, and in your :code:`PATH`.
An activated virtual environment is also recommended.

Getting ariadne_django
======================

Using :code:`pip`:
------------------

.. code-block:: bash

    pip install ariadne_django

Using :code:`poetry`:
---------------------

`Poetry <https://python-poetry.org/>`_ is a tool for dependency management and packaging in Python. It allows
you to declare the libraries your project depends on and it will manage
(install/update) them for you.


.. code-block:: bash

    poetry add ariadne_django

Add to settings
===============

Add :code:`ariadne_django` to your project's :code:`INSTALLED_APPS` setting (usually
located in :code:`<project_name>/settings.py`):

.. code-block:: python

    INSTALLED_APPS = [
        # other stuff
        "ariadne_django",
    ]


The Ariadne app provides a Django template for GraphQL Playground. Make sure that your
django project is configured to load templates from application directories. This can be
done by checking if :code:`APP_DIRS` option located in :code:`TEMPLATES` setting is set to
:code:`True`:

.. code-block:: python

    TEMPLATES = [
        {
            # ...,
            'APP_DIRS': True,
            # ...
        },
    ]
