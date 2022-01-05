"""
Agnostic Autocomplete URLS
"""
from django.urls import path
from .views import AgnocompleteView, CatalogView

urlpatterns = [
    path(
        r'^(?P<klass>[-_\w]+)/$',
        AgnocompleteView.as_view(),
        name='agnocomplete'),
    path(r'^$', CatalogView.as_view(), name='catalog'),
]
