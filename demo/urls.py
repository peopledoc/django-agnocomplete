"""
Demo URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from agnocomplete import get_namespace

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^agnocomplete/',
        include(
            'agnocomplete.urls',
            namespace=get_namespace()
        )
    ),

    # Templated DEMO views
    url(r'^$', 'demo.views.index', name='home'),
    url(r'^selectize/$', 'demo.views.selectize', name='selectize'),
    url(r'^filled-form/$', 'demo.views.filled_form', name='filled-form'),
    url(r'^search-context/$',
        'demo.views.search_context', name='search-context'),
]
