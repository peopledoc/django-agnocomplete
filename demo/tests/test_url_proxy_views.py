import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from .. import DATABASE


class UrlProxyGenericTest(object):

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

    def test_simple_query(self):
        response = self.client.get(self.http_url, {'q': 'person'})
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
        response = self.client.get(self.http_url, {'q': 'first'})
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
        response = self.client.get(self.http_url, {'q': 'lorem ipsum'})
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
