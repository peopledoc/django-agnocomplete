"""
Agnocomplete, the Agnostic Autocomplete Django app.

"""
import logging

from django.conf import settings
from django.utils.module_loading import import_module

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
        except ImportError:
            pass


default_app_config = 'agnocomplete.app.AgnocompleteConfig'
