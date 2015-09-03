"""
Registry handling
"""
import logging
logger = logging.getLogger(__name__)

AUTOCOMPLETE_REGISTRY = {}


def register(autocomplete):
    logger.info("registering {}".format(autocomplete.__name__))
    AUTOCOMPLETE_REGISTRY[autocomplete.__name__] = autocomplete


def get_autocomplete_registry():
    "Get the registered autocompletes."
    return AUTOCOMPLETE_REGISTRY
