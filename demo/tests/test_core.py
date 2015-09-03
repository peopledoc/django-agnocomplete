from django.test import TestCase
from demo.autocomplete import AutocompleteColor
from demo.autocomplete import AutocompletePerson


class AutocompleteChoicesTest(TestCase):
    def test_items(self):
        instance = AutocompleteColor()
        self.assertEqual(list(instance.items()), [])
        self.assertEqual(
            list(instance.items(query='gr')), [
                {'value': 'green', 'label': 'green'},
                {'value': 'gray', 'label': 'gray'},
                {'value': 'grey', 'label': 'grey'},
            ]
        )

        self.assertEqual(
            list(instance.items(query='gre')), [
                {'value': 'green', 'label': 'green'},
                {'value': 'grey', 'label': 'grey'},
            ],
        )
        self.assertEqual(
            list(instance.items(query='zzzzz')),
            []
        )


class AutocompletePersonTest(TestCase):

    def test_items(self):
        instance = AutocompletePerson()
        items = instance.items()
        self.assertEqual(len(items), 0)
        items = instance.items(query="ali")
        self.assertEqual(len(items), 2)
        items = instance.items(query="bob")
        self.assertEqual(len(items), 1)
        items = instance.items(query="zzzzz")
        self.assertEqual(len(items), 0)

    def test_queryset(self):
        instance = AutocompletePerson()
        items = instance.get_queryset()
        self.assertEqual(items.count(), 0)
        items = instance.get_queryset(query="ali")
        self.assertEqual(items.count(), 2)
        items = instance.get_queryset(query="bob")
        self.assertEqual(items.count(), 1)
        items = instance.get_queryset(query="zzzzz")
        self.assertEqual(items.count(), 0)
