# -*- coding: utf8 -*-
from django.test import TestCase
from django.utils.encoding import force_text as text
try:
    from django.test import override_settings
except ImportError:
    # Django 1.6
    from django.test.utils import override_settings

from agnocomplete import constants

from demo.autocomplete import (
    AutocompleteColor,
    AutocompletePerson,
    AutocompleteChoicesPages,
    AutocompleteChoicesPagesOverride,
    AutocompletePersonQueryset,
    AutocompletePersonMisconfigured,
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

    def test_selected(self):
        instance = AutocompleteColor()
        result = instance.selected([])
        self.assertEqual(result, [])
        result = instance.selected(['grey'])
        self.assertEqual(result, [('grey', 'grey')])
        result = instance.selected(['MEUH'])
        self.assertEqual(result, [])


# Using the default settings based on constants
@override_settings(
    AGNOCOMPLETE_DEFAULT_PAGESIZE=None,
    AGNOCOMPLETE_MAX_PAGESIZE=None,
    AGNOCOMPLETE_MIN_PAGESIZE=None,
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
        instance = AutocompleteChoicesPages(page_size=6)
        self.assertEqual(instance.get_page_size(), 6)


class AutocompleteChoicesPagesOverrideTest(TestCase):

    def test_items_page_size(self):
        instance = AutocompleteChoicesPagesOverride()
        result = list(instance.items(query='choice'))
        # item number is greater than the default page size
        self.assertNotEqual(len(result), 15)
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


class AutocompleteModelTest(TestCase):

    def test_queryset_by_model(self):
        instance = AutocompletePerson()
        items = instance.get_queryset()
        self.assertEqual(items.count(), 5)

    def test_queryset_by_queryset(self):
        instance = AutocompletePersonQueryset()
        items = instance.get_queryset()
        self.assertEqual(items.count(), 4)

    def test_misconfigured(self):
        instance = AutocompletePersonMisconfigured()
        with self.assertRaises(NotImplementedError):
            instance.get_queryset()


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

    def test_get_page_size(self):
        instance = AutocompletePerson()
        self.assertEqual(
            instance.get_page_size(), 15)
        # over the limit params, back to default
        instance = AutocompletePerson(page_size=1000)
        self.assertEqual(
            instance.get_page_size(), 15)
        instance = AutocompletePerson(page_size=1)
        self.assertEqual(
            instance.get_page_size(), 15)
        # Reasonable overriding
        instance = AutocompletePerson(page_size=7)
        self.assertEqual(instance.get_page_size(), 7)

    def test_paginated_search(self):
        instance = AutocompletePerson(page_size=3)
        # The raw queryset is not paginated.
        qs = instance.get_queryset()
        conditions = instance.get_queryset_filters(query="ali")
        items = qs.filter(conditions)
        self.assertEqual(items.count(), 4)
        # The "items" method returns paginated objects
        items = instance.items(query="ali")
        self.assertEqual(len(items), 3)

    def test_selected(self):
        instance = AutocompletePerson()
        result = instance.selected([])
        self.assertEqual(result, [])
        result = instance.selected([1])
        self.assertEqual(result, [
            (text('1'), text('Alice Iñtërnâtiônàlizætiøn'))]
        )
        result = instance.selected(['2'])
        self.assertEqual(result, [(text('2'), text('Alice Inchains'))])
        result = instance.selected(['MEUH'])
        self.assertEqual(result, [])


class SettingsLoadingTest(TestCase):

    # Using the default settings based on constants
    @override_settings(
        AGNOCOMPLETE_DEFAULT_PAGESIZE=None,
        AGNOCOMPLETE_MAX_PAGESIZE=None,
        AGNOCOMPLETE_MIN_PAGESIZE=None,
    )
    def test_no_settings(self):
        instance = AutocompleteColor()
        # These are set by configuration
        self.assertEqual(
            instance._page_size, constants.AGNOCOMPLETE_DEFAULT_PAGESIZE)
        self.assertEqual(
            instance._conf_page_size_max, constants.AGNOCOMPLETE_MAX_PAGESIZE)
        self.assertEqual(
            instance._conf_page_size_min, constants.AGNOCOMPLETE_MIN_PAGESIZE)

    def test_no_override(self):
        instance = AutocompleteColor()
        # These are set by configuration
        self.assertEqual(instance._page_size, 15)
        self.assertEqual(instance._conf_page_size_max, 120)
        self.assertEqual(instance._conf_page_size_min, 2)
