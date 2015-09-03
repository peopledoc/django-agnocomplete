"""
Autocomplete URLS
"""
from django.conf.urls import patterns, url
from .views import AutocompleteView, CatalogView

urlpatterns = [
    url(
        r'^(?P<klass>[-_\w]+)/$',
        AutocompleteView.as_view(),
        name='autocomplete'),
    url(r'^$', CatalogView.as_view(), name='catalog'),
]

urlpatterns = patterns('', *urlpatterns)
