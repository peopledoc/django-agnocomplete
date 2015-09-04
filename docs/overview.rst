========
Overview
========

Usage
=====

Setup
-----

Add ``agnocomplete`` to your ``INSTALLED_APPS``.

Include the agnocomplete URLs to your urlconf:

.. code-block:: python

    from django.conf.urls import include, url

    urlpatterns = [
        # Starting here
        url(
            r'^autocomplete/',
            include('agnocomplete.urls', namespace='autocomplete')),
        # ... Continuing here...
    ]

Build your Autocomplete classes
-------------------------------

You'll need to add an ``autocomplete.py`` in your target app. It'll be automatically picked up by the ``agnocomplete`` application at startup.

These classes should be able to dig data out of your data store. In a Django application, it'll probably be models, but it can also be a long list of strings (let's say: the list of the US States, or the full list of the world countries).

There are two types of classes at the moment: :class:`AutocompleteChoices` and :class:`AutocompleteModel`.

Let's take the demo example to make it clearer:

.. code-block:: python

    from agnocomplete.register import register
    from agnocomplete.core import AutocompleteChoices, AutocompleteModel
    from demo.models import Person


    class AutocompleteColor(AutocompleteChoices):
        choices = ['green', 'gray', 'blue', 'grey']


    class AutocompletePerson(AutocompleteModel):
        model = Person
        fields = ['first_name', 'last_name']

    # Registration
    register(AutocompleteColor)
    register(AutocompletePerson)

The :class:`AutocompleteColor` is a simple choice source: a list of strings. For the sake of the demo, it's not very long.

The :class:`AutocompletePerson` will grab its data from the django model Person, and expose the fields `first_name` and `last_name` as source fields for the search.

It means that when the client code will try to search for a term, it'll be searched in both ``first_name`` and ``last_name`` fields. These should be fields defined in your model.

And that's it! The ``agnocomplete`` app will automatically add these two URLs to your URLs::

    /autocomplete/AutocompleteColor/
    /autocomplete/AutocompletePerson/

Want to search for the results? Use `curl` or any other tool to get data.

If the query is empty, it will return no result, for it's not able to know what to search:

.. code-block:: sh

    curl http://yourserver/autocomplete/AutocompleteColor/
    {"data": []}

.. code-block:: sh

    curl http://yourserver/autocomplete/AutocompletePerson/
    {"data": []}

With an interesting search term:

.. code-block:: sh

    curl http://yourserver/autocomplete/AutocompleteColor/?q=gre
    {"data": [
        {"label": "green", "value": "green"},
        {"label": "grey", "value": "grey"}
    ]}

    curl http://yourserver/autocomplete/AutocompletePerson/?q=ali
    {
        "data": [
            {
                "label": "Alice Iñtërnâtiônàlizætiøn",
                "value": "1"
            },
            {
                "label": "Alice Inchains",
                "value": "2"
            },
            {
                "label": "Alice Obvious",
                "value": "4"
            },
            {
                "label": "Alice Galactic",
                "value": "5"
            }
        ]
    }
