from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class AgnocompleteConfig(AppConfig):
    name = 'agnocomplete'

    def ready(self):
        from . import autodiscover
        autodiscover()
