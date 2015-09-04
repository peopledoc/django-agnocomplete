"""
Demo URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^autocomplete/',
        include('agnocomplete.urls', namespace='autocomplete')),

    # Templated DEMO views
    url(r'^$', 'demo.views.index', name='home'),
]
