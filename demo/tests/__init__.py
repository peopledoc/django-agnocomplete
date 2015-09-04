from django.test import TestCase


class RegistryTestGeneric(TestCase):

    def _test_registry_keys(self, keys):
        assert len(keys) == 4
        assert "AutocompleteColor" in keys
        assert "AutocompletePerson" in keys
        assert "AutocompleteChoicesPages" in keys
        assert "AutocompleteChoicesPagesOverride" in keys
