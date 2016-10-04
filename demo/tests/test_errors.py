from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import override_settings
from django.core.exceptions import SuspiciousOperation

import mock
from requests.exceptions import Timeout

from agnocomplete import get_namespace

from . import get_json
from . import LoaddataLiveTestCase
from ..autocomplete import (
    # Classic search
    AutocompletePerson,
    # URL Proxies
    AutocompleteUrlSimpleAuth,
    AutocompleteUrlHeadersAuth,
)


def raise_standard_exception(*args, **kwargs):
    raise Exception("Nothing exceptional")


def raise_suspiciousoperation(*args, **kwargs):
    raise SuspiciousOperation("You are not allowed to do this")


def raise_timeout(*args, **kwargs):
    raise Timeout("Timeout")


class ErrorHandlingTest(object):
    expected_status = 500

    @property
    def klass(self):
        raise NotImplementedError("You need a `klass` property")

    @property
    def mock_function(self):
        raise NotImplementedError("You need a `mock_function` property")

    @property
    def klass_path(self):
        return '{}.{}'.format(self.klass.__module__, self.klass.__name__)

    @property
    def mock_path(self):
        paths = [self.klass_path, 'items']
        return ".".join(paths)

    @property
    def url(self):
        ac_url_name = get_namespace() + ':agnocomplete'
        return reverse(ac_url_name, args=[self.klass.__name__])

    def test_errors(self):
        with mock.patch(self.mock_path, self.mock_function):
            response = self.client.get(
                self.url,
                data={"q": "nothing important"})
            self.assertEqual(response.status_code, self.expected_status)
            data = get_json(response, 'errors')
            self.assertEqual(len(data), 1)


class ErrorHandlingAutocompletePersonTest(ErrorHandlingTest, TestCase):
    klass = AutocompletePerson
    mock_function = raise_standard_exception


class ErrorHandlingSuspiciousOperationTest(ErrorHandlingTest, TestCase):
    klass = AutocompletePerson
    mock_function = raise_suspiciousoperation
    expected_status = 400


@override_settings(HTTP_HOST='')
class ErrorHandlingURLProxySimpleAuthTest(
        ErrorHandlingTest, LoaddataLiveTestCase):
    klass = AutocompleteUrlSimpleAuth
    mock_function = raise_standard_exception

    def test_search_query_wrong_auth(self):
        # URL construct
        instance = self.klass()
        search_url = instance.search_url
        klass = self.klass_path
        with mock.patch(klass + '.get_search_url') as mock_auto:
            mock_auto.return_value = self.live_server_url + search_url
            # Search using the URL proxy view
            search_url = get_namespace() + ':agnocomplete'

            with mock.patch(klass + '.get_http_call_kwargs') as mock_headers:
                mock_headers.return_value = {
                    'auth_token': 'BADAUTHTOKEN',
                    'q': 'person',
                }
                response = self.client.get(
                    reverse(
                        search_url, args=[self.klass.__name__]),
                    data={'q': "person"}
                )
                self.assertEqual(response.status_code, 403)


@override_settings(HTTP_HOST='')
class ErrorHandlingURLProxyHeadersAuthTest(
        ErrorHandlingTest, LoaddataLiveTestCase):
    klass = AutocompleteUrlHeadersAuth
    mock_function = raise_standard_exception

    def test_search_headers_wrong_auth(self):
        # URL construct
        instance = self.klass()
        search_url = instance.search_url
        klass = self.klass_path
        with mock.patch(klass + '.get_search_url') as mock_auto:
            mock_auto.return_value = self.live_server_url + search_url
            # Search using the URL proxy view
            search_url = get_namespace() + ':agnocomplete'
            with mock.patch(klass + '.get_http_headers') as mock_headers:
                mock_headers.return_value = {
                    'NOTHING': 'HERE'
                }
                response = self.client.get(
                    reverse(
                        search_url, args=[self.klass.__name__]),
                    data={'q': "person"}
                )
                self.assertEqual(response.status_code, 403)


@override_settings(HTTP_HOST='')
class ErrorHandlingURLProxyTimeoutTest(LoaddataLiveTestCase):
    klass = AutocompleteUrlHeadersAuth

    @property
    def klass_path(self):
        return '{}.{}'.format(self.klass.__module__, self.klass.__name__)

    def test_timeout(self):
        # Search using the URL proxy view
        search_url = get_namespace() + ':agnocomplete'
        with mock.patch('requests.get', raise_timeout):
            response = self.client.get(
                reverse(
                    search_url, args=[self.klass.__name__]),
                data={'q': "person"}
            )
            self.assertEqual(response.status_code, 408)
