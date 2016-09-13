from django.test import TestCase
from django.core.management import call_command


class LoaddataTestCase(TestCase):
    def setUp(self):
        super(LoaddataTestCase, self).setUp()
        # Explicitly load initial data, not loaded by default since Django 1.9
        # And keep this command quiet
        call_command("loaddata", "initial_data", verbosity=0)


class RegistryTestGeneric(LoaddataTestCase):

    def _test_registry_keys(self, keys):
        self.assertEqual(len(keys), 13)
        self.assertIn("AutocompleteColor", keys)
        self.assertIn("AutocompleteColorExtra", keys)
        self.assertIn("AutocompletePerson", keys)
        self.assertIn("AutocompletePersonExtra", keys)
        self.assertIn("AutocompletePersonShort", keys)
        self.assertIn("AutocompleteChoicesPages", keys)
        self.assertIn("AutocompleteChoicesPagesOverride", keys)
        self.assertIn("AutocompletePersonDomain", keys)
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


class MockRequestUser(object):

    def __init__(self, email, is_authenticated):
        self.email = email
        self._is_authenticated = is_authenticated

    def is_authenticated(self):
        return self._is_authenticated
