=====================
Custom views and URLs
=====================

For some reason, the automatically generated URLs don't fit your architecture. Or you want/need custom URLs that are behind a more complex URL architecture. There are several points that are customizable in ``django-agnocomplete``.

Namespace
=========

By default, the view namespace is ``agnocomplete``. If you want to refer to the
Catalog view or any Agnocomplete view, they're fetchable with:

.. code-block:: python

    from django.core.urlresolvers import reverse

    reverse('agnocomplete:catalog')
    reverse('agnocomplete:agnocomplete', args=['AutocompleteName'])

Nothing forces you to use the ``agnocomplete`` namespace. You can set the ``AGNOCOMPLETE_NAMESPACE`` in your settings to override this. When defining your URLs, you can then use the following:

.. code-block:: python

    from agnocomplete import get_namespace

    urlpatters = [
        # ... some patterns
        url(
            r'^agnocomplete/',
            include('agnocomplete.urls', namespace=get_namespace())
        ),
        # Other patterns
    ]

You can also use the :func:`get_namespace()` function to retrieve your custom URLs.

.. code-block:: python

    from django.core.urlresolvers import reverse
    from agnocomplete import get_namespace

    reverse(get_namespace() + ':catalog')
    reverse(get_namespace() + ':agnocomplete', args=['AutocompleteName'])

Slugs
=====

By default, the slugs used for URLs are using the class name. Even though you normally don't have access to this URL by hand, you may want to customize it, simplify it, crypt it in some way. Any ``Agnocomplete`` class can have a slug class or instance property, like this:

.. code-block:: python


    class AutocompleteCustomUrl(AgnocompleteChoices):
        choices = (
            ('green', 'Green'),
            ('gray', 'Gray'),
            ('blue', 'Blue'),
            ('grey', 'Grey'),
        )
        slug = 'colors'

So, instead of accessing this using::

    /autocomplete/autocomplete/AutocompleteCustomUrl

it'll be accessible with this much cooler URL::

    /autocomplete/autocomplete/colors

Views
=====

Let's say you need to check permissions on a specific autocomplete, and you need it to be completely isolated from the automatic registry. Fine, you still can.

Let's consider a simple ``Agnocomplete`` class:

.. code-block:: python

    class HiddenAutocomplete(AgnocompleteChoices):
        choices = (
            ('green', 'Green'),
            ('gray', 'Gray'),
            ('blue', 'Blue'),
            ('grey', 'Grey'),
        )

This class doesn't have to live in an ``autocomplete.py`` module. It doesn't have to be registered.

Then, build an view:

.. code-block:: python

    from agnocomplete.views import AgnocompleteGenericView
    from arandom.place import HiddenAutocomplete

    class HiddenAutocompleteView(AgnocompleteGenericView):
        klass = HiddenAutocomplete

    hidden_autocomplete = HiddenAutocompleteView.as_view()

Join this view with a custom URL:

.. code-block:: python

    url(r'^hidden/$',
        'arandom.views.hidden_autocomplete', name='hidden_autocomplete'),

That's (almost) it. You can already call the URL ``/hidden`` and query it using the ``q`` or ``page_size`` parameter.

To make sure everything is okay, simply run your server (let's say it's talking on ``http://127.0.0.1:8000/``)

.. code-block:: sh

    curl http://127.0.0.1:8000/hidden/
    {"data": []}
    curl http://127.0.0.1:8000/hidden/?q=gre
    {"data": [
        {"label": "Green", "value": "green"},
        {"label": "Grey", "value": "grey"}]
    }

Then you can apply any access control method on your view (login_required, permission_required, etc) ; it's like a normal view.

Using your custom view with fields
----------------------------------

Since your Agnocomplete class is not registered in the ``agnocomplete`` registry, it can't be used like other ``Agnocomplete`` fields, using the automatic registry URL guessing.

Here's how to build a form which is ready to use your custom view:

.. code-block:: python

    from django.core.urlresolvers import reverse_lazy

    class SearchCustom(forms.Form):
        search_color = fields.AgnocompleteField(
            HiddenAutocomplete(url=reverse_lazy('hidden_autocomplete')),
        )

.. important::

    At this point, you **must** use :func:`reverse_lazy` to make sure that this
    URL will be evaluated when needed, and not before the Django applications are ready.


Final customization
###################

In the previous case, you *have* to use an instance of your Agnocomplete class. Alternatively, you can override the ``url`` class property.

.. code-block:: python

    class HiddenAutocompleteURL(AutocompleteColor):
        query_size_min = 2
        url = '/stuff'

    class HiddenAutocompleteReverseURL(AutocompleteColor):
        query_size_min = 2
        url = '/stuff'
