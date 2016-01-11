from django.test import TestCase
from django.core.urlresolvers import reverse
try:
    from django.test import override_settings
except ImportError:
    # Django 1.6
    from django.test.utils import override_settings

from agnocomplete import get_namespace
from agnocomplete.views import AgnocompleteJSONView
from ..models import Person, PersonTag, Tag


class HomeTest(TestCase):

    def test_widgets(self):
        # This test will validate the widget/field building
        # for all Agnocomplete-ready fields.
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIn('search_color', form.fields)
        self.assertIn('search_person', form.fields)
        search_color = form.fields['search_color']
        attrs_color = search_color.widget.build_attrs()
        self.assertIn('data-url', attrs_color)
        self.assertIn('data-query-size', attrs_color)
        self.assertIn('data-agnocomplete', attrs_color)
        # Not a multi
        self.assertFalse(search_color.widget.allow_multiple_selected)

    @override_settings(AGNOCOMPLETE_DATA_ATTRIBUTE='wow')
    def test_data_attribute(self):
        response = self.client.get(reverse('home'))
        form = response.context['form']
        search_color = form.fields['search_color']
        attrs_color = search_color.widget.build_attrs()
        self.assertIn('data-url', attrs_color)
        self.assertIn('data-query-size', attrs_color)
        self.assertIn('data-wow', attrs_color)

    def test_get(self):
        response = self.client.get(reverse('home'))
        form = response.context['form']
        # Color
        search_color = form.fields['search_color']
        attrs_color = search_color.widget.build_attrs()
        url_color = attrs_color['data-url']
        self.assertEqual(
            url_color,
            reverse(
                get_namespace() + ':agnocomplete',
                args=['AutocompleteColor']
            )
        )
        # Person
        search_person = form.fields['search_person']
        attrs_person = search_person.widget.build_attrs()
        url_person = attrs_person['data-url']
        self.assertEqual(
            url_person,
            reverse(
                get_namespace() + ':agnocomplete',
                args=['AutocompletePerson']
            )
        )

    def test_queries(self):
        # This view should not trigger any SQL query
        # It has no selected value
        with self.assertNumQueries(0):
            self.client.get(reverse('home'))


class FilledFormTest(TestCase):

    def setUp(self):
        super(FilledFormTest, self).setUp()
        self.alice1 = Person.objects.get(pk=1)

    def test_queries(self):
        # This view should just trigger TWO queries
        # It has ONE selected value
        # 1. The first one is to fetch the selected value and check if it's
        #    valid the query is a Model.objects.get(pk=pk)
        # 2. The other is the query that fetches the selected values and feed
        #    the rendered input
        with self.assertNumQueries(2):
            self.client.get(reverse('filled-form'))

    def test_selected(self):
        response = self.client.get(reverse('filled-form'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.is_valid())
        cleaned_data = form.cleaned_data
        self.assertEqual(
            cleaned_data, {
                "search_color": "grey",
                "search_person": self.alice1
            }
        )


class CustomSearchTest(TestCase):

    def test_widgets(self):
        response = self.client.get(reverse('search-custom'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIn('search_color', form.fields)
        search_color = form.fields['search_color']
        attrs_color = search_color.widget.build_attrs()
        self.assertIn('data-url', attrs_color)
        self.assertEqual(
            attrs_color['data-url'],
            reverse('hidden-autocomplete')
        )


class MultiSearchTest(TestCase):

    def test_widgets_multi_create(self):
        response = self.client.get(reverse('selectize-multi'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIn('search_multi_color_create', form.fields)
        search_color = form.fields['search_multi_color_create']
        # Specific: this is a multi
        self.assertTrue(search_color.widget.allow_multiple_selected)
        # But it's also a "create-enabled"
        attrs_color = search_color.widget.build_attrs()
        self.assertIn('data-create', attrs_color)
        self.assertTrue(attrs_color['data-create'])

    def test_widgets_multi_no_create(self):
        response = self.client.get(reverse('selectize-multi'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIn('search_multi_color', form.fields)
        search_color = form.fields['search_multi_color']
        # Specific: this is a multi
        self.assertTrue(search_color.widget.allow_multiple_selected)
        # But it's not "create-enabled"
        attrs_color = search_color.widget.build_attrs()
        self.assertNotIn('data-create', attrs_color)

    def test_tag_multi(self):
        response = self.client.get(reverse('selectize-tag'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIn('person', form.fields)
        self.assertIn('tags', form.fields)

    def test_tag_multi_modelforms(self):
        response = self.client.get(reverse('selectize-model-tag'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIn('person', form.fields)
        self.assertIn('tags', form.fields)

    def test_tag_multi_with_create_modelforms(self):
        response = self.client.get(reverse('selectize-model-tag-with-create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIn('person', form.fields)
        self.assertIn('tags', form.fields)


class ABCTestView(TestCase):

    def test_AgnocompleteJSONView(self):

        class WickedAgnocompleteJSONView(AgnocompleteJSONView):
            pass

        with self.assertRaises(TypeError) as e:
            WickedAgnocompleteJSONView()
        exception = e.exception.args[0]
        self.assertEqual(
            exception,
            """Can't instantiate abstract class WickedAgnocompleteJSONView\
 with abstract methods get_dataset""")


class JSDemoViews(TestCase):

    def test_selectize(self):
        response = self.client.get(reverse('selectize'))
        self.assertEqual(response.status_code, 200)

    def test_selectize_multi(self):
        response = self.client.get(reverse('selectize-multi'))
        self.assertEqual(response.status_code, 200)

    def test_select2(self):
        response = self.client.get(reverse('select2'))
        self.assertEqual(response.status_code, 200)

    def test_jquery_autocomplete(self):
        response = self.client.get(reverse('jquery-autocomplete'))
        self.assertEqual(response.status_code, 200)

    def test_typeahead(self):
        response = self.client.get(reverse('typeahead'))
        self.assertEqual(response.status_code, 200)

    def test_context_search(self):
        response = self.client.get(reverse('search-context'))
        self.assertEqual(response.status_code, 200)


class FormValidationViewTest(TestCase):

    def setUp(self):
        super(FormValidationViewTest, self).setUp()
        self.alice = Person.objects.get(pk=1)
        self.bob = Person.objects.get(email__endswith='demo.com')
        self.client.login(email=self.alice.email)

    def test_post_valid(self):
        response = self.client.post(
            reverse('search-context'),
            data={'search_person': self.alice.pk}
        )
        self.assertEqual(response.status_code, 200)

    def test_post_invalid(self):
        response = self.client.post(
            reverse('search-context'),
            data={'search_person': self.bob.pk}
        )
        self.assertNotEqual(response.status_code, 200)


class MultipleModelSelectGeneric(TestCase):

    def setUp(self):
        super(MultipleModelSelectGeneric, self).setUp()
        self.alice = Person.objects.get(pk=1)
        self.other_person = Person.objects.exclude(pk=self.alice.pk)\
            .order_by('?').first()
        self.random = Tag.objects.first()
        self.random2 = Tag.objects.exclude(pk=self.random.pk).first()


class MultipleModelSelectTest(MultipleModelSelectGeneric):

    def test_no_tag_empty_string(self):
        # Empty string is an error: required field
        count = PersonTag.objects.count()
        response = self.client.post(
            reverse('selectize-model-tag'),
            data={
                u'person': self.alice.pk,
                u'tags': '',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(PersonTag.objects.count(), count)

    def test_no_tag_empty_list(self):
        # Empty list is an error: required field
        count = PersonTag.objects.count()
        response = self.client.post(
            reverse('selectize-model-tag'),
            data={
                u'person': self.alice.pk,
                u'tags': [],
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(PersonTag.objects.count(), count)

    def test_tag_create(self):
        count = PersonTag.objects.count()
        response = self.client.post(
            reverse('selectize-model-tag'),
            data={
                u'person': self.alice.pk,
                u'tags': [self.random.pk, self.random2.pk],
            }
        )
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(PersonTag.objects.count(), count + 1)
        new_person_tag = PersonTag.objects.order_by('pk').last()
        self.assertEqual(new_person_tag.tags.count(), 2)

    def test_tag_edit(self):
        count = PersonTag.objects.count()
        person_tag = PersonTag.objects.first()

        # Checks on this tags
        all_tags = set([p.pk for p in Tag.objects.all()])
        tags = set([t.pk for t in person_tag.tags.all()])
        self.assertNotEqual(all_tags, tags)
        self.assertEqual(self.alice, person_tag.person)

        # Check the edit page as a GET
        response = self.client.get(
            reverse('selectize-model-tag-edit', args=[person_tag.pk]),
        )
        self.assertEqual(response.status_code, 200)

        # It's fine, let's edit it now
        response = self.client.post(
            reverse('selectize-model-tag-edit', args=[person_tag.pk]),
            data={
                u'person': self.other_person.pk,
                u'tags': list(all_tags),
            }
        )
        self.assertRedirects(response, reverse('home'))
        # No new PersonTag
        self.assertEqual(PersonTag.objects.count(), count)
        # Reload
        person_tag = PersonTag.objects.get(pk=person_tag.pk)
        # Check that the object has been modified
        tags = set([t.pk for t in person_tag.tags.all()])
        self.assertEqual(all_tags, tags)
        self.assertEqual(self.other_person, person_tag.person)


class MultipleModelSelectWithCreateTest(MultipleModelSelectGeneric):

    def test_no_tag_empty_string(self):
        # Empty string means empty tag list, no error
        count = PersonTag.objects.count()
        response = self.client.post(
            reverse('selectize-model-tag-with-create'),
            data={
                u'person': self.alice.pk,
                u'tags': '',
            }
        )
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(PersonTag.objects.count(), count + 1)
        new_person_tag = PersonTag.objects.order_by('pk').last()
        self.assertEqual(new_person_tag.tags.count(), 0)

    def test_no_tag_empty_list(self):
        # Empty list is means empty tag list, no error
        count = PersonTag.objects.count()
        response = self.client.post(
            reverse('selectize-model-tag-with-create'),
            data={
                u'person': self.alice.pk,
                u'tags': [],
            }
        )
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(PersonTag.objects.count(), count + 1)
        new_person_tag = PersonTag.objects.order_by('pk').last()
        self.assertEqual(new_person_tag.tags.count(), 0)

    def test_tag_with_create(self):
        count = PersonTag.objects.count()
        count_tag = Tag.objects.count()
        response = self.client.get(reverse('selectize-model-tag-with-create'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse('selectize-model-tag-with-create'),
            data={
                u'person': self.alice.pk,
                u'tags': [
                    self.random.pk,
                    self.random2.pk,
                    'newtag1',
                    'newtag2',
                ],
            }
        )
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(PersonTag.objects.count(), count + 1)
        # Two tags added to the tag table
        self.assertEqual(Tag.objects.count(), count_tag + 2)
        new_person_tag = PersonTag.objects.order_by('pk').last()
        self.assertEqual(new_person_tag.tags.count(), 4)
