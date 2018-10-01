"""
Agnocomplete Widgets
"""
from distutils.version import StrictVersion

from django import get_version

from django.forms import widgets
from django.urls import reverse_lazy
from django.utils.encoding import force_text as text
from django.conf import settings


from . import get_namespace
from .constants import AGNOCOMPLETE_DATA_ATTRIBUTE

__all__ = [
    'AgnocompleteSelect',
    'AgnocompleteTextInput',
    'AgnocompleteMultiSelect'
]


class _AgnocompleteWidgetMixin(object):
    """
    Generic toolset for building Agnocomplete-ready widgets
    """
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


if StrictVersion(get_version()) < StrictVersion('1.11'):
    class AgnocompleteWidgetMixin(_AgnocompleteWidgetMixin):
        """
        Generic toolset for building Agnocomplete-ready widgets
        """
        def build_attrs(self, extra_attrs=None, **kwargs):
            attrs = super(AgnocompleteWidgetMixin, self).build_attrs(
                extra_attrs, **kwargs)
            return self._agnocomplete_build_attrs(attrs)

        def render_options(self, *args):
            # Django >= 1.10, only "selected_choices" in the arg list
            if len(args) == 1:
                selected_choices = args[0]
            else:
                # Django < 1.10 - selected_choices is the second arg.
                _, selected_choices = args
            selected_choices = set(text(v) for v in selected_choices)
            selected_choices_tuples = self.agnocomplete.selected(
                selected_choices)
            output = []
            for option_value, option_label in selected_choices_tuples:
                output.append(self.render_option(
                    selected_choices, option_value, option_label))
            return '\n'.join(output)
else:
    class AgnocompleteWidgetMixin(_AgnocompleteWidgetMixin):
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
