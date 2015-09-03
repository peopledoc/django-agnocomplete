from . import RegistryTestGeneric
from agnocomplete.register import get_autocomplete_registry


class DefaultConfigurationDiscover(RegistryTestGeneric):

    def test_autodiscover(self):
        registry = get_autocomplete_registry()
        keys = list(registry.keys())
        self._test_registry_keys(keys)
