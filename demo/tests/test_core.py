from django.test import TestCase
from demo.autocomplete import AutocompleteColor
from demo.autocomplete import AutocompletePerson


class AutocompleteChoicesTest(TestCase):
    def test_items(self):
        instance = AutocompleteColor()
        self.assertEqual([
            ('green', 'green'),
            ('gray', 'gray'),
            ('blue', 'blue'),
            ('grey', 'grey'),
        ],
            list(instance.items())
        )
        self.assertEqual([
            ('green', 'green'),
            ('gray', 'gray'),
            ('grey', 'grey'),
        ],
            list(instance.items(query='gr'))
        )
        self.assertEqual([
            ('green', 'green'),
            ('grey', 'grey'),
        ],
            list(instance.items(query='gre'))
        )
        self.assertEqual([
        ],
            list(instance.items(query='zzzzz'))
        )


class AutocompletePersonTest(TestCase):

    def test_items(self):
        instance = AutocompletePerson()
        items = instance.items()
        self.assertEqual(len(items), 3)
        items = instance.items(query="ali")
        self.assertEqual(len(items), 2)
        items = instance.items(query="bob")
        self.assertEqual(len(items), 1)
        items = instance.items(query="zzzzz")
        self.assertEqual(len(items), 0)

    def test_queryset(self):
        instance = AutocompletePerson()
        items = instance.get_queryset()
        self.assertEqual(items.count(), 3)
        items = instance.get_queryset(query="ali")
        self.assertEqual(items.count(), 2)
        items = instance.get_queryset(query="bob")
        self.assertEqual(items.count(), 1)
        items = instance.get_queryset(query="zzzzz")
        self.assertEqual(items.count(), 0)
