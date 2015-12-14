===================
django-agnocomplete
===================

Heavily based on `django-autocomplete-light <https://github.com/yourlabs/django-autocomplete-light/>`_ workflow and concepts, this toolkit offers a front-end agnostic way to get fields for autocompletion.

It will provide:

* a simple and configurable entry-point management,
* a REST-like HTTP API to search for results,
* Fields and widgets that will make the interface between our Django code and *your* Javascript.

Demo
====

If you want to see it in action, simply install it as indicated in the README, run ``tox -e serve``, and point at the local devserver. You should be able to click on the "[JS DEMO]" links and see it in action. Browse the source code that lives in ``demo/templates`` to see how easy it is to interact with ``django-agnocomplete``.

So far, we've got it implemented using:

* ``selectize.js``,
* ``select2``,
* ``jquery-autocomplete``,
* ``typeahead``.


.. Contents:

.. toctree::
   :maxdepth: 2

   overview
   autocomplete-definition
   context-dependant-completions
   custom-views
   widgets
   demo-site
   admin-site

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
