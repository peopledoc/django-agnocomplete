"""
Django app definition.

The :class:`AgnocompleteConfig` class should start the agnocomplete
autodiscover.
"""

from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class AgnocompleteConfig(AppConfig):
    """
    Agnocomplete application configuration class. Runs the autodiscover.
    """
    name = 'agnocomplete'

    def ready(self):
        """
        Initialize the autodiscover when ready
        """
        from . import autodiscover
        autodiscover()
