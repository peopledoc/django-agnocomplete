import json
import logging

from django.http import HttpResponse, Http404
from django.utils.encoding import force_text as text
from django.views.decorators.http import require_GET

from . import DATABASE

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


def _search(search_term, convert_func):
    data = []
    if search_term:
        data = filter(lambda x: search_term in x['name'], DATABASE)
    if data and convert_func:
        data = map(convert_func, data)
    data = list(data)
    result = {'data': data}
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
