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

Minimum length of query size
----------------------------

It's obvious that searching for a one-character-term is not a good idea, both on the backend side (too many pointless calls) or on the frontend (too many unusable results). To limit this, we advise the front-end integration not to call the agnocomplete URL if the search term typed in the search box doesn't meet the minimum length.

This is handled by the ``query_size`` parameter. As for the page size, this parameter can be overridden, but only in the backend.

There are two important settings:

* ``AGNOCOMPLETE_DEFAULT_QUERYSIZE``: the usual default minimum length of the search term to be queried.
* ``AGNOCOMPLETE_MIN_QUERYSIZE``: the absolute minimum length of a search term.

These variables are set in the ``agnocomplete.constants`` module.

They can be overridden in the django settings, like this:

.. code-block:: python

    AGNOCOMPLETE_DEFAULT_QUERYSIZE = 5
    AGNOCOMPLETE_MIN_QUERYSIZE = 3

Also, this can be overridden in the autocomplete class definition, like this:

.. code-block:: python

    class AutocompletePerson(AgnocompleteModel):
        query_size = 6
        query_size_min = 5

.. note::

    They don't have to be different, you can also force them to be equal:

    .. code-block:: python

        AGNOCOMPLETE_DEFAULT_QUERYSIZE = AGNOCOMPLETE_MIN_QUERYSIZE = 3


1. In the input, we're providing a ``data-query-size`` attribute you can fetch to adjust your frontend.
2. If the AJAX view is called with a search term that is smaller than the Agnocomplete class minimum length, the resultset will be empty.


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

This section is now handled in the following dedicated document.

see: :doc:`context-dependant-completions`

Customize the label
-------------------

Sometimes, it can be useful to customize the display label. The class provides
a method that can be overridden.

For example:

.. code-block:: python

    class AutocompletePerson(AgnocompleteModel):
        model = Person
        fields = ['first_name', 'last_name']
        query_size_min = 2

        def item(self, current_item):
            label = {
                'value': force_text(current_item.pk),
                'label': u'{item} {mail}'.format(
                    item=force_text(current_item), mail=current_item.email)
            }

            return label


Extract extra-information
-------------------------

You may want to add extra fields to your returned records, fields that belong to another table (e.g. the count of friends each one has). For performance reasons, it's not safe to extract this out of the raw :meth:`get_queryset()` method. Use the :attr:`final_queryset` property instead, or, better, using the result of the :meth:`items()` serialization.


.. code-block:: python

    from django.utils.functional import cached_property

    class AutocompletePerson(AgnocompleteModel):
        model = Person
        fields = ['first_name', 'last_name']

        @cached_property
        def friends(self):
            queryset = self.final_queryset
            # This returns a dict of friends count, the keys being the PKs
            return count_friends([item.pk for item in queryset])

        def item(self, current_item):
            friends = self.friends
            label = {
                'value': force_text(current_item.pk),
                'label': u'{item} {mail} ({friends})'.format(
                    item=force_text(current_item),
                    mail=current_item.email,
                    friends=friends.get(current_item.pk, 0)
                )
            }

            return label


.. important::

    The :attr:`final_queryset` property is **paginated**, which means that you won't be able to re-paginate it again. For example, this won't work:

    .. code-block:: python

        queryset = self.final_queryset.filter(field="something")[:2]

    If you need to feed your extra-information with paginated or re-written queries out of the actual one, use :attr:`final_raw_queryset` instead.

    .. code-block:: python

        queryset = self.final_raw_queryset.filter(field="something")
        queryset = queryset[:2]

Extra arguments
===============

.. versionadded:: 0.6

Your front-end code may send you extra arguments that are not covered by the standard interface definition. These arguments will be passed down to your ``Agnocomplete`` class and can be used in the :meth:`items()` or the :meth:`get_dataset()` methods.

.. code-block:: python

    class AutocompleteColorExtra(AutocompleteColor):
        def items(self, query, **kwargs):
            extra = kwargs.get('extra_suff', None)
            if extra_stuff:
                change_something_in_the_search_method(extra_stuff)
            return super(AutocompleteColorExtra, self).items(query, **kwargs)

You can also override the :meth:`get_extra_arguments()` method **in your views** to eventually filter or manipulate these extra arguments. By default, :meth:`get_extra_arguments()` grabs arguments from the GET parameters that are not the `query` value.

.. code-block:: python

    class SelectizeExtraView(AutoView):
        template_name = 'selectize.html'
        title = "View using the Selectize autocomplete front library"
        form = SearchFormExtra

        def get_extra_arguments(self):
            extras = super(SelectizeExtraView, self).get_extra_arguments()
            whitelist = ['foo', 'bar']
            extras = filter(lambda x: x[0] in whitelist, extras)
            return dict(extras)

Everything is possible in the view: you can even push your custom arguments, based on your current context, the date/time, etc.

.. important::

    The result of this method must be a dictionary.

Using Extra arguments with Models/Querysets
-------------------------------------------

.. versionadded:: 0.6

In the case of a queryset-based Agnocomplete, you can also use the extra arguments in the ``Agnocomplete`` class.

The extra arguments are passed along to :meth:`items()`, and then to the :meth:`build_filtered_queryset()` method.

This method calls :meth:`build_extra_filtered_queryset()`. By default, this method returns the queryset "verbatim". You can override or overwrite this to perform custom filter on this QS.

.. code-block:: python

    class AutocompletePersonExtra(AutocompletePerson):

        def build_extra_filtered_queryset(self, queryset, **kwargs):
            location = kwargs.get('location', None)
            if location:
                queryset = queryset.filter(location__iexact=location)
            return queryset
