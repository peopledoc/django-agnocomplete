"""
Form classes
"""
from django import forms
from django.core.urlresolvers import reverse_lazy

from agnocomplete import fields, widgets
from agnocomplete.forms import UserContextForm

from demo.autocomplete import (
    AutocompleteColor,
    AutocompleteColorShort,
    AutocompletePerson,
    HiddenAutocomplete
)


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
    search_color_create = fields.AgnocompleteField(
        AutocompleteColorShort,
        widget=widgets.AgnocompleteMultiSelect(create=True)
    )
    search_color_no_create = fields.AgnocompleteField(
        AutocompleteColorShort,
        widget=widgets.AgnocompleteMultiSelect
    )
