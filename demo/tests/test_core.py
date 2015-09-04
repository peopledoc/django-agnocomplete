from django.test import TestCase

from agnocomplete import constants

from demo.autocomplete import (
    AutocompleteColor,
    AutocompletePerson,
    AutocompleteChoicesPages,
    AutocompleteChoicesPagesOverride
)


class AutocompleteColorTest(TestCase):
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


class AutcompleteChoicesPagesTest(TestCase):

    def test_items_defaultsize(self):
        instance = AutocompleteChoicesPages()
        result = list(instance.items(query='choice'))
        # item number is greater than the default page size
        self.assertEqual(
            len(result),
            constants.AGNOCOMPLETE_DEFAULT_PAGESIZE
        )

    def test_get_page_size(self):
        instance = AutocompleteChoicesPages()
        self.assertEqual(
            instance.get_page_size(), constants.AGNOCOMPLETE_DEFAULT_PAGESIZE)
        # over the limit params, back to default
        instance = AutocompleteChoicesPages(page_size=1000)
        self.assertEqual(
            instance.get_page_size(), constants.AGNOCOMPLETE_DEFAULT_PAGESIZE)
        instance = AutocompleteChoicesPages(page_size=1)
        self.assertEqual(
            instance.get_page_size(), constants.AGNOCOMPLETE_DEFAULT_PAGESIZE)
        # Reasonable overriding
        instance = AutocompleteChoicesPages(page_size=7)
        self.assertEqual(instance.get_page_size(), 7)


class AutocompleteChoicesPagesOverrideTest(TestCase):

    def test_items_page_size(self):
        instance = AutocompleteChoicesPagesOverride()
        result = list(instance.items(query='choice'))
        # item number is greater than the default page size
        self.assertNotEqual(
            len(result),
            constants.AGNOCOMPLETE_DEFAULT_PAGESIZE
        )
        self.assertEqual(len(result), 30)

    def test_get_page_size(self):
        instance = AutocompleteChoicesPagesOverride()
        self.assertEqual(instance.get_page_size(), 30)
        # over the limit params, back to default
        instance = AutocompleteChoicesPagesOverride(page_size=1000)
        self.assertEqual(instance.get_page_size(), 30)
        instance = AutocompleteChoicesPagesOverride(page_size=1)
        self.assertEqual(instance.get_page_size(), 30)
        # Reasonable overriding
        instance = AutocompleteChoicesPagesOverride(page_size=12)
        self.assertEqual(instance.get_page_size(), 12)


class AutocompletePersonTest(TestCase):

    def test_items(self):
        instance = AutocompletePerson()
        items = instance.items()
        self.assertEqual(len(items), 0)
        items = instance.items(query="ali")
        self.assertEqual(len(items), 4)
        items = instance.items(query="bob")
        self.assertEqual(len(items), 1)
        items = instance.items(query="zzzzz")
        self.assertEqual(len(items), 0)

    def test_queryset(self):
        instance = AutocompletePerson()
        items = instance.get_queryset()
        self.assertEqual(items.count(), 0)
        items = instance.get_queryset(query="ali")
        self.assertEqual(items.count(), 4)
        items = instance.get_queryset(query="bob")
        self.assertEqual(items.count(), 1)
        items = instance.get_queryset(query="zzzzz")
        self.assertEqual(items.count(), 0)

    def test_get_page_size(self):
        instance = AutocompletePerson()
        self.assertEqual(
            instance.get_page_size(), constants.AGNOCOMPLETE_DEFAULT_PAGESIZE)
        # over the limit params, back to default
        instance = AutocompletePerson(page_size=1000)
        self.assertEqual(
            instance.get_page_size(), constants.AGNOCOMPLETE_DEFAULT_PAGESIZE)
        instance = AutocompletePerson(page_size=1)
        self.assertEqual(
            instance.get_page_size(), constants.AGNOCOMPLETE_DEFAULT_PAGESIZE)
        # Reasonable overriding
        instance = AutocompletePerson(page_size=7)
        self.assertEqual(instance.get_page_size(), 7)

    def test_paginated_search(self):
        instance = AutocompletePerson(page_size=3)
        # The queryset is not paginated.
        items = instance.get_queryset(query="ali")
        self.assertEqual(items.count(), 4)
        # The "items" method returns paginated objects
        items = instance.items(query="ali")
        self.assertEqual(len(items), 3)
