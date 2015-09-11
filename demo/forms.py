"""
Form classes
"""
from django import forms
from django.core.urlresolvers import reverse_lazy

from agnocomplete import fields

from demo.autocomplete import AutocompleteColor, AutocompletePerson
from demo.autocomplete import HiddenAutocomplete


class SearchForm(forms.Form):
    search_color = fields.AgnocompleteField(AutocompleteColor)
    search_person = fields.AgnocompleteModelField(AutocompletePerson)


class SearchContextForm(forms.Form):
    search_person = fields.AgnocompleteModelField('AutocompletePersonDomain')


class SearchCustom(forms.Form):
    search_color = fields.AgnocompleteField(
        HiddenAutocomplete(url=reverse_lazy('hidden-autocomplete')),
    )
