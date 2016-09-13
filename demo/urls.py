"""
Demo URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin

from agnocomplete import get_namespace


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # Autodiscovered URLs
    url(
        r'^agnocomplete/',
        include(
            'agnocomplete.urls',
            namespace=get_namespace()
        )
    ),

    # Agnocomplete Custom view
    url(r'^hidden-autocomplete/$', 'demo.views.hidden_autocomplete',
        name='hidden-autocomplete'),

    # Templated DEMO views
    url(r'^$', 'demo.views.index', name='home'),
    url(r'^filled-form/$', 'demo.views.filled_form', name='filled-form'),
    url(r'^search-context/$', 'demo.views.search_context', name='search-context'),  # noqa
    url(r'^custom/$', 'demo.views.search_custom', name='search-custom'),
    # Demo Front JS views
    url(r'^selectize/$', 'demo.views.selectize', name='selectize'),
    url(r'^selectize-extra/$', 'demo.views.selectize_extra', name='selectize-extra'),  # noqa
    url(r'^selectize-multi/$', 'demo.views.selectize_multi', name='selectize-multi'),  # noqa
    url(r'^selectize-tag/$', 'demo.views.selectize_tag', name='selectize-tag'),
    url(r'^selectize-model-tag/$', 'demo.views.selectize_model_tag', name='selectize-model-tag'),  # noqa
    url(r'^selectize-model-tag/edit/(?P<pk>\d+)/$',
        'demo.views.selectize_model_tag_edit',
        name='selectize-model-tag-edit'),  # noqa
    url(r'^selectize-model-tag-with-create/$', 'demo.views.selectize_model_tag_with_create', name='selectize-model-tag-with-create'),  # noqa
    url(r'^selectize-context-tag/$', 'demo.views.selectize_context_tag', name='selectize-context-tag'),  # noqa
    # Select 2, jquery-autocomplete, typeahead
    url(r'^select2/$', 'demo.views.select2', name='select2'),
    url(r'^jquery-autocomplete/$', 'demo.views.jquery_autocomplete',
        name='jquery-autocomplete'),
    url(r'^typeahead/$', 'demo.views.typeahead', name='typeahead'),

    url(r'^url-proxy-simple', 'demo.views.url_proxy_simple',
        name='url-proxy-simple'),

    # Mock Third Party URLs
    url(r'^3rdparty/', include('demo.urls_proxy', namespace='url-proxy')),

]
