import json
from . import RegistryTestGeneric
from django.core.urlresolvers import reverse


def get_json(response, key='data'):
    data = json.loads(response.content.decode())
    if key:
        return data.get(key, None)
    return data


class CatalogViewTest(RegistryTestGeneric):

    def test_get(self):
        response = self.client.get(reverse('autocomplete:catalog'))
        data = get_json(response)
        self._test_registry_keys(data)
