"""
Demo URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

from agnocomplete import get_namespace
from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Autodiscovered URLs
    url(
        r'^agnocomplete/',
        include(
            ('agnocomplete.urls', 'agnocomplete'),
            namespace=get_namespace()
        )
    ),

    # Agnocomplete Custom view
    url(r'^hidden-autocomplete/$', views.hidden_autocomplete,
        name='hidden-autocomplete'),

    # Templated DEMO views
    url(r'^$', views.index, name='home'),
    url(r'^filled-form/$', views.filled_form, name='filled-form'),
    url(r'^search-context/$', views.search_context, name='search-context'),
    url(r'^custom/$', views.search_custom, name='search-custom'),
    # Demo Front JS views
    url(r'^selectize/$', views.selectize, name='selectize'),
    url(r'^selectize-extra/$', views.selectize_extra, name='selectize-extra'),
    url(r'^selectize-multi/$', views.selectize_multi, name='selectize-multi'),
    url(r'^selectize-tag/$', views.selectize_tag, name='selectize-tag'),
    url(r'^selectize-model-tag/$',
        views.selectize_model_tag, name='selectize-model-tag'),
    url(r'^selectize-model-tag/edit/(?P<pk>\d+)/$',
        views.selectize_model_tag_edit,
        name='selectize-model-tag-edit'),
    url(r'^selectize-model-tag-with-create/$',
        views.selectize_model_tag_with_create,
        name='selectize-model-tag-with-create'),
    url(r'^selectize-model-tag-with-duplicate-create/$',
        views.selectize_model_tag_with_duplicate_create,
        name='selectize-model-tag-with-duplicate-create'),
    url(r'^selectize-context-tag/$',
        views.selectize_context_tag, name='selectize-context-tag'),
    # Select 2, jquery-autocomplete, typeahead
    url(r'^select2/$', views.select2, name='select2'),
    url(r'^jquery-autocomplete/$', views.jquery_autocomplete,
        name='jquery-autocomplete'),
    url(r'^typeahead/$', views.typeahead, name='typeahead'),

    # URL Proxy Urls
    url(r'^url-proxy-simple/$', views.url_proxy_simple,
        name='url-proxy-simple'),
    url(r'^url-proxy-convert/$', views.url_proxy_convert,
        name='url-proxy-convert'),
    url(r'^url-proxy-auth/$', views.url_proxy_auth,
        name='url-proxy-auth'),
    url(r'^url-proxy-errors/$', views.url_proxy_errors,
        name='url-proxy-errors'),
    url(r'^url-proxy-with-extra/$', views.url_proxy_with_extra,
        name='url-proxy-with-extra'),

    # Mock Third Party URLs
    url(r'^3rdparty/', include(('demo.urls_proxy', 'url-proxy')))

]
