"""
Demo URL Configuration
"""
from django.conf.urls import url
from . import views_proxy


urlpatterns = [
    url(r'^item/(?P<pk>[0-9]+)$', views_proxy.item, name='item'),
    url(r'^simple/$', views_proxy.simple, name='simple'),
]
