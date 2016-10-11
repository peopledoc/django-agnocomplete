import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text as text

from .. import DATABASE, GOODAUTHTOKEN
from ..views_proxy import (
    MESSAGE_400,
    MESSAGE_403,
    MESSAGE_404,
    MESSAGE_405,
    MESSAGE_500,
)


class UrlProxyGenericTest(object):
    method = 'get'
    data_key = 'data'

    @property
    def http_url(self):
        raise NotImplementedError("You need a `http_url` property")

    @property
    def value_key(self):
        raise NotImplementedError("You need a `value_key` property")

    @property
    def label_key(self):
        raise NotImplementedError("You need a `label_key` property")

    @property
    def item_keys(self):
        return [self.label_key, self.value_key]

    def http_call(self, query, method='get'):
        if method == 'get':
            return self.client.get(self.http_url, {'q': query})
        return self.client.post(self.http_url, {'q': query})

    def test_simple_query(self):
        response = self.http_call('person', self.method)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode())
        self.assertIn(self.data_key, result)
        data = result[self.data_key]
        # Result data is a list
        self.assertTrue(isinstance(data, list))
        # Result data is not empty
        self.assertTrue(data)
        self.assertEqual(len(data), len(DATABASE))
        for item in data:
            for key in self.item_keys:
                self.assertIn(key, item)
            # The label contains "person"
            self.assertIn('person', item[self.label_key])

    def test_single(self):
        response = self.http_call('first', self.method)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode())
        self.assertIn(self.data_key, result)
        data = result[self.data_key]
        # Result data is a list
        self.assertTrue(isinstance(data, list))
        # Result data is not empty
        self.assertTrue(data)
        self.assertEqual(len(data), 1)

    def test_empty_query(self):
        response = self.http_call('lorem ipsum', self.method)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode())
        self.assertIn(self.data_key, result)
        data = result[self.data_key]
        # Result data is a list
        self.assertTrue(isinstance(data, list))
        # Result data is empty
        self.assertFalse(data)


class UrlProxySimpleTest(UrlProxyGenericTest, TestCase):
    http_url = reverse('url-proxy:simple')
    value_key = 'value'
    label_key = 'label'


class UrlProxyConvertTest(UrlProxyGenericTest, TestCase):
    http_url = reverse('url-proxy:convert')
    value_key = 'pk'
    label_key = 'name'


class UrlProxyConvertComplexTest(UrlProxyGenericTest, TestCase):
    http_url = reverse('url-proxy:convert-complex')
    value_key = 'pk'
    label_key = 'last_name'

    @property
    def item_keys(self):
        # Not the same here: the return format is a bit more complex
        return [self.value_key, 'first_name', 'last_name']


class UrlProxyItemTest(TestCase):

    data_key = 'data'

    def test_item(self):
        response = self.client.get(reverse('url-proxy:item', args=[4]))
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode())
        self.assertIn(self.data_key, result)
        data = result[self.data_key]
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


class UrlProxySimpleAuthTest(TestCase):

    def test_simple_query_no_auth(self):
        response = self.client.get(
            reverse('url-proxy:simple-auth'), {'q': 'person'})
        self.assertEqual(response.status_code, 403)

    def test_simple_query_wrong_auth(self):
        response = self.client.get(
            reverse('url-proxy:simple-auth'),
            {'q': 'person', 'auth_token': 'I-AM-WRONG'}
        )
        self.assertEqual(response.status_code, 403)

    def test_simple_query_auth(self):
        response = self.client.get(
            reverse('url-proxy:simple-auth'),
            {'q': 'person', 'auth_token': GOODAUTHTOKEN}
        )
        self.assertEqual(response.status_code, 200)


class UrlProxyHeadersAuthTest(TestCase):

    def test_simple_query_no_auth(self):
        response = self.client.get(
            reverse('url-proxy:headers-auth'), {'q': 'person'})
        self.assertEqual(response.status_code, 403)

    def test_simple_query_wrong_auth(self):
        response = self.client.get(
            reverse('url-proxy:headers-auth'),
            {'q': 'person'},
            HTTP_X_API_TOKEN='I-AM-WRONG',
        )
        self.assertEqual(response.status_code, 403)

    def test_simple_query_auth(self):
        response = self.client.get(
            reverse('url-proxy:headers-auth'),
            {'q': 'person'},
            HTTP_X_API_TOKEN=GOODAUTHTOKEN,
        )
        self.assertEqual(response.status_code, 200)


class UrlProxySimplePostTest(UrlProxyGenericTest, TestCase):
    http_url = reverse('url-proxy:simple-post')
    value_key = 'value'
    label_key = 'label'
    method = 'post'

    def test_get(self):
        # GET requests are forbidden
        response = self.http_call('hello', 'get')
        self.assertEqual(response.status_code, 405)


class UrlProxyConvertSchemaTest(UrlProxyGenericTest, TestCase):
    http_url = reverse('url-proxy:convert-schema')
    # Returning the standard items, but embedded in "result"
    data_key = 'result'
    value_key = 'value'
    label_key = 'label'

    def test_search_person(self):
        response = self.client.get(
            self.http_url,
            {'q': 'person'},
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode())
        # Not "data"
        self.assertNotIn('data', result)


class UrlProxyConvertSchemaListTest(TestCase):
    http_url = reverse('url-proxy:convert-schema-list')
    # Returning the standard items, but as a list

    def test_search_person(self):
        response = self.client.get(
            self.http_url,
            {'q': 'person'},
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode())
        self.assertTrue(isinstance(result, list))


class UrlProxyErrorsTest(TestCase):

    def test_400(self):
        response = self.client.get(
            reverse('url-proxy:errors'), {'q': '400'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(text(response.content), MESSAGE_400)

    def test_403(self):
        response = self.client.get(
            reverse('url-proxy:errors'), {'q': '403'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(text(response.content), MESSAGE_403)

    def test_404(self):
        response = self.client.get(
            reverse('url-proxy:errors'), {'q': '404'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(text(response.content), MESSAGE_404)

    def test_405(self):
        response = self.client.get(
            reverse('url-proxy:errors'), {'q': '405'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(text(response.content), MESSAGE_405)

    def test_500(self):
        response = self.client.get(
            reverse('url-proxy:errors'), {'q': 'whatever'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(text(response.content), MESSAGE_500)
