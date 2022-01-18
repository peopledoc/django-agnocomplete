from django import forms
from django.urls import reverse
from django.test import LiveServerTestCase, TestCase, override_settings
from django.core.exceptions import ValidationError
import mock

from agnocomplete import fields
from agnocomplete.exceptions import UnregisteredAgnocompleteException
from agnocomplete.fields import (
    AgnocompleteField,
    AgnocompleteMultipleField,
    AgnocompleteModelMultipleField,
)
from agnocomplete.forms import UserContextFormMixin
from demo.autocomplete import (
    AutocompleteColor,
    HiddenAutocompleteURL,
    HiddenAutocompleteURLReverse,
    AutocompleteTag,
    AutocompletePersonDomain,
    AutocompleteUrlSkipItem,
)
from demo.fields import AgnocompleteUrlProxyField
from demo.models import Tag, Person
from demo.tests import LoaddataTestCase


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


class ModelSelectTest(LoaddataTestCase):
    class _Form(UserContextFormMixin, forms.Form):
        person = fields.AgnocompleteModelField(AutocompletePersonDomain,
                                               to_field_name='email')

    def setUp(self):
        super().setUp()
        self.alice = Person.objects.get(pk=1)
        self.bob = Person.objects.get(pk=3)

        self.invalid_pk = Person.objects.order_by('pk').last().pk + 1

    def test_render(self):
        form = self._Form(
            user=None,
            data={'person': self.bob.email},
        )

        # bob is selected => only bob <option>
        html_form = "{}".format(form)
        option = '<option value="{}" {}>'.format(
            self.bob.email, 'selected')
        self.assertIn(
            option,
            html_form
        )

        self.assertNotIn(
            '<option value="{}">'.format(self.alice.email),
            html_form
        )

        # alice is selected => only alice <option>
        form = self._Form(
            user=None,
            data={'person': self.alice.email},
        )
        html_form = "{}".format(form)
        option = '<option value="{}" {}>'.format(
            self.alice.email, 'selected')
        self.assertIn(option, html_form)

        self.assertNotIn(
            '<option value="{}">'.format(self.bob.email),
            html_form
        )

    def test_render_no_selection(self):
        # none is selected => no <option>
        form = self._Form(
            user=None,
            data={'person': self.invalid_pk},
        )
        html_form = "{}".format(form)
        self.assertNotIn('<option', html_form)


class MultipleSelectTest(TestCase):
    def test_empty(self):
        field = AgnocompleteMultipleField(
            AutocompleteTag,
            required=False
        )
        self.assertEqual(field.clean(""), [])
        self.assertEqual(field.clean([]), [])
        self.assertEqual(field.clean([""]), [])


class MultipleModelSelectTest(LoaddataTestCase):
    class _Form(forms.Form):
        persons = fields.AgnocompleteModelMultipleField(
            AutocompletePersonDomain,
            to_field_name='email'
        )

    def setUp(self):
        super().setUp()
        self.alice = Person.objects.get(pk=1)
        self.bob = Person.objects.get(pk=3)

        self.aliceinchains = Person.objects.get(pk=2)
        self.aliceinchains.email = self.alice.email
        self.aliceinchains.save()

        self.invalid_pk = Person.objects.order_by('pk').last().pk + 1

    def test_empty_list(self):
        field = AgnocompleteModelMultipleField(
            AutocompleteTag,
            create_field="name",
            required=False
        )
        empty_qs = Tag.objects.none()
        self.assertQuerysetEqual(field.clean(""), empty_qs)
        self.assertQuerysetEqual(field.clean([]), empty_qs)
        self.assertQuerysetEqual(field.clean([""]), empty_qs)

    def test_render(self):
        form = self._Form(
            data={'persons': [self.alice.email]},
        )

        # linux is selected => only linux <option>
        html_form = "{}".format(form)
        option = '<option value="{}" {}>'.format(
            self.alice.email, 'selected')
        self.assertIn(option, html_form)

        self.assertNotIn(
            '<option value="{}">'.format(self.bob.email),
            html_form
        )

        # python is selected => only python <option>
        form = self._Form(
            data={'persons': [self.bob.email]},
        )
        html_form = "{}".format(form)
        option = '<option value="{}" {}>'.format(
            self.bob.email, 'selected')
        self.assertIn(option, html_form)
        self.assertNotIn(
            '<option value="{}">'.format(self.alice.email),
            html_form
        )

    def test_render_multiple(self):
        # both linux and python are selected => all <option>
        form = self._Form(
            data={'persons': [self.alice.email, self.bob.email]},
        )
        html_form = "{}".format(form)
        option = '<option value="{}" {}>'.format(
            self.alice.email, 'selected')
        self.assertIn(option, html_form)

        option = '<option value="{}" {}>'.format(
            self.bob.email, 'selected')
        self.assertIn(option, html_form)

    def test_render_same_key(self):
        # both linux and python are selected => all <option>
        form = self._Form(
            data={'persons': [self.alice.email, self.aliceinchains.email]},
        )
        html_form = "{}".format(form)
        option = '<option value="{}" {}>{}</option>'.format(
            self.aliceinchains.email, 'selected',
            self.aliceinchains
        )
        self.assertIn(option, html_form)

    def test_render_no_selection(self):
        # none is selected => no <option>
        form = self._Form(
            data={'persons': [self.invalid_pk]},
        )
        html_form = "{}".format(form)
        self.assertNotIn('<option', html_form)


@override_settings(HTTP_HOST='')
class FieldUrlProxyTest(LiveServerTestCase):

    def test_clean_method(self):
        person = AgnocompleteUrlProxyField(AutocompleteUrlSkipItem)
        search_url = person.agnocomplete.get_item_url('2')
        with mock.patch('demo.autocomplete.AutocompleteUrlSkipItem'
                        '.get_item_url') as mock_auto:
            mock_auto.return_value = self.live_server_url + search_url
            item = person.clean('2')

        self.assertEqual(item, '2')

    def test_clean_method_value_not_found(self):
        # Value is filter through the `item` method
        person = AgnocompleteUrlProxyField(AutocompleteUrlSkipItem)
        search_url = person.agnocomplete.get_item_url('1')
        with mock.patch('demo.autocomplete.AutocompleteUrlSkipItem'
                        '.get_item_url') as mock_auto:
            mock_auto.return_value = self.live_server_url + search_url
            self.assertRaises(ValidationError, person.clean, '1')
