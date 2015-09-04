"""
Autocomplete classes
"""
from agnocomplete.register import register
from agnocomplete.core import AutocompleteChoices, AutocompleteModel
from demo.models import Person


class AutocompleteColor(AutocompleteChoices):
    choices = ['green', 'gray', 'blue', 'grey']


class AutocompleteChoicesPages(AutocompleteChoices):
    choices = ["choice{}".format(i) for i in range(200)]


class AutocompleteChoicesPagesOverride(AutocompleteChoicesPages):
    page_size = 30


class AutocompletePerson(AutocompleteModel):
    model = Person
    fields = ['first_name', 'last_name']


# Registration
register(AutocompleteColor)
register(AutocompletePerson)
register(AutocompleteChoicesPages)
register(AutocompleteChoicesPagesOverride)
