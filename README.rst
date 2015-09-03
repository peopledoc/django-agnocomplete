============================
Django Agnostic Autocomplete
============================

Heavily based on `django-autcomplete-light <https://github.com/yourlabs/django-autocomplete-light/>`_ workflow and concepts, this toolkit offers a front-end agnostic way to get fields for autocompletion.

It will provide:

* a simple and configurable entry-point management,
* a REST-like HTTP API to search for results,
* Fields and widgets that will make the interface between our Django code and *your* Javascript.

Status
======

Under construction. Warning, fresh paint.

Roadmap
-------

(incomplete roadmap, but hey, it's better than nothing)

- [ ] Empty query should return an empty dataset.
- [ ] Returned data should be objects of the form: ```{"value": "my value", "label": "My Label"}```
- [ ] page_size:
    - [ ] As a backend parameter, it has a minimum value, a max value and a default value.
    - [ ] ``page_size`` as a client argument: ``page_size`` argument to override the default. Although this argument can't be over limits.
- [ ] ``query_size`` :
    - [ ] as a backend parameter, it has a minimum value, a max value and a default value.
    - [ ] ``query_size`` as a client argument: ``query_size`` argument to override the default. Although this argument can't be over limits.


Install
=======

At the moment, it's only a manual install::

    pip install -e ./
