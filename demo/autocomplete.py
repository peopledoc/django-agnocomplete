"""
Autocomplete classes
"""
import logging
from django.urls import reverse_lazy
from django.utils.encoding import force_str as text
from django.conf import settings

from agnocomplete.exceptions import SkipItem
from agnocomplete.register import register
from agnocomplete.core import (
    AgnocompleteChoices,
    AgnocompleteModel,
    AgnocompleteUrlProxy,
)

from .models import Person, Tag, ContextTag
from .common import COLORS
from . import GOODAUTHTOKEN


logger = logging.getLogger(__name__)


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


class AutocompleteLastNameStartsWith(AgnocompleteModel):
    model = Person
    fields = ['^last_name']
    query_size_min = 1


class AutocompleteFirstNameEqualsIgnoreCase(AgnocompleteModel):
    model = Person
    fields = ['=first_name']
    query_size_min = 1


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
    def label(self, current_item):
        return u'{item} {mail}'.format(
            item=text(current_item), mail=current_item.email)


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


class AutocompletePersonDomainSpecial(AutocompletePersonDomain):
    """
    A special domain-related search

    We'll do silly things in the "selected" method.
    """
    def selected(self, ids):
        # Introducing a new variable here, to make sure the
        # "account_registrations" property is able to fetch the matricules.
        self._selected_queryset = self.get_queryset()
        return super(AutocompletePersonDomainSpecial, self).selected(ids)


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

    url_search_string = None

    def get_item_url(self, pk):
        return '{}{}'.format(
            getattr(settings, 'HTTP_HOST', ''),
            reverse_lazy('url-proxy:item', args=[pk]),
        )

    def get_search_url(self):
        return '{}{}'.format(
            getattr(settings, 'HTTP_HOST', ''),
            reverse_lazy(self.url_search_string),
        )


class AutocompleteUrlSimple(AutocompleteUrlMixin):
    url_search_string = 'url-proxy:simple'


class AutocompleteUrlConvert(AutocompleteUrlMixin):
    """
    Only value_key and label_key are redefined here
    """
    value_key = 'pk'
    label_key = 'name'
    url_search_string = 'url-proxy:convert'


class AutocompleteUrlConvertSchema(AutocompleteUrlMixin):
    """
    Return results embedded under the "result" key.
    """
    data_key = 'result'
    url_search_string = 'url-proxy:convert-schema'


class AutocompleteUrlConvertSchemaList(AutocompleteUrlMixin):
    """
    Return results as a list, not a dict
    """
    url_search_string = 'url-proxy:convert-schema-list'

    def get_http_result(self, payload):
        # Return the payload as is, it's a list.
        return payload


class AutocompleteUrlConvertComplex(AutocompleteUrlMixin):
    url_search_string = 'url-proxy:convert-complex'

    def item(self, current_item):
        return dict(
            value=text(current_item['pk']),
            label='{} {}'.format(
                current_item['first_name'], current_item['last_name']),
        )


class AutocompleteUrlSimpleAuth(AutocompleteUrlMixin):
    url_search_string = 'url-proxy:simple-auth'

    def get_http_call_kwargs(self, query):
        query_args = super(
            AutocompleteUrlSimpleAuth, self).get_http_call_kwargs(query)
        query_args['auth_token'] = GOODAUTHTOKEN
        return query_args


class AutocompleteUrlHeadersAuth(AutocompleteUrlMixin):
    url_search_string = 'url-proxy:headers-auth'

    def get_http_headers(self):
        return {'X-API-TOKEN': GOODAUTHTOKEN}


class AutocompleteUrlSimplePost(AutocompleteUrlMixin):
    method = 'post'
    url_search_string = 'url-proxy:simple-post'


class AutocompleteUrlErrors(AutocompleteUrlMixin):
    url_search_string = 'url-proxy:errors'
    query_size = 2
    query_size_min = 2


class AutocompleteUrlSimpleWithExtra(AutocompleteUrlSimple):
    query_size = 2
    query_size_min = 2

    def items(self, query=None, **kwargs):
        logger.debug("I am exploiting the kwargs [%s]", kwargs)
        if 'extra_argument' in kwargs and kwargs['extra_argument'] == 'moo':
            return [{'value': 'moo', 'label': 'moo'}]
        return super(AutocompleteUrlSimple, self).items(query, **kwargs)


class AutocompleteUrlSkipItem(AutocompleteUrlSimple):

    data_key = 'data'

    def item(self, obj):
        if obj['label'] == 'first person':
            raise SkipItem
        return super(AutocompleteUrlSkipItem, self).item(obj)

    def get_item_url(self, pk):
        return '{}{}'.format(
            getattr(settings, 'HTTP_HOST', ''),
            reverse_lazy('url-proxy:atomic-item', args=[pk])
        )


# Registration
register(AutocompleteColor)
register(AutocompleteColorExtra)
register(AutocompleteColorShort)
register(AutocompletePerson)
register(AutocompleteLastNameStartsWith)
register(AutocompleteFirstNameEqualsIgnoreCase)
register(AutocompletePersonExtra)
register(AutocompletePersonShort)
register(AutocompleteChoicesPages)
register(AutocompleteChoicesPagesOverride)
register(AutocompletePersonDomain)
register(AutocompletePersonDomainSpecial)
register(AutocompleteCustomUrl)
register(AutocompleteTag)
register(AutocompleteContextTag)
# URL-proxy autocompletion
register(AutocompleteUrlSimple)
register(AutocompleteUrlConvert)
register(AutocompleteUrlConvertComplex)
register(AutocompleteUrlConvertSchema)
register(AutocompleteUrlConvertSchemaList)
register(AutocompleteUrlSimpleAuth)
register(AutocompleteUrlHeadersAuth)
register(AutocompleteUrlSimplePost)
register(AutocompleteUrlErrors)
register(AutocompleteUrlSimpleWithExtra)
register(AutocompleteUrlSkipItem)
