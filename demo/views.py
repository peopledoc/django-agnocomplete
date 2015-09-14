from django.views.generic import TemplateView

from agnocomplete.views import AgnocompleteGenericView

from .forms import (SearchForm, SearchContextForm, SearchCustom,
                    SearchFormTextInput)
from .autocomplete import HiddenAutocomplete


class AutoView(TemplateView):
    template_name = 'base.html'

    def get_form(self):
        return SearchForm()

    def get_context_data(self):
        data = super(AutoView, self).get_context_data()
        data.update({
            "form": self.get_form(),
            "title": self.title,
        })
        return data


class IndexView(AutoView):
    title = "Basic view, no JS"


class FilledFormView(AutoView):
    title = "Basic view, no JS, filled form"

    def get_form(self):
        return SearchForm({'search_color': 'grey', 'search_person': '1'})


class SearchContextFormView(AutoView):
    title = "Form filtering on logged in user context"

    def get_form(self):
        return SearchContextForm()


class SearchCustomView(AutoView):
    title = "Form using a non-registered Agnocomplete class"

    def get_form(self):
        return SearchCustom()


class HiddenAutocompleteView(AgnocompleteGenericView):
    klass = HiddenAutocomplete


# JS Demo views
class SelectizeView(AutoView):
    template_name = 'selectize.html'
    title = "View using the Selectize autocomplete front library"


class JqueryAutocompleteView(AutoView):
    template_name = 'jquery-autocomplete.html'
    title = "View using the JQuery autocomplete front library"

    def get_form(self):
        return SearchFormTextInput()


index = IndexView.as_view()
filled_form = FilledFormView.as_view()
search_context = SearchContextFormView.as_view()
# Custom search
search_custom = SearchCustomView.as_view()
hidden_autocomplete = HiddenAutocompleteView.as_view()
# JS Demo views
selectize = SelectizeView.as_view()
jquery_autocomplete = JqueryAutocompleteView.as_view()
