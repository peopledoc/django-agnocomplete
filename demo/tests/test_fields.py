from django.test import TestCase

from agnocomplete.fields import AgnocompleteField
from agnocomplete.exceptions import UnregisteredAgnocompleteException

from demo.autocomplete import AutocompleteColor


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
