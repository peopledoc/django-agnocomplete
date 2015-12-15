"""
Form classes
"""
from django import forms
from django.core.urlresolvers import reverse_lazy

from agnocomplete import fields, widgets
from agnocomplete.forms import UserContextForm

from .autocomplete import (
    AutocompleteColor,
    AutocompleteColorShort,
    AutocompletePerson,
    AutocompletePersonShort,
    HiddenAutocomplete
)
from .models import Friendship


class SearchForm(forms.Form):
    search_color = fields.AgnocompleteField(AutocompleteColor)
    search_person = fields.AgnocompleteModelField(AutocompletePerson)


class SearchFormTextInput(forms.Form):
    """
    For some reasons, JQuery Autocomplete needs a TextInput instead of a basic
    select.
    """
    search_color = fields.AgnocompleteField(
        AutocompleteColor, widget=widgets.AgnocompleteTextInput)
    search_person = fields.AgnocompleteModelField(
        AutocompletePerson, widget=widgets.AgnocompleteTextInput)


class SearchContextForm(UserContextForm):
    search_person = fields.AgnocompleteModelField('AutocompletePersonDomain')


class SearchCustom(forms.Form):
    search_color = fields.AgnocompleteField(
        HiddenAutocomplete(url=reverse_lazy('hidden-autocomplete')),
    )


class SearchColorMulti(forms.Form):
    search_multi_color = fields.AgnocompleteMultipleField(
        AutocompleteColorShort)
    search_multi_color_create = fields.AgnocompleteMultipleField(
        AutocompleteColorShort,
        create=True,
    )


class FriendshipForm(forms.Form):
    person = fields.AgnocompleteModelField(AutocompletePersonShort)
    friends = fields.AgnocompleteModelMultipleField(AutocompletePersonShort)


class FriendshipModelForm(forms.ModelForm):
    person = fields.AgnocompleteModelField(AutocompletePersonShort)
    friends = fields.AgnocompleteModelMultipleField(AutocompletePersonShort)

    class Meta:
        model = Friendship
        fields = '__all__'
