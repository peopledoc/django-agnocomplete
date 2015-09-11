=================================
Changelog for django-agnocomplete
=================================

master (unreleased)
==================

Nothing happened yet.

v0.1.0 (2015-09-11)
===================

First official release, yay!

Features
--------

* Define your Autocomplete classes to offer a list of choices, based on static data or Django models,
* Customize the data source to adjust to your business logic: filter based on static flags (``is_active=True``) or on the user-context (filter users that share the same customer_id that the current user),
* Create forms with Agnocomplete-ready fields ; standard usage doesn't need anymore cutomization or tweaking,
* Integrate these barebone forms with **the JS front-end you want**. We're simply providing a simple automatically generated API,
* Customize almost everything: query size, page size, target URL, target views,...
* Read the full documentation on standard usage and customization howto's,
* Browse the demo website with simple backend/frontend samples,
* Use this lib with python 2.7, 3.3, 3.4 and Django 1.6, 1.7, 1.8 (thank you tox!).
* Use, hack, redistribute, contribute, because it's MIT-Licensed.
