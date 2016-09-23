"""
Autocomplete classes
"""
from django.core.urlresolvers import reverse_lazy
from django.utils.encoding import force_text as text
from django.conf import settings

from agnocomplete.register import register
from agnocomplete.core import (
    AgnocompleteChoices,
    AgnocompleteModel,
    AgnocompleteUrlProxy,
)
from .models import Person, Tag, ContextTag
from .common import COLORS
from . import GOODAUTHTOKEN


class AutocompleteColor(AgnocompleteChoices):
    choices = COLORS


class AutocompleteColorExtra(AutocompleteColor):
    def items(self, query, **kwargs):
        extra_argument = kwargs.get('extra_argument', None)
        result = super(AutocompleteColorExtra, self).items(query, **kwargs)
        # This is a very dummy usage of the extra argument
        if extra_argument:
            result.append({'value': 'EXTRA', 'label': 'EXTRA'})
        return result


class AutocompleteColorShort(AutocompleteColor):
    query_size = 2
    query_size_min = 2


class AutocompleteCustomUrl(AutocompleteColor):
    slug = 'my-autocomplete'


class AutocompleteChoicesPages(AgnocompleteChoices):
    choices = [
        ("choice{}".format(i), "choice{}".format(i)) for i in range(200)
    ]


class AutocompleteChoicesPagesOverride(AutocompleteChoicesPages):
    page_size = 30
    query_size = 6
    query_size_min = 5


class AutocompletePerson(AgnocompleteModel):
    model = Person
    fields = ['first_name', 'last_name']
    query_size_min = 2


class AutocompletePersonExtra(AutocompletePerson):

    def build_extra_filtered_queryset(self, queryset, **kwargs):
        # Filtering on location if provided
        location = kwargs.get('extra_argument', None)
        if location:
            queryset = queryset.filter(location__iexact=location)
        return queryset


class AutocompletePersonShort(AutocompletePerson):
    query_size = 2


class AutocompletePersonLabel(AutocompletePerson):
    def item(self, current_item):
        label = {
            'value': text(current_item.pk),
            'label': u'{item} {mail}'.format(
                item=text(current_item), mail=current_item.email)
        }

        return label


# Special: not integrated into the registry (yet)
class AutocompletePersonQueryset(AgnocompleteModel):
    fields = ['first_name', 'last_name']
    requires_authentication = False

    def get_queryset(self):
        return Person.objects.filter(email__contains='example.com')


# Special: not integrated into the registry (yet)
class AutocompletePersonMisconfigured(AgnocompleteModel):
    fields = ['first_name', 'last_name']


class AutocompletePersonDomain(AgnocompleteModel):
    fields = ['first_name', 'last_name']
    model = Person
    requires_authentication = True
    query_size_min = 2

    def get_queryset(self):
        email = self.user.email
        _, domain = email.split('@')
        return Person.objects.filter(email__endswith=domain)


# Do not register this, it's for custom view demo
class HiddenAutocomplete(AutocompleteColor):
    query_size_min = 2


# Do not register this, it's for custom view demo
class HiddenAutocompleteURL(AutocompleteColor):
    query_size_min = 2
    url = '/stuff'


# Do not register this, it's for custom view demo
class HiddenAutocompleteURLReverse(AutocompleteColor):
    query_size_min = 2
    url = reverse_lazy('hidden-autocomplete')


class AutocompleteTag(AgnocompleteModel):
    model = Tag
    fields = ['name']
    query_size_min = 2
    query_size = 2


class AutocompleteContextTag(AgnocompleteModel):
    model = ContextTag
    fields = ['name']
    query_size_min = 2
    query_size = 2
    requires_authentication = True

    def get_queryset(self):
        email = self.user.email
        _, domain = email.split('@')
        return ContextTag.objects.filter(domain__contains=domain)


# Toolbox
class AutocompleteUrlMixin(AgnocompleteUrlProxy):
    def get_item_url(self, pk):
        return '{}{}'.format(
            getattr(settings, 'HTTP_HOST', ''),
            reverse_lazy('url-proxy:item', args=[pk]),
        )


class AutocompleteUrlSimple(AutocompleteUrlMixin):

    def get_search_url(self):
        return '{}{}?{}'.format(
            getattr(settings, 'HTTP_HOST', ''),
            reverse_lazy('url-proxy:simple'),
            r'q={q}'
        )


class AutocompleteUrlConvert(AutocompleteUrlMixin):
    """
    Only value_key and label_key are redefined here
    """
    value_key = 'pk'
    label_key = 'name'

    def get_search_url(self):
        return '{}{}?{}'.format(
            getattr(settings, 'HTTP_HOST', ''),
            reverse_lazy('url-proxy:convert'),
            r'q={q}'
        )


class AutocompleteUrlConvertComplex(AgnocompleteUrlProxy):
    def get_search_url(self):
        return '{}{}?{}'.format(
            getattr(settings, 'HTTP_HOST', ''),
            reverse_lazy('url-proxy:convert-complex'),
            r'q={q}'
        )

    def item(self, current_item):
        return dict(
            value=text(current_item['pk']),
            label='{} {}'.format(
                current_item['first_name'], current_item['last_name']),
        )


class AutocompleteUrlSimpleAuth(AutocompleteUrlMixin):
    def get_search_url(self):
        return '{}{}?{}'.format(
            getattr(settings, 'HTTP_HOST', ''),
            reverse_lazy('url-proxy:simple-auth'),
            r'q={q}&auth_token={auth_token}'
        )

    def get_http_call_kwargs(self, query):
        query_args = super(
            AutocompleteUrlSimpleAuth, self).get_http_call_kwargs(query)
        query_args['auth_token'] = GOODAUTHTOKEN
        return query_args


class AutocompleteUrlHeadersAuth(AutocompleteUrlMixin):
    def get_search_url(self):
        return '{}{}?{}'.format(
            getattr(settings, 'HTTP_HOST', ''),
            reverse_lazy('url-proxy:headers-auth'),
            r'q={q}'
        )

    def get_http_headers(self):
        return {'X-API-TOKEN': GOODAUTHTOKEN}


# Registration
register(AutocompleteColor)
register(AutocompleteColorExtra)
register(AutocompleteColorShort)
register(AutocompletePerson)
register(AutocompletePersonExtra)
register(AutocompletePersonShort)
register(AutocompleteChoicesPages)
register(AutocompleteChoicesPagesOverride)
register(AutocompletePersonDomain)
register(AutocompleteCustomUrl)
register(AutocompleteTag)
register(AutocompleteContextTag)
# URL-proxy autocompletion
register(AutocompleteUrlSimple)
register(AutocompleteUrlConvert)
register(AutocompleteUrlConvertComplex)
register(AutocompleteUrlSimpleAuth)
register(AutocompleteUrlHeadersAuth)
