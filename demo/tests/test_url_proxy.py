"""
Tests for URL Proxy views
"""
from django.test import LiveServerTestCase
from django.test import override_settings
from django.utils.encoding import force_text as text

import mock

from ..autocomplete import AutocompleteUrlSimple, AutocompleteUrlConvert
from .. import DATABASE
RESULT_DICT = [{'value': text(item['pk']), 'label': text(item['name'])} for item in DATABASE]  # noqa


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
                    {'value': '1', 'label': 'first person'},
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


@override_settings(
    AGNOCOMPLETE_DEFAULT_QUERYSIZE=2,
    AGNOCOMPLETE_MIN_QUERYSIZE=2,
    HTTP_HOST='',
)
class AutocompleteUrlConvertTest(LiveServerTestCase):
    """
    The AutocompleteUrlConvert does not use the same value/label keys.
    """
    def test_search(self):
        instance = AutocompleteUrlConvert()
        # "mock" Change URL by adding the host
        search_url = instance.search_url
        with mock.patch('demo.autocomplete.AutocompleteUrlConvert'
                        '.get_search_url') as mock_auto:
            mock_auto.return_value = self.live_server_url + search_url
            self.assertEqual(
                list(instance.items(query='person')), RESULT_DICT
            )
            # Search for first person
            self.assertEqual(
                list(instance.items(query='first')), [
                    {'value': '1', 'label': 'first person'},
                ],
            )
