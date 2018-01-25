# -*- coding: utf8 -*-
import json

from django.test import TestCase, LiveServerTestCase
from django.core.management import call_command


class LoaddataMixin(object):
    def setUp(self):
        super(LoaddataMixin, self).setUp()
        # Explicitly load initial data, not loaded by default since Django 1.9
        # And keep this command quiet
        call_command("loaddata", "initial_data", verbosity=0)


class LoaddataTestCase(LoaddataMixin, TestCase):
    """
    Test class that loads data.

    ref: starting from Django 1.9, there's no more automatic implicit loaddata
    for initial_data fixtures.
    """


class LoaddataLiveTestCase(LoaddataMixin, LiveServerTestCase):
    """
    Test class that loads data, along with the LiveServer service activated.

    ref: starting from Django 1.9, there's no more automatic implicit loaddata
    for initial_data fixtures.
    """


class RegistryTestGeneric(LoaddataTestCase):

    def _test_registry_keys(self, keys):
        self.assertEqual(len(keys), 23)
        self.assertIn("AutocompleteColor", keys)
        self.assertIn("AutocompleteColorExtra", keys)
        self.assertIn("AutocompletePerson", keys)
        self.assertIn("AutocompletePersonExtra", keys)
        self.assertIn("AutocompletePersonShort", keys)
        self.assertIn("AutocompleteChoicesPages", keys)
        self.assertIn("AutocompleteChoicesPagesOverride", keys)
        self.assertIn("AutocompletePersonDomain", keys)
        self.assertIn("AutocompletePersonDomainSpecial", keys)
        self.assertIn("AutocompleteTag", keys)
        # Multiselect
        self.assertIn("AutocompleteColorShort", keys)
        # You're a customized URL
        self.assertNotIn("AutocompleteCustomUrl", keys)
        self.assertIn("my-autocomplete", keys)
        # Customized views demo
        self.assertNotIn("HiddenAutocomplete", keys)
        self.assertIn("AutocompleteContextTag", keys)
        # URL Proxies
        self.assertIn("AutocompleteUrlSimple", keys)
        self.assertIn("AutocompleteUrlSimplePost", keys)
        self.assertIn("AutocompleteUrlConvert", keys)
        self.assertIn("AutocompleteUrlConvertSchema", keys)
        self.assertIn("AutocompleteUrlConvertSchemaList", keys)
        self.assertIn("AutocompleteUrlConvertComplex", keys)
        self.assertIn("AutocompleteUrlSimpleAuth", keys)
        self.assertIn("AutocompleteUrlHeadersAuth", keys)
        self.assertIn("AutocompleteUrlErrors", keys)
        self.assertIn("AutocompleteUrlSimpleWithExtra", keys)


class MockRequestUser(object):

    def __init__(self, email, is_authenticated):
        self.email = email
        self._is_authenticated = is_authenticated

    def is_authenticated(self):
        return self._is_authenticated


def get_json(response, key='data'):
    data = json.loads(response.content.decode())
    if key:
        return data.get(key, None)
    return data
