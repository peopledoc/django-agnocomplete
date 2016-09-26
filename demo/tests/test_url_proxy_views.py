import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from .. import DATABASE, GOODAUTHTOKEN


class UrlProxyGenericTest(object):
    method = 'get'

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
        self.assertIn('data', result)
        data = result['data']
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
        self.assertIn('data', result)
        data = result['data']
        # Result data is a list
        self.assertTrue(isinstance(data, list))
        # Result data is not empty
        self.assertTrue(data)
        self.assertEqual(len(data), 1)

    def test_empty_query(self):
        response = self.http_call('lorem ipsum', self.method)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode())
        self.assertIn('data', result)
        data = result['data']
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
