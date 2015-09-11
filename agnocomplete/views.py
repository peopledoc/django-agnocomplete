"""
Agnocomplete views.
"""
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.functional import cached_property
from django.views.generic import View

from .register import get_agnocomplete_registry
from .exceptions import (
    AuthenticationRequiredAgnocompleteException,
    ImproperlyConfiguredView
)


try:
    from django.http import JsonResponse
except ImportError:
    # JsonResponse for Django 1.6.
    # Source: https://gist.github.com/philippeowagner/3179eb475fe1795d6515
    import json
    from django.http import HttpResponse

    class JsonResponse(HttpResponse):
        """
        JSON response
        """
        def __init__(self, content,
                     status=None, content_type=None):
            super(JsonResponse, self).__init__(
                content=json.dumps(content),
                status=status, content_type=content_type)


class AgnocompleteJSONView(View):
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
            return "application/json;charset UTF-8"
        else:
            return "text/html"

    def get_dataset(self):
        raise NotImplementedError("You must implement a `get_dataset` method")

    def get(self, *args, **kwargs):
        return JsonResponse(
            {'data': self.get_dataset()},
            content_type=self.content_type,
        )


class RegistryMixin(object):
    """
    This mixin is able to return the agnocomplete registry.
    """
    @cached_property
    def registry(self):
        """
        Return the agnocomplete registry (cached)
        """
        return get_agnocomplete_registry()


class CatalogView(RegistryMixin, AgnocompleteJSONView):
    """
    The catalog view displays every available Agnocomplete slug available in
    the registry.
    """
    def get_dataset(self):
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

    def get_dataset(self):
        klass = self.get_klass()
        # Query passed via the argument
        query = self.request.GET.get('q', "")
        if not query:
            # Empty set, no value to complete
            return []

        # Optional Page size
        try:
            page_size = int(self.request.GET.get('page_size', None))
        except:
            page_size = None

        # Agnocomplete instance is ready
        try:
            instance = klass(user=self.request.user, page_size=page_size)
            return instance.items(query=query)
        except AuthenticationRequiredAgnocompleteException:
            raise PermissionDenied(
                "Unauthorized access to this Autocomplete")
        except:
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
