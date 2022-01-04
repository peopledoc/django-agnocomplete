"""
Agnocomplete, the Agnostic Autocomplete Django app.

"""
import logging

import django
from django.conf import settings
from django.utils.module_loading import autodiscover_modules

logger = logging.getLogger(__name__)


def get_namespace():
    """
    Return the agnocomplete view namespace.

    Default value is "agnocomplete", but it can be overridden using the
    ``AGNOCOMPLETE_NAMESPACE`` settings variable.
    """
    return getattr(settings, 'AGNOCOMPLETE_NAMESPACE', 'agnocomplete')


def autodiscover():
    """Auto-discover INSTALLED_APPS agnocomplete modules."""
    autodiscover_modules('autocomplete')


if django.VERSION[:2] < (3, 2):
    default_app_config = 'agnocomplete.app.AgnocompleteConfig'
