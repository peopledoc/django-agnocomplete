==============
Error Handling
==============

We're handling errors on many levels. What the front-end integrators need to know is that, if an error occurs at some point (Database, HTTP request, etc), the corresponding payload is sent back to the user:

.. code-block:: json

    {
        "errors": [
            {
                "title": "Database Error",
                "detail": "An error has occurred. Please contact your administrator"
            }
        ]
    }

This error payload format is inspired by `JSON API <http://jsonapi.org/format/#errors>`_


.. important::

    Along with this payload, the response status code may be a 4xx or a 5xx depending on the error raised.
