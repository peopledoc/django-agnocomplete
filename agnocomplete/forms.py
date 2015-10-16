from django import forms

from .constants import AGNOCOMPLETE_USER_ATTRIBUTE


class UserContextForm(forms.Form):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserContextForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            setattr(field, AGNOCOMPLETE_USER_ATTRIBUTE, self.user)
