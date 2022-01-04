"""
Agnocomplete Widgets
"""
from django.forms import widgets
from django.urls import reverse_lazy
from django.utils.encoding import force_str as text
from django.conf import settings


from . import get_namespace
from .constants import AGNOCOMPLETE_DATA_ATTRIBUTE

__all__ = [
    'AgnocompleteSelect',
    'AgnocompleteTextInput',
    'AgnocompleteMultiSelect'
]


class AgnocompleteWidgetMixin(object):
    def _agnocomplete_build_attrs(self, attrs):
        data_url = reverse_lazy(
            '{}:agnocomplete'.format(get_namespace()),
            args=[self.agnocomplete.slug]
        )
        # Priority to the configurable URL
        data_url = self.agnocomplete.get_url() or data_url
        # Data attribute
        data_attribute = getattr(
            settings, 'AGNOCOMPLETE_DATA_ATTRIBUTE',
            AGNOCOMPLETE_DATA_ATTRIBUTE)
        data_attribute = 'data-{}'.format(data_attribute)
        attrs.update({
            'data-url': data_url,
            'data-query-size': self.agnocomplete.get_query_size(),
            data_attribute: 'on',
        })

        return attrs

    """
    Generic toolset for building Agnocomplete-ready widgets
    """
    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super(AgnocompleteWidgetMixin, self).build_attrs(
            base_attrs, extra_attrs)
        return self._agnocomplete_build_attrs(attrs)

    """
    Render only selected options
    """
    def optgroups(self, name, value, attrs=None):
        selected_ids = set(text(v) for v in value)
        selected_choices = self.agnocomplete.selected(selected_ids)
        options = []
        groups = [
            (None, options, 0)  # single unnamed group
        ]

        for option_value, option_label in selected_choices:
            opt = self.create_option(
                name, option_value, option_label, True, 0,
                subindex=None, attrs=attrs,
            )
            opt['attrs']['selected'] = True
            options.append(opt)

        return groups


class AgnocompleteSelect(AgnocompleteWidgetMixin, widgets.Select):
    """
    The default Agnocomplete-ready input is a Select box.
    """
    pass


class AgnocompleteTextInput(AgnocompleteWidgetMixin, widgets.TextInput):
    """
    Alternate Agnocomplete-ready widget: TextInput.

    This widget is needed for front librairies which want a text input.
    """
    pass


class AgnocompleteMultiSelect(AgnocompleteWidgetMixin, widgets.SelectMultiple):
    """
    A multi-selection-ready Select widget Mixin
    """
    def __init__(self, create=False, *args, **kwargs):
        super(AgnocompleteMultiSelect, self).__init__(*args, **kwargs)
        self.create = create

    def _agnocomplete_build_attrs(self, attrs):
        attrs = super(AgnocompleteMultiSelect, self). \
            _agnocomplete_build_attrs(attrs)

        if self.create:
            attrs.update({'data-create': 'on'})

        return attrs
