"""
Form classes
"""
from django import forms
from agnocomplete import fields
from demo.autocomplete import AutocompleteColor, AutocompletePerson


class SearchForm(forms.Form):
    search_color = fields.AgnocompleteField(AutocompleteColor)
    search_person = fields.AgnocompleteModelField(AutocompletePerson)


class SearchContextForm(forms.Form):
    search_person = fields.AgnocompleteModelField('AutocompletePersonDomain')
