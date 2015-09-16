from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


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
