"""
Demo URL Configuration
"""
from django.conf.urls import include
from django.urls import re_path
from django.contrib import admin

from agnocomplete import get_namespace
from . import views


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),

    # Autodiscovered URLs
    re_path(
        r'^agnocomplete/',
        include(
            ('agnocomplete.urls', 'agnocomplete'),
            namespace=get_namespace()
        )
    ),

    # Agnocomplete Custom view
    re_path(r'^hidden-autocomplete/$', views.hidden_autocomplete,
        name='hidden-autocomplete'),

    # Templated DEMO views
    re_path(r'^$', views.index, name='home'),
    re_path(r'^filled-form/$', views.filled_form, name='filled-form'),
    re_path(r'^search-context/$', views.search_context, name='search-context'),
    re_path(r'^custom/$', views.search_custom, name='search-custom'),
    # Demo Front JS views
    re_path(r'^selectize/$', views.selectize, name='selectize'),
    re_path(r'^selectize-extra/$', views.selectize_extra, name='selectize-extra'),
    re_path(r'^selectize-multi/$', views.selectize_multi, name='selectize-multi'),
    re_path(r'^selectize-tag/$', views.selectize_tag, name='selectize-tag'),
    re_path(r'^selectize-model-tag/$',
        views.selectize_model_tag, name='selectize-model-tag'),
    re_path(r'^selectize-model-tag/edit/(?P<pk>\d+)/$',
        views.selectize_model_tag_edit,
        name='selectize-model-tag-edit'),
    re_path(r'^selectize-model-tag-with-create/$',
        views.selectize_model_tag_with_create,
        name='selectize-model-tag-with-create'),
    re_path(r'^selectize-model-tag-with-duplicate-create/$',
        views.selectize_model_tag_with_duplicate_create,
        name='selectize-model-tag-with-duplicate-create'),
    re_path(r'^selectize-context-tag/$',
        views.selectize_context_tag, name='selectize-context-tag'),
    # Select 2, jquery-autocomplete, typeahead
    re_path(r'^select2/$', views.select2, name='select2'),
    re_path(r'^jquery-autocomplete/$', views.jquery_autocomplete,
        name='jquery-autocomplete'),
    re_path(r'^typeahead/$', views.typeahead, name='typeahead'),

    # URL Proxy Urls
    re_path(r'^url-proxy-simple/$', views.url_proxy_simple,
        name='url-proxy-simple'),
    re_path(r'^url-proxy-convert/$', views.url_proxy_convert,
        name='url-proxy-convert'),
    re_path(r'^url-proxy-auth/$', views.url_proxy_auth,
        name='url-proxy-auth'),
    re_path(r'^url-proxy-errors/$', views.url_proxy_errors,
        name='url-proxy-errors'),
    re_path(r'^url-proxy-with-extra/$', views.url_proxy_with_extra,
        name='url-proxy-with-extra'),

    # Mock Third Party URLs
    re_path(r'^3rdparty/', include(('demo.urls_proxy', 'url-proxy')))

]
