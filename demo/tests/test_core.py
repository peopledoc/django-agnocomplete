# -*- coding: utf8 -*-
from django.conf import settings
from django.test import TestCase
from django.utils.encoding import force_text as text
try:
    from django.test import override_settings
except ImportError:
    # Django 1.6
    from django.test.utils import override_settings

from agnocomplete import constants
from agnocomplete.exceptions import AuthenticationRequiredAgnocompleteException

from demo.autocomplete import (
    AutocompleteColor,
    AutocompletePerson,
    AutocompleteChoicesPages,
    AutocompleteChoicesPagesOverride,
    AutocompletePersonQueryset,
    AutocompletePersonMisconfigured,
    AutocompletePersonDomain
)
from demo.models import Person
from demo.tests import MockRequestUser


# Should work with this query size
@override_settings(
    AGNOCOMPLETE_DEFAULT_QUERYSIZE=2,
    AGNOCOMPLETE_MIN_QUERYSIZE=2,
)
class AutocompleteColorTest(TestCase):
    def test_items(self):
        instance = AutocompleteColor()
        self.assertEqual(list(instance.items()), [])
        # Limit is 2, a 1-char-long query should be empty
        self.assertEqual(list(instance.items(query='g')), [])
        # Starting from 2 chars, it's okay
        self.assertEqual(
            list(instance.items(query='gr')), [
                {'value': 'green', 'label': 'Green'},
                {'value': 'gray', 'label': 'Gray'},
                {'value': 'grey', 'label': 'Grey'},
            ]
        )

        self.assertEqual(
            list(instance.items(query='gre')), [
                {'value': 'green', 'label': 'Green'},
                {'value': 'grey', 'label': 'Grey'},
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
        self.assertEqual(result, [('grey', 'Grey')])
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

    def test_get_query_size(self):
        instance = AutocompleteChoicesPagesOverride()
        self.assertNotEqual(
            instance.get_query_size(), settings.AGNOCOMPLETE_DEFAULT_QUERYSIZE)
        self.assertNotEqual(
            instance.get_query_size_min(), settings.AGNOCOMPLETE_MIN_QUERYSIZE)
        self.assertEqual(
            instance.get_query_size(),
            AutocompleteChoicesPagesOverride.query_size)
        self.assertEqual(
            instance.get_query_size_min(),
            AutocompleteChoicesPagesOverride.query_size_min)


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

    def test_get_model(self):
        instance = AutocompletePerson()
        self.assertEqual(Person, instance.get_model())
        instance = AutocompletePersonQueryset()
        self.assertEqual(Person, instance.get_model())


class AutocompletePersonTest(TestCase):

    def test_items(self):
        instance = AutocompletePerson()
        items = instance.items()
        self.assertEqual(len(items), 0)
        # Limit is "2"
        items = instance.items(query="a")
        self.assertEqual(len(items), 0)
        # Should be okay now
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


class RequiresAuthenticationTest(TestCase):

    def test_does_not_require(self):
        instance = AutocompletePerson()
        self.assertTrue(instance.user is None)

    def test_requires(self):

        mock_unauth_user = MockRequestUser('joe@example.com', False)
        mock_auth_user = MockRequestUser('joe2@example.com', True)

        instance = AutocompletePersonDomain()
        self.assertTrue(instance.user is None)
        with self.assertRaises(AuthenticationRequiredAgnocompleteException):
            instance.items(query="ali")

        instance = AutocompletePersonDomain(mock_unauth_user)
        self.assertFalse(instance.user is None)
        # Unauthenticated user
        with self.assertRaises(AuthenticationRequiredAgnocompleteException):
            instance.items(query="ali")

        instance = AutocompletePersonDomain(user=mock_auth_user)
        # Should be fine
        self.assertFalse(instance.user is None)
        self.assertTrue(instance.items(query="ali"))


class SettingsLoadingTest(TestCase):

    # Using the default settings based on constants
    @override_settings(
        AGNOCOMPLETE_DEFAULT_PAGESIZE=None,
        AGNOCOMPLETE_MAX_PAGESIZE=None,
        AGNOCOMPLETE_MIN_PAGESIZE=None,
    )
    def test_no_settings_pagesize(self):
        instance = AutocompleteColor()
        # These are set by configuration
        self.assertEqual(
            instance._page_size, constants.AGNOCOMPLETE_DEFAULT_PAGESIZE)
        self.assertEqual(
            instance._conf_page_size_max, constants.AGNOCOMPLETE_MAX_PAGESIZE)
        self.assertEqual(
            instance._conf_page_size_min, constants.AGNOCOMPLETE_MIN_PAGESIZE)

    # Using the default settings based on constants
    @override_settings(
        AGNOCOMPLETE_DEFAULT_QUERYSIZE=None,
        AGNOCOMPLETE_MIN_QUERYSIZE=None,
    )
    def test_no_settings_querysize(self):
        instance = AutocompleteColor()
        # These are set by configuration
        self.assertEqual(
            instance.get_query_size(),
            constants.AGNOCOMPLETE_DEFAULT_QUERYSIZE)
        self.assertEqual(
            instance.get_query_size_min(),
            constants.AGNOCOMPLETE_MIN_QUERYSIZE)

    def test_no_override_pagesize(self):
        instance = AutocompleteColor()
        # These are set by configuration
        self.assertEqual(
            instance._page_size, settings.AGNOCOMPLETE_DEFAULT_PAGESIZE)
        self.assertEqual(
            instance._conf_page_size_max, settings.AGNOCOMPLETE_MAX_PAGESIZE)
        self.assertEqual(
            instance._conf_page_size_min, settings.AGNOCOMPLETE_MIN_PAGESIZE)

    def test_no_override_querysize(self):
        instance = AutocompleteColor()
        # These are set by configuration
        self.assertEqual(
            instance.get_query_size(), settings.AGNOCOMPLETE_DEFAULT_QUERYSIZE)
        self.assertEqual(
            instance.get_query_size_min(), settings.AGNOCOMPLETE_MIN_QUERYSIZE)
