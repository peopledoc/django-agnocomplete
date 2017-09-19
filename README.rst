============================
Django Agnostic Autocomplete
============================


.. image:: https://travis-ci.org/novafloss/django-agnocomplete.svg?branch=master
    :target: https://travis-ci.org/novafloss/django-agnocomplete


Heavily based on `django-autocomplete-light v2 <https://github.com/yourlabs/django-autocomplete-light/>`_ workflow and concepts, this toolkit offers a front-end agnostic way to get fields for autocompletion.

It will provide:

* a simple and configurable entry-point management,
* a REST-like HTTP API to search for results,
* Fields and widgets that will make the interface between our Django code and *your* Javascript.

Status
======

Beta, used in production.

Install
=======

.. code:: sh

    $ pip install django-agnocomplete

Or add ``django-agnocomplete`` to your project requirements.

Documentation
=============

`The full documentation is browsable on RTFD <http://django-agnocomplete.readthedocs.org/en/latest/>`_


Tests
=====

Install ``tox`` in your environment (it could be a virtualenv) and run:

.. code:: sh

    $ tox

It'll run the tests for all the combinations of the following:

* Python 2.7, 3.4, 3.5.
* Django 1.8, 1.9, 1.10, 1.11.

and a ``flake8`` check.

.. note::

    The combination Python 3.3 and Django 1.9 is incompatible - `see Django 1.9 release notes <https://docs.djangoproject.com/en/1.10/releases/1.9/>`_

Are you a developer?
--------------------

To target a specific test case, use the following:

.. code:: sh

    $ tox -e py27-django18 --  demo.tests.test_core.AutocompleteChoicesPagesOverrideTest

Everything after the double-dash will be passed to the django-admin.py test command.

If you need to install a debugger (let's say `ipdb`), you can use the ``TOX_EXTRA`` environment variable like this:

.. code:: sh

    $ TOX_EXTRA=ipdb tox -e py27-django18

.. note::

    We've got a self documented Makefile for common tasks, such as running the tests, building the docs, etc.

Run the demo
============

The (draft) demo site can be browsed using the Django devserver. Run:

.. code:: sh

    $ make serve

It will run a syncdb (it may ask you questions) and then a runserver with your current ``demo.settings``. You can browse the (very rough) website at http://127.0.0.1:8000/. You can add
any runserver options you want using the `tox` positional parameters, like this:

.. code:: sh

    $ tox -e serve -- 9090  # to change the listening port


Here you'll be able to see that ``django-agnocomplete`` has been easily and rapidly integrated with ``selectize.js``, ``select2``, ``jquery-autocomplete`` and ``typeahead``. With the same backend, you can plug the JS front-end you want.

Troubles running the demo?
--------------------------

This demo project is not build as a production-ready application, models can change, but there's no migration in it. If you have database errors, you can try to remove it using:

.. code:: sh

    $ make clean-db

Or, for more radical cleanup:

.. code:: sh

    $ make clean-all


License
=======

This piece of software is being published under the terms of the MIT License. Please read the `LICENSE` file for more details.
