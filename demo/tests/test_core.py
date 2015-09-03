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
        self.assertEquals(len(items), 3)

    def test_queryset(self):
        instance = AutocompletePerson()
        items = instance.get_queryset()
        self.assertEquals(items.count(), 3)
        items = instance.get_queryset(query="ali")
        self.assertEquals(items.count(), 2)
