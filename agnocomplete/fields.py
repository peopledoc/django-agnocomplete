"""
Agnocomplete specific form fields.

"""
from django import forms

from .core import AgnocompleteBase
from .constants import AGNOCOMPLETE_USER_ATTRIBUTE
from .widgets import AgnocompleteSelect, AgnocompleteMultiSelect
from .register import get_agnocomplete_registry
from .exceptions import UnregisteredAgnocompleteException


__all__ = [
    'AgnocompleteField',
    'AgnocompleteModelField',
    'AgnocompleteMultipleField',
    'AgnocompleteModelMultipleField',
]


class AgnocompleteMixin(object):
    """
    Handles the Agnocomplete generic handling for fields.
    """
    widget = AgnocompleteSelect

    def __init__(self, klass_or_instance, user=None, *args, **kwargs):
        self.set_agnocomplete(klass_or_instance, user)
        super(AgnocompleteMixin, self).__init__(
            self.agnocomplete.get_choices(), *args, **kwargs)
        # Update the widget with the target agnocomplete
        self.widget.agnocomplete = self.agnocomplete

    def set_agnocomplete(self, klass_or_instance, user):
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
            klass_or_instance = klass_or_instance(user=user)
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
    def clean(self, *args, **kwargs):
        """
        Potentially, these fields should validate against context-based
        queries.

        If a context variable has been transmitted to the field, it's being
        used to 'reset' the queryset and make sure the chosen item fits to
        the user context.
        """
        if hasattr(self, AGNOCOMPLETE_USER_ATTRIBUTE):
            user = getattr(self, AGNOCOMPLETE_USER_ATTRIBUTE, None)
            if user:
                self.agnocomplete.user = user
                self.queryset = self.agnocomplete.get_queryset()
        return super(AgnocompleteModelField, self).clean(*args, **kwargs)


class AgnocompleteMultipleMixin(AgnocompleteMixin):
    """
    Core mixin for multiple-selection enabled fields
    """
    widget = AgnocompleteMultiSelect
    clean_empty = True

    def __init__(self, *args, **kwargs):
        create_arg = kwargs.pop('create', False)
        self.create_field = kwargs.pop('create_field', False)
        self.create = bool(self.create_field) or create_arg
        super(AgnocompleteMultipleMixin, self).__init__(*args, **kwargs)
        # self.widget is a thing here
        self.widget.create = self.create
        self._new_values = []

    @property
    def empty_value(self):
        return []

    def pre_clean(self, value):
        """
        Clean the argument value to eliminate None or Falsy values if needed.
        """
        # Don't go any further: this value is empty.
        if not value:
            return self.empty_value
        # Clean empty items if wanted
        if self.clean_empty:
            value = [v for v in value if v]
        # return the new cleaned value or the default empty_value
        return value or self.empty_value

    def clean(self, value, pre_clean=True):
        if pre_clean:
            # Transform value to drop empty values
            value = self.pre_clean(value)
        return super(AgnocompleteMultipleMixin, self).clean(value)


class AgnocompleteMultipleField(AgnocompleteMultipleMixin,
                                forms.MultipleChoiceField):
    """
    Agnocomplete Field class for multiple Choice fields.
    """


class AgnocompleteModelMultipleField(AgnocompleteMultipleMixin,
                                     forms.ModelMultipleChoiceField):
    """
    Field class for multiple selection on Django models.
    """

    @property
    def empty_value(self):
        return self.queryset.model.objects.none()

    def create_new_values(self):
        model = self.queryset.model
        pks = []
        for value in self._new_values:
            new_item = model.objects.create(**{self.create_field: value})
            pks.append(new_item.pk)
        return model.objects.filter(pk__in=pks)

    def clean(self, value):
        if not self.create:
            # No new value can be created, use the regular clean field
            return super(AgnocompleteModelMultipleField, self).clean(value)

        value = self.pre_clean(value)
        # Split the actual values with the potential new values
        # Numeric values will always be considered as PKs
        pks = [v for v in value if v.isdigit()]
        self._new_values = [v for v in value if not v.isdigit()]

        qs = super(AgnocompleteModelMultipleField, self).clean(
            pks, pre_clean=False)

        return qs
