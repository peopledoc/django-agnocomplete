"""
Tests for URL Proxy views
"""
from django.test import LiveServerTestCase
from django.test import override_settings
from django.utils.encoding import force_text as text

import mock
from requests.exceptions import HTTPError


from ..autocomplete import (
    AutocompleteUrlSimple,
    AutocompleteUrlConvert,
    AutocompleteUrlConvertSchema,
    AutocompleteUrlConvertSchemaList,
    AutocompleteUrlConvertComplex,
    AutocompleteUrlSimpleAuth,
    AutocompleteUrlHeadersAuth,
    AutocompleteUrlSimplePost,
    AutocompleteUrlSimpleWithExtra,
)
from .. import DATABASE, GOODAUTHTOKEN
RESULT_DICT = [{'value': text(item['pk']), 'label': text(item['name'])} for item in DATABASE]  # noqa


@override_settings(HTTP_HOST='')
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


@override_settings(HTTP_HOST='')
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


@override_settings(HTTP_HOST='')
class AutocompleteUrlConvertSchemaTest(LiveServerTestCase):
    """
    The AutocompleteUrlConvertSchema URL returns a non-standard schema.
    """
    def test_search(self):
        instance = AutocompleteUrlConvertSchema()
        # "mock" Change URL by adding the host
        search_url = instance.search_url
        with mock.patch('demo.autocomplete.AutocompleteUrlConvertSchema'
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


@override_settings(HTTP_HOST='')
class AutocompleteUrlConvertSchemaListTest(LiveServerTestCase):
    """
    The AutocompleteUrlConvertSchemaList URL returns a list.
    """
    def test_search(self):
        instance = AutocompleteUrlConvertSchemaList()
        # "mock" Change URL by adding the host
        search_url = instance.search_url
        with mock.patch('demo.autocomplete.AutocompleteUrlConvertSchemaList'
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


@override_settings(HTTP_HOST='')
class AutocompleteUrlConvertComplexTest(LiveServerTestCase):
    """
    The AutocompleteUrlConvertComplex returns a different item format.
    """
    def test_search(self):
        instance = AutocompleteUrlConvertComplex()
        # "mock" Change URL by adding the host
        search_url = instance.search_url
        with mock.patch('demo.autocomplete.AutocompleteUrlConvertComplex'
                        '.get_search_url') as mock_auto:
            mock_auto.return_value = self.live_server_url + search_url
            search_result = instance.items(query='person')
            self.assertEqual(
                list(search_result), RESULT_DICT
            )
            # Search for first person
            self.assertEqual(
                list(instance.items(query='first')), [
                    {'value': '1', 'label': 'first person'},
                ],
            )


@override_settings(HTTP_HOST='')
class AutocompleteUrlSimpleAuthTest(LiveServerTestCase):
    def test_search(self):
        instance = AutocompleteUrlSimpleAuth()
        # "mock" Change URL by adding the host
        search_url = instance.search_url
        with mock.patch('demo.autocomplete.AutocompleteUrlSimpleAuth'
                        '.get_search_url') as mock_auto:
            mock_auto.return_value = self.live_server_url + search_url
            search_result = instance.items(query='person')
            self.assertEqual(
                list(search_result), RESULT_DICT
            )
            # Search for first person
            self.assertEqual(
                list(instance.items(query='first')), [
                    {'value': '1', 'label': 'first person'},
                ],
            )

    def test_query_args(self):
        instance = AutocompleteUrlSimpleAuth()
        query_args = instance.get_http_call_kwargs('hello')
        self.assertIn('q', query_args)
        self.assertIn('auth_token', query_args)
        self.assertEqual(query_args['auth_token'], GOODAUTHTOKEN)


@override_settings(HTTP_HOST='')
class AutocompleteUrlHeadersAuthTest(LiveServerTestCase):
    def test_search(self):
        instance = AutocompleteUrlHeadersAuth()
        # "mock" Change URL by adding the host
        search_url = instance.search_url
        with mock.patch('demo.autocomplete.AutocompleteUrlHeadersAuth'
                        '.get_search_url') as mock_auto:
            mock_auto.return_value = self.live_server_url + search_url
            search_result = instance.items(query='person')
            self.assertEqual(
                list(search_result), RESULT_DICT
            )
            # Search for first person
            self.assertEqual(
                list(instance.items(query='first')), [
                    {'value': '1', 'label': 'first person'},
                ],
            )

    def test_headers(self):
        instance = AutocompleteUrlHeadersAuth()
        headers = instance.get_http_headers()
        self.assertIn('X-API-TOKEN', headers)
        self.assertEqual(headers['X-API-TOKEN'], GOODAUTHTOKEN)


@override_settings(HTTP_HOST='')
class HTTPErrorHandlingTest(LiveServerTestCase):

    def test_wrong_auth_error(self):
        instance = AutocompleteUrlHeadersAuth()
        search_url = instance.search_url
        klass = 'demo.autocomplete.AutocompleteUrlHeadersAuth'
        with mock.patch(klass + '.get_search_url') as mock_auto:
            mock_auto.return_value = self.live_server_url + search_url
            with mock.patch(klass + '.get_http_headers') as mock_headers:
                mock_headers.return_value = {
                    'NOTHING': 'HERE'
                }
                with self.assertRaises(HTTPError):
                    # Raising a "requests" exception
                    instance.items(query='person')


@override_settings(HTTP_HOST='')
class AutocompleteUrlSimplePostTest(LiveServerTestCase):
    def test_search(self):
        instance = AutocompleteUrlSimplePost()
        # "mock" Change URL by adding the host
        search_url = instance.search_url
        with mock.patch('demo.autocomplete.AutocompleteUrlSimplePost'
                        '.get_search_url') as mock_auto:
            mock_auto.return_value = self.live_server_url + search_url
            search_result = instance.items(query='person')
            self.assertEqual(
                list(search_result), RESULT_DICT
            )
            # Search for first person
            self.assertEqual(
                list(instance.items(query='first')), [
                    {'value': '1', 'label': 'first person'},
                ],
            )


@override_settings(HTTP_HOST='')
class AutocompleteUrlWithExtraTest(LiveServerTestCase):
    def test_search(self):
        # Should work exactly like the AutocompleteUrlSimple
        instance = AutocompleteUrlSimpleWithExtra()
        # "mock" Change URL by adding the host
        search_url = instance.search_url
        with mock.patch('demo.autocomplete.AutocompleteUrlSimpleWithExtra'
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

    def test_search_extra(self):
        instance = AutocompleteUrlSimpleWithExtra()
        # "moo" is an easter egg value here
        self.assertEqual(
            list(instance.items(query='person', special='moo')),
            [
                {'value': 'moo', 'label': 'moo'}
            ]
        )
