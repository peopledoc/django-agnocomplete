from django import forms
from .core import AutocompleteBase
from .widgets import AgnocompleteSelect


__all__ = ['AgnocompleteField', 'AgnocompleteModelField']


class AgnocompleteMixin(object):
    widget = AgnocompleteSelect

    def __init__(self, autocomplete, *args, **kwargs):
        self.set_autocomplete(autocomplete)
        super(AgnocompleteMixin, self).__init__(
            self.autocomplete.get_choices(), *args, **kwargs)
        # Update the widget with the name of the target autocomplete
        self.widget.autocomplete_name = self.autocomplete.__class__.__name__

    def set_autocomplete(self, autocomplete):
        # If not an instance, instanciate this
        if not isinstance(autocomplete, AutocompleteBase):
            autocomplete = autocomplete()
        # Keep it safe
        self.autocomplete = autocomplete


class AgnocompleteField(AgnocompleteMixin, forms.ChoiceField):
    pass


class AgnocompleteModelField(AgnocompleteMixin, forms.ModelChoiceField):
    pass
