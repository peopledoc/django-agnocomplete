from django.test import TestCase


class RegistryTestGeneric(TestCase):

    def _test_registry_keys(self, keys):
        assert len(keys) == 2
        assert "AutocompleteChoicesExample" in keys
        assert "AutocompletePerson" in keys
