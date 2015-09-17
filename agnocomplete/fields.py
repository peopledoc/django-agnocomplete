"""
Agnocomplete specific form fields.

"""
from django import forms

from .core import AgnocompleteBase
from .widgets import AgnocompleteSelect
from .register import get_agnocomplete_registry
from .exceptions import UnregisteredAgnocompleteException


__all__ = ['AgnocompleteField', 'AgnocompleteModelField']


class AgnocompleteMixin(object):
    """
    Handles the Agnocomplete generic handling for fields.
    """
    widget = AgnocompleteSelect

    def __init__(self, klass_or_instance, *args, **kwargs):
        self.set_agnocomplete(klass_or_instance)
        super(AgnocompleteMixin, self).__init__(
            self.agnocomplete.get_choices(), *args, **kwargs)
        # Update the widget with the target agnocomplete
        self.widget.agnocomplete = self.agnocomplete

    def set_agnocomplete(self, klass_or_instance):
        """
        Handling the assignation of the agnocomplete object inside the field.
        A developer may want to use a class or an instance of an
        :class:`AgnocompleteBase` class to configure her field.

        Ex::

            from agnocomplete import Fields

            class SearchForm(forms.Form):
                search_class = fields.AgnocompleteField(AgnocompleteColor)
                search_class2 = fields.AgnocompleteField('AgnocompleteColor')
                search_instance = fields.AgnocompleteField(
                    AgnocompleteColor(page_size=3))

            if it's a :class: being passed as a parameter, it'll be
            instantiated using the default parameters. If it's a string, it'll
            be instanciated also, using the name of the class as the key to
            fetch the actual class.

        """
        # If string, use register to fetch the class
        if isinstance(klass_or_instance, str):
            registry = get_agnocomplete_registry()
            if klass_or_instance not in registry:
                raise UnregisteredAgnocompleteException(
                    "Unregistered Agnocomplete class: {} is unknown".format(klass_or_instance)  # noqa
                )
            klass_or_instance = registry[klass_or_instance]
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
