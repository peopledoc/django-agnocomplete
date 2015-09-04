from django.views.generic import TemplateView
from .forms import SearchForm


class AutoView(TemplateView):

    def get_context_data(self):
        data = super(AutoView, self).get_context_data()
        data.update({
            "form": SearchForm(),
            "title": self.title,
        })
        return data


class IndexView(AutoView):
    template_name = 'base.html'
    title = "Basic view, no JS"

index = IndexView.as_view()
