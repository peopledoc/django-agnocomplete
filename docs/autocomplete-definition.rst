=======================
Autocomplete definition
=======================

Here we'll see how to define Agnocomplete-compatible autocomplete classes.

Where should they live?
=======================

These classes **must** live in a module names ``autocomplete``, located in one of your Django ``INSTALLED_APPS``. How you're organizing these modules is up to you, but the autodiscover feature **needs** them to be located in this module.

General options
===============

Page size
---------

The page size parameter can have four different sources. It's the maximum number of items returned by the autocomplete when you're being querying it. In order to keep it performant and pertinent, it has limits.

By default, it's defined by the constants that live in the :mod:`agnocomplete.constants` module:

.. literalinclude:: ../agnocomplete/constants.py
   :language: python
   :lines: 5-12

You can override these module defaults using your django settings:

.. code-block:: python

    # AGNOCOMPLETE specifics
    AGNOCOMPLETE_DEFAULT_PAGESIZE = 15
    AGNOCOMPLETE_MAX_PAGESIZE = 120
    AGNOCOMPLETE_MIN_PAGESIZE = 2

If you need to specify a default / min / max page size for your specific Autocomplete class, you still can do it via a class property:

.. code-block:: python

    class AutocompletePerson(AgnocompleteModel):
        page_size = 30
        page_size_max = 120
        page_size_min = 5

Finally, when the HTTP client (usually a JS script, but it can be a curl-like command line tool) is querying, it can add a ``page_size`` argument to tailor the page size to its need:

.. code-block:: sh

    curl http://yourserver/agnocomplete/AutocompletePerson/?q=ali&page_size=3

.. note::

    The minimum and maximum page size can't be overridden by the client, to avoid performances issues.

AgnocompleteField
=================

This basic class provides non-Django-model autocompletion tools. This class is built when your dataset is computed or generated, or a static list of values (like the states of the United States of America, for example).

When you're deriving this class, you *have to* provide a ``choices`` property. This property is usually a list of valid values.

AgnocompleteModel
=================

Choices in this class are related to a Django model. You **must** provide:

* a ``model`` property pointing at a Django model class **OR** a ``get_queryset()`` method, returning the raw records, ready to be filtered by the searched terms.,
* a ``fields`` property listing the fields to be used when searching for a value.


.. code-block:: python

    class AutocompletePerson(AgnocompleteModel):
        model = Person
        fields = ['first_name', 'last_name']

    class AutocompletePersonQueryset(AgnocompleteModel):
        fields = ['first_name', 'last_name']

        def get_queryset(self):
            return Person.objects.filter(email__contains='example.com')


In this class, when you'll be searching for "alice", the returned results will **contain** this word in the ``first_name`` OR the ``last_name`` field.

.. note::

    The field searches will be joined using a ``OR``. In our example, the resulting query will be:

    .. code-block:: sql

        SELECT * from demo_people
        WHERE first_name ILIKE '%value%' OR last_name ILIKE '%value%'


Fields definition
-----------------

You can define fields using a few tricks to refine your search:

* ``^field_name`` will look return values that will **start with** the query argument,
* ``=field_name`` will look for **exact matches** for the query argument,
* ``@field_name`` will use the ``__search`` lookup, taking advantage of the full-text search indexes.

Otherwise, the search will be a simple ``ILIKE '%value%'`` SQL statement.

User-dependant querysets
------------------------

A common usecase: "Please display the items depending on the user context".
In a multi-site context, you *have* to define a preemptive filter to gather informations based on the current context. That's the reason why the ``django-agnocomplete`` views carry the request user into the Autocomplete class. This instance variable is ``self.user``. If you're using a custom authentication profile, it'll be an instance of your ``AUTH_USER_MODE`` class, hence it'll have access to its properties and methods.

.. code-block:: python

    class AutocompletePersonQueryset(AgnocompleteModel):
        fields = ['first_name', 'last_name']
        requires_authentication = True
        model = Person

        def get_queryset(self):
            email = self.user.email
            _, domain = email.split('@')
            return Person.objects.filter(email__endswith=domain)

    class AutocompletePersonSameSite(AgnocompleteModel):
        fields = ['first_name', 'last_name']
        requires_authentication = True
        model = Person

        def get_queryset(self):
            return Person.objects.filter(site=self.user.site)

.. important::

    You may have noticed that these two classes have a ``model`` property and a ``requires_authentication`` property set to ``True``. Because we're using a user-based context, the ``requires_authentication`` will allow the general "out-of-context code" (form class creation) to instanciate the Agnocomplete class without the context, but will disallow it to return results based on the ``query``. This way, you can filter out unauthorized uses of the autocomplete, as you could do it with the ``@login_required`` decorator in
    your views.
