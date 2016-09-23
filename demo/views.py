import logging

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import CreateView, FormView, UpdateView
from django.utils.decorators import method_decorator

from agnocomplete.views import (
    AgnocompleteGenericView,
    UserContextFormViewMixin
)
from agnocomplete.decorators import allow_create

from .forms import (
    SearchForm, SearchFormExtra, SearchContextForm, SearchCustom,
    SearchFormTextInput, SearchColorMulti,
    PersonTagForm, PersonTagModelForm,
    PersonTagModelFormWithCreate,
    PersonContextTagModelForm,
    UrlProxyForm, UrlProxyConvertForm,
    UrlProxyAuthForm,
)
from .autocomplete import HiddenAutocomplete
from .models import PersonTag

logger = logging.getLogger(__name__)


class AutoTitleMixin(object):

    def get_context_data(self, **kwargs):
        data = super(AutoTitleMixin, self).get_context_data(**kwargs)
        data.update({
            "title": self.title,
        })
        return data


class AutoView(AutoTitleMixin, FormView):
    template_name = 'base.html'
    form_class = SearchForm

    def post(self, request, **kwargs):
        logger.info(request.POST)
        return HttpResponse("POST request {}".format(dict(request.POST)))


class IndexView(AutoView):
    title = "Basic view, no JS"


class FilledFormView(AutoView):
    title = "Basic view, no JS, filled form"

    def get_form_kwargs(self):
        data = super(FilledFormView, self).get_form_kwargs()
        data.update({
            "data": {'search_color': 'grey', 'search_person': '1'}
        })
        return data


class SearchContextFormView(UserContextFormViewMixin, AutoView):
    title = "Form filtering on logged in user context"
    form_class = SearchContextForm

    def post(self, request, *args, **kwargs):
        form = self.get_form(form_class=self.form_class)
        if form.is_valid():
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest("KO")


class SearchCustomView(AutoView):
    title = "Form using a non-registered Agnocomplete class"
    form_class = SearchCustom


class HiddenAutocompleteView(AgnocompleteGenericView):
    klass = HiddenAutocomplete


# JS Demo views
class SelectizeView(AutoView):
    template_name = 'selectize.html'
    title = "View using the Selectize autocomplete front library"


class SelectizeExtraView(AutoView):
    template_name = 'selectize.html'
    title = "View using the Selectize autocomplete front library" \
        " + extra arguments"
    form_class = SearchFormExtra

    def get_context_data(self, *args, **kwargs):
        data = super(SelectizeExtraView, self).get_context_data(
            *args, **kwargs)
        data['selectize_with_extra'] = 'yes'
        return data


class SelectizeMultiView(AutoView):
    template_name = "selectize.html"
    title = "View using Selectize for a multi-select (tags)"
    form_class = SearchColorMulti


class Select2View(AutoView):
    template_name = 'select2.html'
    title = "View using the Select2 autocomplete front library"


class JqueryAutocompleteView(AutoView):
    template_name = 'jquery-autocomplete.html'
    title = "View using the JQuery autocomplete front library"
    form_class = SearchFormTextInput


class TypeaheadView(AutoView):
    template_name = 'typeahead.html'
    title = "View using the typeahead.js autocomplete front library"
    form_class = SearchFormTextInput


class PersonTagView(AutoView):
    template_name = "selectize.html"
    title = "Multi select with Models"
    form_class = PersonTagForm


class PersonTagModelView(AutoTitleMixin, CreateView):
    template_name = "selectize.html"
    title = "Multi select with Models & Modelforms (Create View)"
    form_class = PersonTagModelForm

    def get_success_url(self):
        return reverse('home')


class PersonTagModelViewEdit(AutoTitleMixin, UpdateView):
    template_name = "selectize.html"
    title = "Multi select with Models & Modelforms (Create View)"
    form_class = PersonTagModelForm
    model = PersonTag

    def get_success_url(self):
        return reverse('home')


class PersonTagModelViewWithCreate(PersonTagModelView):
    title = "Multi select with Models & Modelforms w/create mode (Create View)"
    form_class = PersonTagModelFormWithCreate

    # See documentation about this decorated method.
    @method_decorator(allow_create)
    def form_valid(self, form):
        return super(PersonTagModelViewWithCreate, self).form_valid(form)


class PersonContextTagView(AutoTitleMixin,
                           UserContextFormViewMixin,
                           CreateView):
    title = "Multi select w/ models w/ create mode w/ context"
    form_class = PersonContextTagModelForm
    template_name = "selectize.html"

    @method_decorator(allow_create)
    def form_valid(self, form):
        return super(PersonContextTagView, self).form_valid(form)

    def get_success_url(self):
        return reverse('home')


class UrlProxySimpleView(AutoView):
    form_class = UrlProxyForm
    title = 'Simple URL, returned data without transformation'
    template_name = "selectize.html"


class UrlProxyConvertView(AutoView):
    form_class = UrlProxyConvertForm
    title = 'Converted data when returned, more or less mangled'
    template_name = "selectize.html"


class UrlProxyAuthView(AutoView):
    form_class = UrlProxyAuthForm
    title = 'Authenticated URLs, returned normal data'
    template_name = "selectize.html"


index = IndexView.as_view()
filled_form = FilledFormView.as_view()
search_context = SearchContextFormView.as_view()
# Custom search
search_custom = SearchCustomView.as_view()
hidden_autocomplete = HiddenAutocompleteView.as_view()
# JS Demo views
selectize = SelectizeView.as_view()
selectize_extra = SelectizeExtraView.as_view()
selectize_multi = SelectizeMultiView.as_view()
select2 = Select2View.as_view()
jquery_autocomplete = JqueryAutocompleteView.as_view()
typeahead = TypeaheadView.as_view()
# Multi-select with models
selectize_tag = PersonTagView.as_view()
selectize_model_tag = PersonTagModelView.as_view()
selectize_model_tag_edit = PersonTagModelViewEdit.as_view()
selectize_model_tag_with_create = PersonTagModelViewWithCreate.as_view()
selectize_context_tag = PersonContextTagView.as_view()
# URL proxies
url_proxy_simple = UrlProxySimpleView.as_view()
url_proxy_convert = UrlProxyConvertView.as_view()
url_proxy_auth = UrlProxyAuthView.as_view()
