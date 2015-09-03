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
        self.assertEquals([
            ('green', 'green'),
            ('gray', 'gray'),
            ('grey', 'grey'),
        ],
            list(instance.items(query='gr'))
        )
        self.assertEquals([
            ('green', 'green'),
            ('grey', 'grey'),
        ],
            list(instance.items(query='gre'))
        )
        self.assertEquals([
        ],
            list(instance.items(query='zzzzz'))
        )


class AutocompletePersonTest(TestCase):

    def test_items(self):
        instance = AutocompletePerson()
        items = instance.items()
        self.assertEquals(len(items), 3)
        items = instance.items(query="ali")
        self.assertEquals(len(items), 2)
        items = instance.items(query="bob")
        self.assertEquals(len(items), 1)
        items = instance.items(query="zzzzz")
        self.assertEquals(len(items), 0)

    def test_queryset(self):
        instance = AutocompletePerson()
        items = instance.get_queryset()
        self.assertEquals(items.count(), 3)
        items = instance.get_queryset(query="ali")
        self.assertEquals(items.count(), 2)
        items = instance.get_queryset(query="bob")
        self.assertEquals(items.count(), 1)
        items = instance.get_queryset(query="zzzzz")
        self.assertEquals(items.count(), 0)
