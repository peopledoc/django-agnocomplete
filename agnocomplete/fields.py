"""
Agnocomplete specific form fields.

"""
from django import forms

import six

from .core import AgnocompleteBase
from .constants import AGNOCOMPLETE_USER_ATTRIBUTE
from .widgets import AgnocompleteSelect, AgnocompleteMultiSelect
from .register import get_agnocomplete_registry
from .exceptions import ItemNotFound
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

    def _setup_agnocomplete_widget(self):
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
        if isinstance(klass_or_instance, six.string_types):
            registry = get_agnocomplete_registry()
            if klass_or_instance not in registry:
                raise UnregisteredAgnocompleteException(
                    "Unregistered Agnocomplete class: {} is unknown".format(klass_or_instance)  # noqa
                )
            klass_or_instance = registry[klass_or_instance]
        # If not an instance, instanciate this
        if not isinstance(klass_or_instance, AgnocompleteBase):
            klass_or_instance = klass_or_instance(user=user)
        # Pass the field when we have an AgnocompleteBase instance
        if isinstance(klass_or_instance, AgnocompleteBase):
            klass_or_instance.set_agnocomplete_field(self)
        # Store it in the instance
        self.agnocomplete = klass_or_instance
        self.agnocomplete.user = user

    def get_agnocomplete_context(self):
        """
        Return the agnocomplete user variable, if set.
        """
        return getattr(self, AGNOCOMPLETE_USER_ATTRIBUTE, None)

    def transmit_agnocomplete_context(self):
        """
        Assign the user context to the agnocomplete class, if any.
        """
        # Only if the field has this attribute set.
        if hasattr(self, AGNOCOMPLETE_USER_ATTRIBUTE):
            user = self.get_agnocomplete_context()
            if user:
                self.agnocomplete.user = user
            return user
        # if not, would implicitly return None.

    def clean(self, *args, **kwargs):
        """
        Potentially, these fields should validate against context-based
        queries.

        If a context variable has been transmitted to the field, it's being
        used to 'reset' the queryset and make sure the chosen item fits to
        the user context.
        """
        self.transmit_agnocomplete_context()
        return super(AgnocompleteMixin, self).clean(*args, **kwargs)


class AgnocompleteContextQuerysetMixin(object):
    def transmit_agnocomplete_context(self):
        """
        We'll reset the current queryset only if the user is set.
        """
        user = super(AgnocompleteContextQuerysetMixin, self) \
            .transmit_agnocomplete_context()
        if user:
            self.queryset = self.agnocomplete.get_queryset()
        return user


class AgnocompleteField(AgnocompleteMixin, forms.ChoiceField):
    """
    Agnocomplete Field class for simple Choice fields.
    """
    def __init__(self, agnocomplete, user=None, **kwargs):
        self.set_agnocomplete(agnocomplete, user)
        super(AgnocompleteField, self).__init__(
            choices=self.agnocomplete.get_choices(), **kwargs)
        self._setup_agnocomplete_widget()


class AgnocompleteModelField(AgnocompleteContextQuerysetMixin,
                             AgnocompleteMixin,
                             forms.ModelChoiceField):
    """
    Agnocomplete Field class for Choice fields based on models / querysets.
    """
    def __init__(self, agnocomplete, user=None, **kwargs):
        self.set_agnocomplete(agnocomplete, user)
        super(AgnocompleteModelField, self).__init__(
            self.agnocomplete.get_choices(), **kwargs)
        self._setup_agnocomplete_widget()


class AgnocompleteMultipleMixin(AgnocompleteMixin):
    """
    Core mixin for multiple-selection enabled fields
    """
    widget = AgnocompleteMultiSelect
    clean_empty = True

    def _setup_agnocomplete_widget(self):
        super(AgnocompleteMultipleMixin, self)._setup_agnocomplete_widget()
        # self.widget is a thing here
        self.widget.create = self.create

    def set_create_field(self, create=False, create_field=False):
        self.create_field = create_field
        self.create = bool(create_field) or create

    @property
    def empty_value(self):
        "Default empty value for this field."
        return []

    def to_python(self, value):
        # Pre-clean the list value
        value = self.clear_list_value(value)
        value = super(AgnocompleteMultipleMixin, self).to_python(value)
        # return the new cleaned value or the default empty_value
        return value or self.empty_value

    def clear_list_value(self, value):
        """
        Clean the argument value to eliminate None or Falsy values if needed.
        """
        # Don't go any further: this value is empty.
        if not value:
            return self.empty_value
        # Clean empty items if wanted
        if self.clean_empty:
            value = [v for v in value if v]
        return value or self.empty_value


class AgnocompleteMultipleField(AgnocompleteMultipleMixin,
                                forms.MultipleChoiceField):
    """
    Agnocomplete Field class for multiple Choice fields.
    """
    def __init__(self, agnocomplete, user=None,
                 create=False, create_field=False, **kwargs):
        self.set_agnocomplete(agnocomplete, user)
        self.set_create_field(create=create, create_field=create_field)
        super(AgnocompleteMultipleField, self).__init__(
            choices=self.agnocomplete.get_choices(), **kwargs)
        self._setup_agnocomplete_widget()


class AgnocompleteModelMultipleField(AgnocompleteContextQuerysetMixin,
                                     AgnocompleteMultipleMixin,
                                     forms.ModelMultipleChoiceField):
    """
    Field class for multiple selection on Django models.
    """
    def __init__(self, agnocomplete, user=None,
                 create=False, create_field=False, **kwargs):
        self.set_agnocomplete(agnocomplete, user)
        self.set_create_field(create=create, create_field=create_field)
        super(AgnocompleteModelMultipleField, self).__init__(
            self.agnocomplete.get_choices(), **kwargs)
        self._setup_agnocomplete_widget()
        self._new_values = []

    @property
    def empty_value(self):
        """
        Return default empty value as a Queryset.

        This value can be added via the `|` operator, so we surely need
        a queryset and not a list.
        """
        return self.queryset.model.objects.none()

    def create_item(self, **kwargs):
        """
        Return a model instance created from kwargs.
        """
        item, created = self.queryset.model.objects.get_or_create(**kwargs)
        return item

    def extra_create_kwargs(self):
        """
        Return extra arguments to create the new model instance.

        You can pass context-related arguments in the dictionary, or default
        values.
        """
        return {}

    def create_new_values(self):
        """
        Create values created by the user input. Return the model instances QS.
        """
        model = self.queryset.model
        pks = []
        extra_create_kwargs = self.extra_create_kwargs()
        for value in self._new_values:
            create_kwargs = {self.create_field: value}
            create_kwargs.update(extra_create_kwargs)
            new_item = self.create_item(**create_kwargs)
            pks.append(new_item.pk)
        return model.objects.filter(pk__in=pks)

    def clean(self, value):
        """
        Clean the field values.
        """
        if not self.create:
            # No new value can be created, use the regular clean field
            return super(AgnocompleteModelMultipleField, self).clean(value)

        # We have to do this here before the call to "super".
        # It'll be called again, but we can't find a way to "pre_clean" the
        # field value before pushing it into the parent class "clean()" method.
        value = self.clear_list_value(value)
        # Split the actual values with the potential new values
        # Numeric values will always be considered as PKs
        pks = [v for v in value if v.isdigit()]
        self._new_values = [v for v in value if not v.isdigit()]

        qs = super(AgnocompleteModelMultipleField, self).clean(pks)

        return qs


class AgnocompleteUrlProxyMixin(object):
    """
    This mixin can be used with a field which actually using
    :class:`agnocomplete.core.AutocompletUrlProxy`. The main purpose is to
    provide a mechanism to validate the value through the Autocomplete.
    """

    def valid_value(self, value):
        try:
            self.agnocomplete.validate(value)
        except ItemNotFound:
            return False

        return True
