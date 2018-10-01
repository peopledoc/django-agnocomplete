from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ..admin import FavoriteColorModelForm


class AdminTest(TestCase):

    def setUp(self):
        super(AdminTest, self).setUp()
        # create a superuser to be logged in
        self.admin = User.objects.create_superuser(
            'admin', 'admin@example.com', 'abcd1234')
        self.client.login(username='admin', password='abcd1234')

    def test_home(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

    def test_demo_person(self):
        response = self.client.get(reverse('admin:demo_person_changelist'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('admin:demo_person_add'))
        self.assertEqual(response.status_code, 200)

    def test_demo_color(self):
        response = self.client.get(
            reverse('admin:demo_favoritecolor_changelist'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('admin:demo_favoritecolor_add'))
        self.assertEqual(response.status_code, 200)

    def test_demo_color_form(self):
        response = self.client.get(reverse('admin:demo_favoritecolor_add'))
        self.assertIn('adminform', response.context)
        adminform = response.context['adminform']
        form = adminform.form
        self.assertTrue(isinstance(form, FavoriteColorModelForm))
        self.assertIn('media', response.context)
        media = response.context['media']
        media = "{}".format(media)
        self.assertIn('selectize.js', media)
        self.assertIn('selectize.css', media)
