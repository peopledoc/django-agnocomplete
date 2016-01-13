"""
Agnocomplete, the Agnostic Autocomplete Django app.

"""
import logging

from distutils.version import StrictVersion

import django
from django.conf import settings
from django.utils.importlib import import_module

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
    module_name = "autocomplete"
    for app in settings.INSTALLED_APPS:
        # Attempt to import the app's 'routing' module
        module = '{}.{}'.format(app, module_name)
        try:
            import_module(module)
        except ImportError as ex:
            reason = ex.args[0]
            if 'No module named {}'.format(module_name) in reason \
                    or "No module named '{}'".format(module) in reason:
                logger.info('No module named {}'.format(module))
            else:  # re-raise - something's wrong
                logger.warning(ex)
                raise ImportError(ex)

default_app_config = 'agnocomplete.app.AgnocompleteConfig'


if StrictVersion(django.get_version()) < StrictVersion('1.7'):
    # We need to load the register before the admin site tries to collect it.
    # It's Django 1.6 specific, because it doesn't handle the Django 1.7+ app
    # loading.
    autodiscover()
