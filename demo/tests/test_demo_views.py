from django.test import TestCase
from django.core.urlresolvers import reverse


class IndexTest(TestCase):

    def test_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIn('search_color', form.fields)
        self.assertIn('search_person', form.fields)
        # Color
        search_color = form.fields['search_color']
        attrs_color = search_color.widget.build_attrs()
        self.assertIn('data-url', attrs_color)
        url_color = attrs_color['data-url']
        self.assertEqual(
            url_color,
            reverse('agnocomplete:agnocomplete', args=['AutocompleteColor']))
        # Person
        search_person = form.fields['search_person']
        attrs_person = search_person.widget.build_attrs()
        self.assertIn('data-url', attrs_person)
        url_person = attrs_person['data-url']
        self.assertEqual(
            url_person,
            reverse('agnocomplete:agnocomplete', args=['AutocompletePerson']))

    def test_queries(self):
        # This view should not trigger any SQL query
        # It has no selected value
        with self.assertNumQueries(0):
            self.client.get(reverse('home'))
