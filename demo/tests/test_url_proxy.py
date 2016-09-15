"""
Tests for URL Proxy views
"""
import json

from django.test import TestCase, LiveServerTestCase
from django.core.urlresolvers import reverse
from django.test import override_settings
from django.utils.encoding import force_text as text

import mock

from ..autocomplete import AutocompleteUrlSimple
from ..views_proxy import DATABASE
RESULT_DICT = [{'value': item['pk'], 'label': item['name']} for item in DATABASE]  # noqa


class UrlProxySimpleTest(TestCase):

    def test_simple_query(self):
        response = self.client.get(
            reverse('url-proxy:simple'), {'q': 'person'})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode())
        self.assertIn('data', result)
        data = result['data']
        # Result data is a list
        self.assertTrue(isinstance(data, list))
        # Result data is not empty
        self.assertTrue(data)
        self.assertEqual(len(data), len(DATABASE))
        for item in data:
            self.assertIn('value', item)
            self.assertIn('label', item)
            # The label contains "person"
            self.assertIn('person', item['label'])

    def test_single(self):
        response = self.client.get(
            reverse('url-proxy:simple'), {'q': 'first'})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode())
        self.assertIn('data', result)
        data = result['data']
        # Result data is a list
        self.assertTrue(isinstance(data, list))
        # Result data is not empty
        self.assertTrue(data)
        self.assertEqual(len(data), 1)

    def test_empty_query(self):
        response = self.client.get(
            reverse('url-proxy:simple'), {'q': 'lorem ipsum'})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode())
        self.assertIn('data', result)
        data = result['data']
        # Result data is a list
        self.assertTrue(isinstance(data, list))
        # Result data is empty
        self.assertFalse(data)

    def test_item(self):
        response = self.client.get(reverse('url-proxy:item', args=[4]))
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode())
        self.assertIn('data', result)
        data = result['data']
        # Result data is a list
        self.assertTrue(isinstance(data, list))
        # Result data is not empty
        self.assertTrue(data)
        self.assertEqual(len(data), 1)
        item = data[0]
        self.assertIn('value', item)
        self.assertIn('label', item)
        # The label is "first person"
        self.assertEqual(item['label'], 'fourth person')

    def test_item_unknown(self):
        response = self.client.get(reverse('url-proxy:item', args=[42]))
        self.assertEqual(response.status_code, 404)


@override_settings(
    AGNOCOMPLETE_DEFAULT_QUERYSIZE=2,
    AGNOCOMPLETE_MIN_QUERYSIZE=2,
    HTTP_HOST='',
)
class AutocompleteUrlSimpleTest(LiveServerTestCase):

    def test_search(self):
        instance = AutocompleteUrlSimple()
        # "mock" Change URL by adding the host
        search_url = instance.search_url
        with mock.patch('demo.autocomplete.AutocompleteUrlSimple'
                        '.get_search_url') as mock_auto:
            mock_auto.return_value = self.live_server_url + search_url
            self.assertEqual(list(instance.items()), [])
            # Limit is 2, a 1-char-long query should be empty
            self.assertEqual(list(instance.items(query='p')), [])
            # Starting from 2 chars, it's okay
            self.assertEqual(
                list(instance.items(query='person')), RESULT_DICT
            )

            self.assertEqual(
                list(instance.items(query='first')), [
                    {'value': 1, 'label': 'first person'},
                ],
            )
            self.assertEqual(
                list(instance.items(query='zzzzz')),
                []
            )

    def test_selected(self):
        instance = AutocompleteUrlSimple()
        searched_id = 1
        item_url = instance.get_item_url(searched_id)
        with mock.patch('demo.autocomplete.AutocompleteUrlSimple'
                        '.get_item_url') as mock_auto:
            mock_auto.return_value = self.live_server_url + item_url
            result = instance.selected([])
            self.assertEqual(result, [])
            result = instance.selected([searched_id])
            self.assertEqual(result, [
                (text(searched_id), text('first person'))]
            )
