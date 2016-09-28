"""
Demo URL Configuration
"""
from django.conf.urls import url
from . import views_proxy


urlpatterns = [
    url(r'^item/(?P<pk>[0-9]+)$', views_proxy.item, name='item'),
    url(r'^simple/$', views_proxy.simple, name='simple'),
    url(r'^simple-post/$', views_proxy.simple_post, name='simple-post'),
    url(r'^convert/$', views_proxy.convert, name='convert'),
    url(r'^convert-complex/$',
        views_proxy.convert_complex, name='convert-complex'),
    url(r'^convert-schema/$',
        views_proxy.convert_schema, name='convert-schema'),
    url(r'^convert-schema-list/$',
        views_proxy.convert_schema_list, name='convert-schema-list'),
    url(r'^simple-auth/$', views_proxy.simple_auth, name='simple-auth'),
    url(r'^headers-auth/$', views_proxy.headers_auth, name='headers-auth'),
]
