from django.http import Http404
from django.views.generic import View
from django.utils.functional import cached_property
from .register import get_agnocomplete_registry

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


class JSONView(View):

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

    @cached_property
    def registry(self):
        return get_agnocomplete_registry()


class CatalogView(RegistryMixin, JSONView):
    def get_dataset(self):
        return tuple(self.registry.keys())


class AgnocompleteView(RegistryMixin, JSONView):

    def get_dataset(self):
        klass_name = self.kwargs.get('klass', None)
        klass = self.registry.get(klass_name, None)
        if not klass:
            raise Http404("Unknown autocomplete class `{}`".format(klass_name))
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
        instance = klass(user=self.request.user, page_size=page_size)
        return instance.items(query=query)
