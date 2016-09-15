import json

from django.http import HttpResponse, Http404
from django.utils.encoding import force_text as text
from django.views.decorators.http import require_GET

# This is your fake DB
DATABASE = (
    {"pk": 1, 'name': 'first person'},
    {"pk": 2, 'name': 'second person'},
    {"pk": 3, 'name': 'third person'},
    {"pk": 4, 'name': 'fourth person'},
    {"pk": 5, 'name': 'fifth person'},
    {"pk": 6, 'name': 'sixth person'},
    {"pk": 7, 'name': 'seventh person'},
)


def convert_data(item):
    return {'value': item['pk'], 'label': item['name']}


def _search(search_term, convert=True):
    data = []
    if search_term:
        data = filter(lambda x: search_term in x['name'], DATABASE)
    if convert:
        data = map(convert_data, data)
    data = list(data)
    result = {'data': data}
    return result


@require_GET
def simple(request):
    search_term = request.GET.get('q', None)
    result = _search(search_term)
    return HttpResponse(json.dumps(result))


@require_GET
def convert(request):
    search_term = request.GET.get('q', None)
    # Fetching result without converting item JSON payload.
    result = _search(search_term, False)
    return HttpResponse(json.dumps(result))


@require_GET
def item(request, pk):
    data = filter(lambda item: text(item['pk']) == text(pk), DATABASE)
    data = map(convert_data, data)
    data = list(data)
    if not data:
        raise Http404("Unknown item `{}`".format(pk))
    result = {'data': data}
    return HttpResponse(json.dumps(result))
