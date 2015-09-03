"""
The different autocomplete classes to be discovered
"""


class AutocompleteBase(object):
    def items(self):
        raise NotImplementedError(
            "Developer: Your class needs at least a items() method")


class AutocompleteChoices(AutocompleteBase):
    """
    Example::

        class AutocompleteColor(AutocompleteChoices):
            choices = ['red', 'green', 'blue']
    """
    choices = []

    def items(self):
        return zip(self.choices, self.choices)


class AutocompleteModel(AutocompleteBase):
    """

    Example::

        class AutocompletePeople(AutocompleteModel):
            model = People
            fields = ['first_name', 'last_name']
    """

    @property
    def model(self):
        raise NotImplementedError(
            "Integrator: You must have a `model` property")

    @property
    def fields(self):
        raise NotImplementedError(
            "Integrator: You must have a `fields` property")

    def get_queryset(self):
        return self.model.objects.all()

    def items(self):
        return self.get_queryset()
