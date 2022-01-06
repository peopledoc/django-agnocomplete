"""
Demo URL Configuration
"""
from django.conf.urls import include
from django.urls import path
from django.contrib import admin

from agnocomplete import get_namespace
from . import views


urlpatterns = [
    path(r'^admin/', admin.site.urls),

    # Autodiscovered URLs
    path(
        r'^agnocomplete/',
        include(
            ('agnocomplete.urls', 'agnocomplete'),
            namespace=get_namespace()
        )
    ),

    # Agnocomplete Custom view
    path(r'^hidden-autocomplete/$', views.hidden_autocomplete,
        name='hidden-autocomplete'),

    # Templated DEMO views
    path(r'^$', views.index, name='home'),
    path(r'^filled-form/$', views.filled_form, name='filled-form'),
    path(r'^search-context/$', views.search_context, name='search-context'),
    path(r'^custom/$', views.search_custom, name='search-custom'),
    # Demo Front JS views
    path(r'^selectize/$', views.selectize, name='selectize'),
    path(r'^selectize-extra/$', views.selectize_extra, name='selectize-extra'),
    path(r'^selectize-multi/$', views.selectize_multi, name='selectize-multi'),
    path(r'^selectize-tag/$', views.selectize_tag, name='selectize-tag'),
    path(r'^selectize-model-tag/$',
        views.selectize_model_tag, name='selectize-model-tag'),
    path(r'^selectize-model-tag/edit/(?P<pk>\d+)/$',
        views.selectize_model_tag_edit,
        name='selectize-model-tag-edit'),
    path(r'^selectize-model-tag-with-create/$',
        views.selectize_model_tag_with_create,
        name='selectize-model-tag-with-create'),
    path(r'^selectize-model-tag-with-duplicate-create/$',
        views.selectize_model_tag_with_duplicate_create,
        name='selectize-model-tag-with-duplicate-create'),
    path(r'^selectize-context-tag/$',
        views.selectize_context_tag, name='selectize-context-tag'),
    # Select 2, jquery-autocomplete, typeahead
    path(r'^select2/$', views.select2, name='select2'),
    path(r'^jquery-autocomplete/$', views.jquery_autocomplete,
        name='jquery-autocomplete'),
    path(r'^typeahead/$', views.typeahead, name='typeahead'),

    # URL Proxy Urls
    path(r'^url-proxy-simple/$', views.url_proxy_simple,
        name='url-proxy-simple'),
    path(r'^url-proxy-convert/$', views.url_proxy_convert,
        name='url-proxy-convert'),
    path(r'^url-proxy-auth/$', views.url_proxy_auth,
        name='url-proxy-auth'),
    path(r'^url-proxy-errors/$', views.url_proxy_errors,
        name='url-proxy-errors'),
    path(r'^url-proxy-with-extra/$', views.url_proxy_with_extra,
        name='url-proxy-with-extra'),

    # Mock Third Party URLs
    path(r'^3rdparty/', include(('demo.urls_proxy', 'url-proxy')))

]
