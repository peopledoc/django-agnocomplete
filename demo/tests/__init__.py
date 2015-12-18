from django.test import TestCase


class RegistryTestGeneric(TestCase):

    def _test_registry_keys(self, keys):
        self.assertEqual(len(keys), 9)
        self.assertIn("AutocompleteColor", keys)
        self.assertIn("AutocompletePerson", keys)
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


class MockRequestUser(object):

    def __init__(self, email, is_authenticated):
        self.email = email
        self._is_authenticated = is_authenticated

    def is_authenticated(self):
        return self._is_authenticated
