"""
Django app definition.

The :class:`AgnocompleteConfig` class should start the agnocomplete
autodiscover.
"""

from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class AgnocompleteConfig(AppConfig):
    name = 'agnocomplete'

    def ready(self):
        from . import autodiscover
        autodiscover()
