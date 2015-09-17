=============
The Demo Site
=============

The demo site will give you access to demo pages and eventually help you hack on features (add a new demo, integrate a new kind of field, etc).

To be able to access it, the simple was is to:

1 - create a tox dedicated environment. For example:

.. code-block:: sh

    mkvirtualenv TOX
    pip install tox

2 - build at least once, or rebuild, the "serve" tox job:

.. code-block:: sh

    tox -re serve

.. note::

    The `serve` tox job is currenly based on Python 2.7 and Django 1.7.

On the first run, this will create a sqlite database, create tables and will feed them with the initial fixtures data. Then it will launch the integrated dev server.

3 - create a superuser

Stop the dev server using Ctrl-C. Then, activate the ``serve`` virtualenv:

.. code-block:: sh

    source .tox/serve/bin/activate
    cd demo
    python manage.py createsuperuser

This will ask for a username, an email and a password (with confirmation).

Now you can relaunch the dev server using the command ``tox -e serve`` or ``python manage.py runserver``. You can then access to the demo *and* the admin site, which lives under the ``/admin/`` URL.
