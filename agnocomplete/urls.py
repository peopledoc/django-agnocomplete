"""
Agnostic Autocomplete URLS
"""
from django.urls import re_path
from .views import AgnocompleteView, CatalogView

urlpatterns = [
    re_path(
        r'^(?P<klass>[-_\w]+)/$',
        AgnocompleteView.as_view(),
        name='agnocomplete'),
    re_path(r'^$', CatalogView.as_view(), name='catalog'),
]
