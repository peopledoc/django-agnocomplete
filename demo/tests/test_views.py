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


class AutocompleteViewTest(RegistryTestGeneric):

    def test_get_404(self):
        response = self.client.get(
            reverse('autocomplete:autocomplete', args=['MEUH']))
        self.assertEquals(response.status_code, 404)

    def test_autocomplete_person(self):
        response = self.client.get(
            reverse('autocomplete:autocomplete', args=['AutocompletePerson']))
        self.assertEquals(response.status_code, 200)

    def test_autocomplete_person_noquery(self):
        response = self.client.get(
            reverse('autocomplete:autocomplete', args=['AutocompletePerson']),
        )
        self.assertEquals(response.status_code, 200)
        data = get_json(response)
        # No query, the dataset should be empty
        self.assertFalse(data)

    def test_autocomplete_person_empty_query(self):
        response = self.client.get(
            reverse('autocomplete:autocomplete', args=['AutocompletePerson']),
            data={"q": ""}
        )
        self.assertEquals(response.status_code, 200)
        data = get_json(response)
        # No query, the dataset should be empty
        self.assertFalse(data)
