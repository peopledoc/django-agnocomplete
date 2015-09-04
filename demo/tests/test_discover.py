from . import RegistryTestGeneric
from agnocomplete.register import get_agnocomplete_registry


class DefaultConfigurationDiscover(RegistryTestGeneric):

    def test_autodiscover(self):
        registry = get_agnocomplete_registry()
        keys = list(registry.keys())
        self._test_registry_keys(keys)
