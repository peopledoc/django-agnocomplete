"""
Demo URL Configuration
"""
from django.urls import re_path
from . import views_proxy


urlpatterns = [
    re_path(r'^item/(?P<pk>[0-9]+)$', views_proxy.item, name='item'),
    re_path(r'^atomicitem/(?P<pk>[0-9]+)$', views_proxy.atomic_item,
        name='atomic-item'),
    re_path(r'^simple/$', views_proxy.simple, name='simple'),
    re_path(r'^simple-post/$', views_proxy.simple_post, name='simple-post'),
    re_path(r'^convert/$', views_proxy.convert, name='convert'),
    re_path(r'^convert-complex/$',
        views_proxy.convert_complex, name='convert-complex'),
    re_path(r'^convert-schema/$',
        views_proxy.convert_schema, name='convert-schema'),
    re_path(r'^convert-schema-list/$',
        views_proxy.convert_schema_list, name='convert-schema-list'),
    re_path(r'^simple-auth/$', views_proxy.simple_auth, name='simple-auth'),
    re_path(r'^headers-auth/$', views_proxy.headers_auth, name='headers-auth'),
    re_path(r'^errors/$', views_proxy.errors, name='errors'),
]
