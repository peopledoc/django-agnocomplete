"""
Registry handling
"""
import logging
logger = logging.getLogger(__name__)

AGNOCOMPLETE_REGISTRY = {}


def register(klass):
    "Register a class into the agnocomplete registry."
    logger.info("registering {}".format(klass.__name__))
    AGNOCOMPLETE_REGISTRY[klass.__name__] = klass


def get_agnocomplete_registry():
    "Get the registered agnostic autocompletes."
    return AGNOCOMPLETE_REGISTRY
