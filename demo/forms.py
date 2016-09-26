"""
Form classes
"""
import pprint

from django import forms
from django.core.urlresolvers import reverse_lazy

from agnocomplete import fields, widgets
from agnocomplete.forms import UserContextFormMixin

from .autocomplete import (
    AutocompleteColor,
    AutocompleteColorExtra,
    AutocompleteColorShort,
    AutocompletePerson,
    AutocompletePersonExtra,
    AutocompletePersonShort,
    HiddenAutocomplete,
    AutocompleteTag,
    AutocompleteContextTag,
)
from .models import PersonTag, PersonContextTag
from .fields import ModelMultipleDomainField
from . import DATABASE


class SearchForm(forms.Form):
    search_color = fields.AgnocompleteField(AutocompleteColor)
    search_person = fields.AgnocompleteModelField(AutocompletePerson)


class SearchFormExtra(forms.Form):
    search_color = fields.AgnocompleteField(AutocompleteColorExtra)
    search_person = fields.AgnocompleteModelField(AutocompletePersonExtra)
    extra_argument = forms.CharField(required=False)


class SearchFormTextInput(forms.Form):
    """
    For some reasons, JQuery Autocomplete needs a TextInput instead of a basic
    select.
    """
    search_color = fields.AgnocompleteField(
        AutocompleteColor, widget=widgets.AgnocompleteTextInput)
    search_person = fields.AgnocompleteModelField(
        AutocompletePerson, widget=widgets.AgnocompleteTextInput)


class SearchContextForm(UserContextFormMixin, forms.Form):
    search_person = fields.AgnocompleteModelField('AutocompletePersonDomain')


class SearchCustom(forms.Form):
    search_color = fields.AgnocompleteField(
        HiddenAutocomplete(url=reverse_lazy('hidden-autocomplete')),
    )


class SearchColorMulti(forms.Form):
    search_multi_color = fields.AgnocompleteMultipleField(
        AutocompleteColorShort)
    search_multi_color_create = fields.AgnocompleteMultipleField(
        AutocompleteColorShort,
        create=True,
    )


class PersonTagForm(forms.Form):
    person = fields.AgnocompleteModelField(AutocompletePersonShort)
    tags = fields.AgnocompleteModelMultipleField(AutocompleteTag)


class PersonTagModelForm(forms.ModelForm):
    person = fields.AgnocompleteModelField(AutocompletePersonShort)
    tags = fields.AgnocompleteModelMultipleField(AutocompleteTag)

    class Meta:
        model = PersonTag
        fields = '__all__'


class PersonTagModelFormWithCreate(PersonTagModelForm):
    tags = fields.AgnocompleteModelMultipleField(
        AutocompleteTag,
        create_field="name",
        required=False
    )


class PersonContextTagModelForm(UserContextFormMixin, forms.ModelForm):
    person = fields.AgnocompleteModelField(AutocompletePersonShort)
    tags = ModelMultipleDomainField(
        AutocompleteContextTag,
        create_field="name",
        required=False
    )

    class Meta:
        model = PersonContextTag
        fields = '__all__'


class UrlProxyFormMixin(object):
    help_text = """
We're not using the usual fixture here. Here's our "database":
-------
<pre>
{}
</pre>
""".format(pprint.pformat(DATABASE))


class UrlProxyForm(UrlProxyFormMixin, forms.Form):
    person = fields.AgnocompleteField('AutocompleteUrlSimple')


class UrlProxyConvertForm(UrlProxyFormMixin, forms.Form):
    person_convert_simple = fields.AgnocompleteField(
        'AutocompleteUrlConvert',
        help_text='Simple returned data conversion')
    person_convert_complex = fields.AgnocompleteField(
        'AutocompleteUrlConvertComplex',
        help_text='Complex returned data conversion')


class UrlProxyAuthForm(UrlProxyFormMixin, forms.Form):
    person_query_auth = fields.AgnocompleteField(
        'AutocompleteUrlSimpleAuth',
        help_text='Query-arg based authentication')
    person_headers_auth = fields.AgnocompleteField(
        'AutocompleteUrlHeadersAuth',
        help_text='Headers-based authentication')
