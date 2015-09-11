# -*- coding: utf8 -*-
import json

from django.core.urlresolvers import reverse
from django.utils.encoding import force_text as text
from django.contrib.auth.models import User

from agnocomplete import get_namespace

from ..models import Person
from . import RegistryTestGeneric


def get_json(response, key='data'):
    data = json.loads(response.content.decode())
    if key:
        return data.get(key, None)
    return data


class NamespaceGeneric(object):

    def setUp(self):
        super(NamespaceGeneric, self).setUp()
        self.catalog_url_name = get_namespace() + ':catalog'
        self.ac_url_name = get_namespace() + ':agnocomplete'


class CatalogViewTest(NamespaceGeneric, RegistryTestGeneric):

    def test_get(self):
        response = self.client.get(reverse(self.catalog_url_name))
        data = get_json(response)
        self._test_registry_keys(data)


class AgnocompleteViewTest(NamespaceGeneric, RegistryTestGeneric):

    def test_get_404(self):
        response = self.client.get(reverse(self.ac_url_name, args=['MEUH']))
        self.assertEqual(response.status_code, 404)

    def test_custom_slug(self):
        response = self.client.get(
            reverse(self.ac_url_name, args=['my-autocomplete']))
        self.assertEqual(response.status_code, 200)


class AutocompleteViewTestGeneric(NamespaceGeneric):
    view_key = "PLEASE DEFINE ME"

    def setUp(self):
        super(AutocompleteViewTestGeneric, self).setUp()
        self.url = reverse(self.ac_url_name, args=[self.view_key])

    def test_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_noquery(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        # No query, the dataset should be empty
        self.assertFalse(data)

    def test_empty_query(self):
        response = self.client.get(
            self.url,
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
        self.alice3 = Person.objects.get(pk=4)
        self.alice4 = Person.objects.get(pk=5)

    def test_autocomplete_person_queries(self):
        response = self.client.get(
            self.url,
            data={"q": "ali"}
        )
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        # query, the dataset has 4 records
        self.assertTrue(data)
        self.assertEqual(len(data), 4)
        self.assertIn({
            "value": text(self.alice1.pk),
            "label": text(self.alice1)},
            data
        )
        self.assertIn({
            "value": text(self.alice2.pk),
            "label": text(self.alice2)},
            data
        )
        self.assertIn({
            "value": text(self.alice3.pk),
            "label": text(self.alice3)},
            data
        )
        self.assertIn({
            "value": text(self.alice4.pk),
            "label": text(self.alice4)},
            data
        )

    def test_autocomplete_person_paginated(self):
        response = self.client.get(
            self.url,
            data={"q": "ali", "page_size": 3}
        )
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        # query, the dataset has 4 records
        self.assertTrue(data)
        self.assertEqual(len(data), 3)


class AutocompleteColorViewTest(AutocompleteViewTestGeneric,
                                RegistryTestGeneric):
    view_key = 'AutocompleteColor'


class SearchContextFormTest(AutocompleteViewTestGeneric,
                            RegistryTestGeneric):
    view_key = 'AutocompletePersonDomain'

    def test_search_unauthorized(self):
        response = self.client.get(self.url, data={"q": "ali"})
        self.assertEqual(response.status_code, 403)

    def test_authorized_empty(self):
        User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword'
        )
        # Logged in with John
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(self.url, data={"q": "ali"})
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        self.assertFalse(data)

    def test_authorized_result(self):
        User.objects.create_user(
            'bob', 'bob@example.com', 'bobpassword'
        )
        # Logged in with Bob
        self.client.login(username='bob', password='bobpassword')
        response = self.client.get(self.url, data={"q": "ali"})
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        self.assertTrue(data)


class CustomizedViewsTest(RegistryTestGeneric):

    @property
    def url(self):
        return reverse('hidden-autocomplete')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        # No query, the dataset should be empty
        self.assertFalse(data)

    def test_empty_query(self):
        response = self.client.get(
            self.url,
            data={"q": ""}
        )
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        # No query, the dataset should be empty
        self.assertFalse(data)

    def test_query_color(self):
        response = self.client.get(
            self.url,
            data={"q": "gre"}
        )
        self.assertEqual(response.status_code, 200)
        data = get_json(response)
        self.assertTrue(data)
