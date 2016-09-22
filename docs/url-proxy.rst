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
++++++++++++++++++++

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

For more complicated cases
++++++++++++++++++++++++++

If the returned JSON is in now way similar to what you were expecting, you have several options:

**If the JSON is a list or an iterable**, you can override the `Agnocomplete` class :meth:`item()` method, like this:

.. code-block:: python

    class AutocompleteUrlConvert(AgnocompleteUrlProxy):

        def item(self, current_item):
            return dict(
                value=current_item['pk'],
                label='{} {}'.format(current_item['first_name'], current_item['last_name']),
            )
    

or, if things are going more complicated:

.. code-block:: python

    class AutocompleteUrlConvert(AgnocompleteUrlProxy):

        def item(self, current_item):
            return dict(
                value=current_item[current_item['meta']['value_field']],
                label='{} {}'.format(current_item['label1'], current_item['label2']),
            )
