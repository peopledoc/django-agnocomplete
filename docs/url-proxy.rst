==================================
Autocompletion via a 3rd party URL
==================================

.. versionadded:: 0.6

This features gives you the opportunity to create an autocompletion field that fetches its data from a 3rd party library (typically a REST or an HTTP API).

Example:

.. code-block:: python

    from agnocomplete.core import AgnocompleteUrlProxy

    class ServiceAutocomplete(AgnocompleteUrlProxy):
        search_url = "https://api.example.com/search?q={q}"
        item_url = "https://api.example.com/item/{id}"

You may want to have either a :meth:`get_search_url()` method in your class, or overriding the ``search_url`` property.

Also, the ``item_url`` can be overridden by a :meth:`get_item_url()` method.

These must be an accessible full-URL (including scheme, domain, and port if necessary) with at least one search term variable to inject in the URL for searching it.

If you're lucky enough, this target URL respects:

* the agnocomplete return data schema,
* the agnocomplete query argument list (q, page_size, etc).

then, you won't have to do anything else: this service will return data directly usable with your favorite HTML/JS tool.

What if it doesn't return the standard agnocomplete JSON?
---------------------------------------------------------

You'll have to convert this data into a format known by the agnocomplete widgets. Hopefully, we're providing simple parameters to make an easy conversion.

What's configurable?

* ``value_key``: the name of the key in the item dictionary to be used for ``value``,
* ``label_key``: the name of the key in the item dictionary to be used for ``label``,

Example:

.. code-block:: python

    class AutocompleteUrlConvert(AgnocompleteUrlProxy):
        value_key = 'pk'
        label_key = 'full_name'

With this class, the item:

.. code-block:: json

    {"pk": 19911, "full_name": "Inigo Montoya", "country": "Spain"}

will be converted like this before being returned by the search:

.. code-block:: json

    {"value": 19911, "label": "Inigo Montoya"}
