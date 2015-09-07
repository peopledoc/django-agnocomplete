"""
Agnocomplete specific form fields.

"""
from django import forms
from .core import AgnocompleteBase
from .widgets import AgnocompleteInput


__all__ = ['AgnocompleteField', 'AgnocompleteModelField']


class AgnocompleteMixin(object):
    """
    Handles the Agnocomplete generic handling for fields.
    """
    widget = AgnocompleteInput

    def __init__(self, klass_or_instance, *args, **kwargs):
        self.set_agnocomplete(klass_or_instance)
        super(AgnocompleteMixin, self).__init__(
            self.agnocomplete.get_choices(), *args, **kwargs)
        # Update the widget with the name of the target agnocomplete
        self.widget.agnocomplete_name = self.agnocomplete.__class__.__name__

    def set_agnocomplete(self, klass_or_instance):
        """
        Handling the assignation of the agnocomplete object inside the field.
        A developer may want to use a class or an instance of an
        :class:`AgnocompleteBase` class to configure her field.

        Ex::

            from agnocomplete import Fields

            class SearchForm(forms.Form):
                search_class = fields.AgnocompleteField(AgnocompleteColor)
                search_instance = fields.AgnocompleteField(
                    AgnocompleteColor(page_size=3))

            if it's a :class: being passed as a parameter, it'll be
            instantiated using the default parameters.

        """
        # If not an instance, instanciate this
        if not isinstance(klass_or_instance, AgnocompleteBase):
            klass_or_instance = klass_or_instance()
        # Store it in the instance
        self.agnocomplete = klass_or_instance


class AgnocompleteField(AgnocompleteMixin, forms.ChoiceField):
    """
    Agnocomplete Field class for simple Choice fields.
    """


class AgnocompleteModelField(AgnocompleteMixin, forms.ModelChoiceField):
    """
    Agnocomplete Field class for Choice fields based on models / querysets.
    """
