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
    reverse('agnocomplete:agnocomplete')

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
    reverse(get_namespace() + ':agnocomplete')
