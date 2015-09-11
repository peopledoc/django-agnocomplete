"""
Agnocomplete Widgets
"""
from django.forms import widgets
from django.core.urlresolvers import reverse_lazy
from django.utils.encoding import force_text as text

from . import get_namespace

__all__ = ['AgnocompleteInput']


class AgnocompleteWidgetMixin(object):
    """
    Generic toolset for building Agnocomplete-ready widgets
    """
    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(AgnocompleteWidgetMixin, self).build_attrs(
            extra_attrs, **kwargs)
        data_url = reverse_lazy(
            '{}:agnocomplete'.format(get_namespace()),
            args=[self.agnocomplete.slug]
        )
        # Priority to the configurable URL
        data_url = self.agnocomplete.get_url() or data_url
        attrs.update({
            'data-url': data_url,
            'data-query-size': self.agnocomplete.get_query_size(),
        })
        return attrs

    def render_options(self, choices, selected_choices):
        selected_choices = set(text(v) for v in selected_choices)
        selected_choices_tuples = self.agnocomplete.selected(selected_choices)
        output = []
        for option_value, option_label in selected_choices_tuples:
            output.append(self.render_option(selected_choices, option_value, option_label))  # noqa
        return '\n'.join(output)


class AgnocompleteInput(AgnocompleteWidgetMixin, widgets.Select):
    pass
