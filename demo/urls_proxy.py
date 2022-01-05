"""
Demo URL Configuration
"""
from django.urls import path
from . import views_proxy


urlpatterns = [
    path(r'^item/(?P<pk>[0-9]+)$', views_proxy.item, name='item'),
    path(r'^atomicitem/(?P<pk>[0-9]+)$', views_proxy.atomic_item,
        name='atomic-item'),
    path(r'^simple/$', views_proxy.simple, name='simple'),
    path(r'^simple-post/$', views_proxy.simple_post, name='simple-post'),
    path(r'^convert/$', views_proxy.convert, name='convert'),
    path(r'^convert-complex/$',
        views_proxy.convert_complex, name='convert-complex'),
    path(r'^convert-schema/$',
        views_proxy.convert_schema, name='convert-schema'),
    path(r'^convert-schema-list/$',
        views_proxy.convert_schema_list, name='convert-schema-list'),
    path(r'^simple-auth/$', views_proxy.simple_auth, name='simple-auth'),
    path(r'^headers-auth/$', views_proxy.headers_auth, name='headers-auth'),
    path(r'^errors/$', views_proxy.errors, name='errors'),
]
