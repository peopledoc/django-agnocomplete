============================
Django Agnostic Autocomplete
============================

Heavily based on `django-autocomplete-light <https://github.com/yourlabs/django-autocomplete-light/>`_ workflow and concepts, this toolkit offers a front-end agnostic way to get fields for autocompletion.

It will provide:

* a simple and configurable entry-point management,
* a REST-like HTTP API to search for results,
* Fields and widgets that will make the interface between our Django code and *your* Javascript.

Status
======

Under construction. Warning, fresh paint.

Install
=======

At the moment, it's only a manual install::

    pip install -e ./

Tests
=====

Install ``tox`` in your environment (it could be a virtualenv) and run::

    tox

It'll run the tests for all the combinations of the following:

* Python 2.7, 3.3, 3.4
* Django 1.6, 1.7, 1.8

and a ``flake8`` check.

Run the demo
============

The (draft) demo site can be browsed using the Django devserver. Run::

    tox -e serve

It will run a syncdb (it may ask you questions) and then a runserver with your current ``demo.settings``. You can browse the (very rough) website at http://127.0.0.1:8000/. You can add
any runserver options you want using the `tox` positional parameters, like this::

    tox -e serve -- 9090  # to change the listening port
