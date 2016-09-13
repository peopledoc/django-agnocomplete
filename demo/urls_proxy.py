"""
Demo URL Configuration
"""
from django.conf.urls import url
from . import views_proxy


urlpatterns = [
    url(r'^simple/$', views_proxy.simple, name='simple'),
]
