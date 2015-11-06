from django.test import TestCase

from ..forms import SearchContextForm
from ..models import Person


class TestSearchContext(TestCase):

    def setUp(self):
        super(TestSearchContext, self).setUp()
        self.alice = Person.objects.get(pk=1)
        self.bob = Person.objects.get(pk=3)
        self.invalid_pk = Person.objects.order_by('pk').last().pk + 1

    def test_valid_no_user(self):
        form = SearchContextForm(
            user=None,
            data={'search_person': self.alice.pk},
        )
        self.assertTrue(form.is_valid())

    def test_valid_user(self):
        form = SearchContextForm(
            user=self.alice,
            data={'search_person': self.alice.pk},
        )
        self.assertTrue(form.is_valid())

    def test_invalid_pk(self):
        form = SearchContextForm(
            user=None,
            data={'search_person': self.invalid_pk},
        )
        self.assertFalse(form.is_valid())

    def test_invalid_user(self):
        form = SearchContextForm(
            user=self.alice,
            data={'search_person': self.bob.pk},
        )
        self.assertFalse(form.is_valid())
