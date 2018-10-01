"""
Demo-specific authentication backend.

**WARNING**: this is far from being secure, since you only need an email
address to authenticate. The only purpose of this backend is to run tests using
the user-context in the views.
"""
from .models import Person


class PersonBackend(object):
    """
    Authenticate against the Person model.
    """

    def authenticate(self, request=None, email=None):
        try:
            person = Person.objects.get(email=email)
        except Person.DoesNotExist:
            return None
        return person

    def get_user(self, person_id):
        try:
            return Person.objects.get(pk=person_id)
        except Person.DoesNotExist:
            return None
