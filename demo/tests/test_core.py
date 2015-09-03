from django.test import TestCase
from demo.autocomplete import AutocompleteColor
from demo.autocomplete import AutocompletePerson


class AutocompleteChoicesTest(TestCase):
    def test_items(self):
        instance = AutocompleteColor()
        self.assertEquals([
            ('green', 'green'),
            ('gray', 'gray'),
            ('blue', 'blue'),
            ('grey', 'grey'),
        ],
            list(instance.items())
        )


class AutocompletePersonTest(TestCase):

    def test_items(self):
        instance = AutocompletePerson()
        items = instance.items()
        self.assertEquals(items.count(), 3)
