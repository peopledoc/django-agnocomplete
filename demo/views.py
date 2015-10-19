from django.views.generic import FormView
from django.http import HttpResponse, HttpResponseBadRequest

from agnocomplete.views import AgnocompleteGenericView, UserContextFormMixin

from .forms import (SearchForm, SearchContextForm, SearchCustom,
                    SearchFormTextInput)
from .autocomplete import HiddenAutocomplete


class AutoView(FormView):
    template_name = 'base.html'
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        data = super(AutoView, self).get_context_data(**kwargs)
        data.update({
            "title": self.title,
        })
        return data


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


class SearchContextFormView(UserContextFormMixin, AutoView):
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


index = IndexView.as_view()
filled_form = FilledFormView.as_view()
search_context = SearchContextFormView.as_view()
# Custom search
search_custom = SearchCustomView.as_view()
hidden_autocomplete = HiddenAutocompleteView.as_view()
# JS Demo views
selectize = SelectizeView.as_view()
select2 = Select2View.as_view()
jquery_autocomplete = JqueryAutocompleteView.as_view()
typeahead = TypeaheadView.as_view()
