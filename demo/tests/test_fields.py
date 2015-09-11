from django.test import TestCase
from django.core.urlresolvers import reverse

from agnocomplete.fields import AgnocompleteField
from agnocomplete.exceptions import UnregisteredAgnocompleteException

from demo.autocomplete import (
    AutocompleteColor,
    HiddenAutocompleteURL,
    HiddenAutocompleteURLReverse
)


class AgnocompleteInstanceTest(TestCase):

    def test_instance(self):
        field = AgnocompleteField(AutocompleteColor())
        self.assertTrue(field.agnocomplete)
        self.assertTrue(isinstance(field.agnocomplete, AutocompleteColor))

    def test_class(self):
        field = AgnocompleteField(AutocompleteColor)
        self.assertTrue(field.agnocomplete)
        self.assertTrue(isinstance(field.agnocomplete, AutocompleteColor))

    def test_string(self):
        field = AgnocompleteField('AutocompleteColor')
        self.assertTrue(field.agnocomplete)
        self.assertTrue(isinstance(field.agnocomplete, AutocompleteColor))

    def test_unkown_string(self):
        with self.assertRaises(UnregisteredAgnocompleteException):
            AgnocompleteField('MEUUUUUUH')

    def test_instance_url(self):
        field = AgnocompleteField(AutocompleteColor())
        self.assertFalse(field.agnocomplete.get_url())
        field = AgnocompleteField(AutocompleteColor(url='/something'))
        self.assertEqual(field.agnocomplete.get_url(), '/something')

    def test_class_url(self):
        field = AgnocompleteField(HiddenAutocompleteURL())
        self.assertEqual(field.agnocomplete.get_url(), '/stuff')
        field = AgnocompleteField(HiddenAutocompleteURL)
        self.assertEqual(field.agnocomplete.get_url(), '/stuff')

    def test_class_url_reversed(self):
        field = AgnocompleteField(HiddenAutocompleteURLReverse())
        self.assertEqual(
            "{}".format(field.agnocomplete.get_url()),
            reverse('hidden-autocomplete')
        )
        field = AgnocompleteField(HiddenAutocompleteURLReverse)
        self.assertEqual(
            "{}".format(field.agnocomplete.get_url()),
            reverse('hidden-autocomplete')
        )
