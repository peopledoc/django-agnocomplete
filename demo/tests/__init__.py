from django.test import TestCase


class RegistryTestGeneric(TestCase):

    def _test_registry_keys(self, keys):
        assert len(keys) == 6
        assert "AutocompleteColor" in keys
        assert "AutocompletePerson" in keys
        assert "AutocompleteChoicesPages" in keys
        assert "AutocompleteChoicesPagesOverride" in keys
        assert "AutocompletePersonDomain" in keys
        # You're a customized URL
        assert "AutocompleteCustomUrl" not in keys
        assert "my-autocomplete" in keys
        # Customized views demo
        assert "HiddenAutocomplete" not in keys


class MockRequestUser(object):

    def __init__(self, email, is_authenticated):
        self.email = email
        self._is_authenticated = is_authenticated

    def is_authenticated(self):
        return self._is_authenticated
