==================================
Autocompletion via a 3rd party URL
==================================

.. versionadded:: 0.6

This features gives you the opportunity to create an autocompletion field that fetches its data from a 3rd party library (typically a REST or an HTTP API).

Example:

.. code-block:: python

    from agnocomplete.core import AgnocompleteUrlProxy

    class ServiceAutocomplete(AgnocompleteUrlProxy):
        search_url = "https://api.example.com/search"
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

By default, ``django-agnocomplete`` assumes that the returned data looks like this:

.. code-block:: json

    {
        "data": [
            {"value": "value", "label": "label"},
            {"value": "value2", "label": "label2"},
            {"value": "etc, etc", "label": "etc, etc..."}
        ]
    }

Of course, this very simple structure is a bit biased and we're sure it's not even a standard.

As a consequence, you'll probablay have to convert this data into a format known by the agnocomplete widgets. Hopefully, we're providing simple parameters and methods to make an easy conversion.

Configurable parameters
+++++++++++++++++++++++

If your target API follows the dataset structure, you have two params to adjust to your return schema.

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

If you need to merge fields
+++++++++++++++++++++++++++

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

If the result doesn't follow standard schema
++++++++++++++++++++++++++++++++++++++++++++

The simplest case is this one:

.. code-block:: json

    {
        "resultset": [
            {"value": "value", "label": "label"},
            {"value": "value2", "label": "label2"},
            {"value": "etc, etc", "label": "etc, etc..."}
        ]
    }

Your dataset is embedded in a dictionary, but the key to this dataset is not ``data`` but *something else*. You'll only have to give a different value to the class property ``data_key``.


.. code-block:: python

    class AutocompleteUrlConvert(AgnocompleteUrlProxy):
        data_key = 'resultset'

If your result payload is more complicated and you need to loop over it or transform it, you can still overwrite/override the method :meth:`get_http_result`.

.. important::

    this overridden/overwritten method **must** return an iterable (list, set, tuple...)

Simple example:

.. code-block:: python

    class AutocompleteUrlSchema(AgnocompleteUrlProxy):
        def get_http_result(self, payload):
            return payload.get('meta', {}).get('dataset', {})



Passing extra arguments to the API call
---------------------------------------

For various reasons (mostly authentication), you may need to pass extra arguments to the 3rd party API.

The :meth:`get_http_call_kwargs()` method is completely overridable like this:

.. code-block:: python

    class AutocompleteUrlExtraArgs(AgnocompleteProxy):
        search_url = 'http://api.example.com/search'

        def get_http_call_kwargs(self, query, **kwargs):
            query_args = super(
                AutocompleteUrlExtraArgs, self).get_http_call_kwargs(query)
            query_args['auth_token'] = 'GOODAUTHTOKEN'
            return query_args

.. note::

    You may want to change here the default name of the search term field, if the 3rd party API doesn't accept "q" as a search term name.

    .. code-block:: python

        def get_http_call_kwargs(self, query, **kwargs):
            return {
                'search': query,
                'auth_token': 'GOODAUTHTOKEN',
            }

.. note::

    Please note that the ``**kwargs`` argument passed into :meth:`get_http_call_kwargs` will be the same arguments passed to the :meth:`items` method. This way, you can manipulate the argument transmitted by the view to the Agnocomplete class and extract them, manipulate them using your context, etc.


Adding headers to the HTTP call
-------------------------------

You also may want to add custom HTTP headers to your request to the 3rd party API. For authentication reasons, or if you need to specify a Content-type, etc.
In order to do so, you can override the :meth:`get_http_headers()` method in the Agnocomplete class.

By default, this method returns an empty dictionary, so you can completely scratch it, no offense.

.. code-block:: python

    class AutocompleteUrlExtraHeaders(AgnocompleteProxy):
        search_url = 'http://api.example.com/search'

        def get_http_headers(self):
            return {
                'X-API-TOKEN': 'GOODAUTHTOKEN',
                'Content-type': 'application/json',
            }

GET or POST
-----------

The default HTTP verb used is ``GET``, but you may be forced to use ``POST`` if your 3rd party API wants you to. It's just one configuration flag here:

.. code-block:: python

    class AutocompleteUrlPost(AgnocompleteProxy):
        search_url = 'http://api.example.com/search'
        method = 'post'

The payload (with or without extra arguments) will be sent as a JSON dictionary.
