"""
Agnocomplete exception classes
"""
from requests.exceptions import HTTPError


class UnregisteredAgnocompleteException(Exception):
    """
    Occurs when trying to instanciate an unregistered Agnocompletion class
    """
    pass


class AuthenticationRequiredAgnocompleteException(Exception):
    """
    Occurs when trying to instanciate an unregistered Agnocompletion class
    """
    pass


class ImproperlyConfiguredView(Exception):
    """
    Occurs if you want to misuse an AgnocompleteGenericView
    """
    pass


class HTTPError(HTTPError):
    """
    Occurs when the 3rd party API returns an error code
    """
    pass


class SkipItem(Exception):
    """
    Occurs when Item has to be skipped when building the final Payload
    """
    pass
