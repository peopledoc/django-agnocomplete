"""
Agnocomplete Widgets
"""
from django.forms import widgets
from django.core.urlresolvers import reverse


class AgnocompleteWidgetMixin(object):
    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(AgnocompleteWidgetMixin, self).build_attrs(
            extra_attrs, **kwargs)
        attrs.update({
            'data-url': reverse(
                'autocomplete:autocomplete', args=[self.autocomplete_name])
        })
        return attrs


class AgnocompleteSelect(AgnocompleteWidgetMixin, widgets.Select):
    pass
