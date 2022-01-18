"""
Agnocomplete views.
"""
from abc import abstractmethod, ABCMeta
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import Http404, JsonResponse
from django.utils.encoding import force_str as text
from django.utils.functional import cached_property
from django.views.generic import View

from .register import get_agnocomplete_registry
from .exceptions import (
    AuthenticationRequiredAgnocompleteException,
    ImproperlyConfiguredView
)
from requests.exceptions import HTTPError, Timeout


def get_error(exc):
    """
    Return the appropriate HTTP status code according to the Exception/Error.
    """

    if isinstance(exc, HTTPError):
        # Returning the HTTP Error code coming from requests module
        return exc.response.status_code, text(exc.response.content)

    if isinstance(exc, Timeout):
        # A timeout is a 408, and it's not a HTTPError (why? dunno).
        return 408, exc

    if isinstance(exc, Http404):
        # 404 is 404
        return 404, exc

    if isinstance(exc, PermissionDenied):
        # Permission denied is 403
        return 403, exc

    if isinstance(exc, SuspiciousOperation):
        # Shouldn't happen, but you never know
        return 400, exc

    # The default error code is 500
    return 500, exc


class AgnocompleteJSONView(View, metaclass=ABCMeta):
    """
    Generic toolbox for JSON-returning views
    """

    @property
    def content_type(self):
        """
        Return content-type of the response.
        For a JSONResponseMixin, the obvious answer is ``application/json``.
        But Internet Explorer v8 can't handle this content-type and instead
        of processing it as a normal AJAX data response, it tries to download
        it.
        We're tricking this behaviour by sending back a ``text/html``
        content-type header instead.
        """
        if 'HTTP_X_REQUESTED_WITH' in self.request.META:
            return "application/json;charset=utf-8"
        else:
            return "text/html"

    @abstractmethod
    def get_dataset(self, **kwargs):
        pass

    def get_extra_arguments(self):
        extra = filter(lambda x: x[0] != 'q', self.request.GET.items())
        return dict(extra)

    def get(self, *args, **kwargs):
        try:
            dataset = self.get_dataset(**self.get_extra_arguments())
            return JsonResponse(
                {'data': dataset},
                content_type=self.content_type,
            )
        except Exception as exc:
            status, message = get_error(exc)
            return JsonResponse(
                {"errors": [{
                    "title": "An error has occurred",
                    "detail": "{}".format(message)
                }]},
                content_type=self.content_type,
                status=status,
            )


class RegistryMixin:
    """
    This mixin is able to return the agnocomplete registry.
    """
    @cached_property
    def registry(self):
        """
        Return the agnocomplete registry (cached)
        """
        return get_agnocomplete_registry()


class UserContextFormViewMixin:
    """
    This mixin is injecting the context variable into the form kwargs
    """

    def get_agnocomplete_context(self):
        """
        Return the view current user.

        You may want to change this value by overrding this method.
        """
        return self.request.user

    def get_form_kwargs(self):
        """
        Return the form kwargs.

        This method injects the context variable, defined in
        :meth:`get_agnocomplete_context`. Override this method to adjust it to
        your needs.
        """
        data = super().get_form_kwargs()
        data.update({
            'user': self.get_agnocomplete_context(),
        })
        return data


class CatalogView(RegistryMixin, AgnocompleteJSONView):
    """
    The catalog view displays every available Agnocomplete slug available in
    the registry.
    """
    def get_dataset(self, **kwargs):
        """
        Return the registry key set.
        """
        return tuple(self.registry.keys())


class AgnocompleteGenericView(AgnocompleteJSONView):
    def get_klass(self):
        """
        Return the agnocomplete class to be used with the eventual query.
        """
        # Return the instance if it's defined in the class properties
        if hasattr(self, 'klass') and self.klass:
            return self.klass
        raise ImproperlyConfiguredView("Undefined autocomplete class")

    def get_dataset(self, **kwargs):
        klass = self.get_klass()
        # Query passed via the argument
        query = self.request.GET.get('q', "")
        if not query:
            # Empty set, no value to complete
            return []

        # Optional Page size
        try:
            page_size = int(self.request.GET.get('page_size', None))
        except Exception:
            page_size = None

        # Agnocomplete instance is ready
        try:
            instance = klass(user=self.request.user, page_size=page_size)
            return instance.items(query=query, **kwargs)
        except AuthenticationRequiredAgnocompleteException:
            raise PermissionDenied(
                "Unauthorized access to this Autocomplete")
        except Exception:
            # re-raise the unknown exception
            raise


class AgnocompleteView(RegistryMixin, AgnocompleteGenericView):

    def get_klass(self):
        """
        Return the agnocomplete class to be used with the eventual query.
        """
        # Extract the klass name from the URL arguments
        klass_name = self.kwargs.get('klass', None)
        klass = self.registry.get(klass_name, None)
        if not klass:
            raise Http404("Unknown autocomplete class `{}`".format(klass_name))
        return klass
