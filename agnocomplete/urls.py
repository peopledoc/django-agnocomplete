"""
Agnostic Autocomplete URLS
"""
from django.urls import path
from .views import AgnocompleteView, CatalogView

urlpatterns = [
    path('<klass>/', AgnocompleteView.as_view(), name='agnocomplete'),
    path('', CatalogView.as_view(), name='catalog'),
]
