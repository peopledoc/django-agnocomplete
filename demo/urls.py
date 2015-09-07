"""
Demo URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^agnocomplete/',
        # FIXME: the namespace should be a settings var.
        include('agnocomplete.urls', namespace='agnocomplete')),

    # Templated DEMO views
    url(r'^$', 'demo.views.index', name='home'),
    url(r'^filled-form/$', 'demo.views.filled_form', name='filled-form'),
]
