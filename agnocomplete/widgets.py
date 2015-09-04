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
                # FIXME: the namespace should be a setting variable.
                'agnocomplete:agnocomplete', args=[self.agnocomplete_name])
        })
        return attrs


class AgnocompleteSelect(AgnocompleteWidgetMixin, widgets.Select):
    pass
