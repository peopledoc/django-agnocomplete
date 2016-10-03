import json
import logging

from django.core.exceptions import PermissionDenied
from django.http import (
    HttpResponse,
    Http404,
    HttpResponseNotFound,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponseServerError,
)
from django.utils.encoding import force_text as text
from django.views.decorators.http import require_GET, require_POST

from . import DATABASE, GOODAUTHTOKEN

logger = logging.getLogger(__name__)


def convert_data(item):
    return {'value': item['pk'], 'label': item['name']}


def convert_data_complex(item):
    first, last = item['name'].split(' ')
    return {
        'pk': item['pk'],
        'first_name': first,
        'last_name': last,
    }


def _search(search_term, convert_func, key='data'):
    data = []
    if search_term:
        data = filter(lambda x: search_term in x['name'], DATABASE)
    if data and convert_func:
        data = map(convert_func, data)
    data = list(data)
    result = {key: data}
    return result


@require_GET
def simple(request, *args, **kwargs):
    search_term = request.GET.get('q', None)
    result = _search(search_term, convert_data)
    response = json.dumps(result)
    logger.debug('3rd party simple search: `%s`', search_term)
    logger.debug('response: `%s`', response)
    return HttpResponse(response)


@require_GET
def convert(request, *args, **kwargs):
    search_term = request.GET.get('q', None)
    # Fetching result and not converting the item JSON payload.
    # i.e.: leaving the pk/name labels.
    result = _search(search_term, None)
    response = json.dumps(result)
    logger.debug('3rd party converted search: `%s`', search_term)
    logger.debug('response: `%s`', response)
    return HttpResponse(response)


@require_GET
def convert_complex(request, *args, **kwargs):
    search_term = request.GET.get('q', None)
    # Fetching result without converting item JSON payload.
    result = _search(search_term, convert_data_complex)
    response = json.dumps(result)
    logger.debug('3rd party complex conversion search: `%s`', search_term)
    logger.debug('response: `%s`', response)
    return HttpResponse(response)


@require_GET
def convert_schema(request, *args, **kwargs):
    search_term = request.GET.get('q', None)
    # Fetching result without converting item JSON payload.
    result = _search(search_term, convert_data, key='result')
    response = json.dumps(result)
    logger.debug('3rd party schema conversion search: `%s`', search_term)
    logger.debug('response: `%s`', response)
    return HttpResponse(response)


@require_GET
def convert_schema_list(request, *args, **kwargs):
    """
    Return a list of items not embedded in a dict.
    """
    search_term = request.GET.get('q', None)
    # Fetching result without converting item JSON payload.
    result = _search(search_term, convert_data)
    response = json.dumps(result.get('data', []))
    logger.debug(
        '3rd party schema conversion search w/ list: `%s`', search_term)
    logger.debug('response: `%s`', response)
    return HttpResponse(response)


@require_GET
def simple_auth(request, *args, **kwargs):
    # Check authentication
    auth_token = request.GET.get('auth_token', None)
    if not auth_token or auth_token != GOODAUTHTOKEN:
        logger.error('Error: Failed authentication')
        raise PermissionDenied("Failed Authentication")
    search_term = request.GET.get('q', None)
    result = _search(search_term, convert_data)
    response = json.dumps(result)
    logger.debug('3rd party simple search: `%s`', search_term)
    logger.debug('response: `%s`', response)
    return HttpResponse(response)


@require_GET
def headers_auth(request, *args, **kwargs):
    # Check authentication
    auth_token = request.META.get('HTTP_X_API_TOKEN', None)
    if not auth_token or auth_token != GOODAUTHTOKEN:
        logger.error('Error: Failed authentication')
        raise PermissionDenied("Failed Authentication")
    search_term = request.GET.get('q', None)
    result = _search(search_term, convert_data)
    response = json.dumps(result)
    logger.debug('3rd party simple search: `%s`', search_term)
    logger.debug('response: `%s`', response)
    return HttpResponse(response)


@require_POST
def simple_post(request, *args, **kwargs):
    search_term = request.POST.get('q', None)
    result = _search(search_term, convert_data)
    response = json.dumps(result)
    logger.debug('3rd party POST search: `%s`', search_term)
    logger.debug('response: `%s`', response)
    return HttpResponse(response)


@require_GET
def errors(request, *args, **kwargs):
    """
    A dummy view that will throw errors.

    It'll throw any HTTP error that is contained in the search query.
    """
    search_term = request.GET.get('q', None)
    if '400' in search_term:
        return HttpResponseBadRequest()
    elif '403' in search_term:
        return HttpResponseForbidden()
    elif '404' in search_term:
        return HttpResponseNotFound()
    elif '405' in search_term:
        return HttpResponseNotAllowed()
    return HttpResponseServerError()


@require_GET
def item(request, pk):
    data = filter(lambda item: text(item['pk']) == text(pk), DATABASE)
    data = map(convert_data, data)
    data = list(data)
    logger.debug('3rd item search: `%s`', pk)
    if not data:
        raise Http404("Unknown item `{}`".format(pk))
    result = {'data': data}
    response = json.dumps(result)
    logger.debug('response: `%s`', response)
    return HttpResponse(response)
