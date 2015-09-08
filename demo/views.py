from django.views.generic import TemplateView
from .forms import SearchForm


class AutoView(TemplateView):

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
    template_name = 'base.html'
    title = "Basic view, no JS"


class SelectizeView(AutoView):
    template_name = 'selectize.html'
    title = "View using the Selectize autocomplete front library"


class FilledFormView(AutoView):
    template_name = 'base.html'
    title = "Basic view, no JS, filled form"

    def get_form(self):
        return SearchForm({'search_color': 'grey', 'search_person': '1'})

index = IndexView.as_view()
selectize = SelectizeView.as_view()
filled_form = FilledFormView.as_view()
