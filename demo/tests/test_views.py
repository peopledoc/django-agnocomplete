# -*- coding: utf8 -*-
import json

from django.core.urlresolvers import reverse
from django.utils.encoding import force_text

from ..models import Person
from . import RegistryTestGeneric


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
        self.assertEqual(response.status_code, 404)


class AutocompleteViewTestGeneric(object):
    view_key = "PLEASE DEFINE ME"

    def test_url(self):
        response = self.client.get(
            reverse('autocomplete:autocomplete', args=[self.view_key]))
        self.assertEqual(response.status_code, 200)

    def test_noquery(self):
        response = self.client.get(
            reverse('autocomplete:autocomplete', args=[self.view_key]),
        )
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        # No query, the dataset should be empty
        self.assertFalse(data)

    def test_empty_query(self):
        response = self.client.get(
            reverse('autocomplete:autocomplete', args=[self.view_key]),
            data={"q": ""}
        )
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        # No query, the dataset should be empty
        self.assertFalse(data)


class AutocompletePersonViewTest(AutocompleteViewTestGeneric,
                                 RegistryTestGeneric):
    view_key = 'AutocompletePerson'

    def setUp(self):
        super(AutocompletePersonViewTest, self).setUp()
        self.alice1 = Person.objects.get(pk=1)
        self.alice2 = Person.objects.get(pk=2)
        self.bob = Person.objects.get(pk=3)

    def test_autocomplete_person_queries(self):
        response = self.client.get(
            reverse('autocomplete:autocomplete', args=['AutocompletePerson']),
            data={"q": "ali"}
        )
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        # No query, the dataset should be empty
        self.assertTrue(data)
        self.assertEqual(len(data), 2)
        self.assertIn({
            "value": force_text(self.alice1.pk),
            "label": force_text(self.alice1)},
            data
        )
        self.assertIn({
            "value": force_text(self.alice2.pk),
            "label": force_text(self.alice2)},
            data
        )


class AutocompleteColorViewTest(AutocompleteViewTestGeneric,
                                RegistryTestGeneric):
    view_key = 'AutocompleteColor'
