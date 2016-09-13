import json

from django.http import HttpResponse
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


@require_GET
def simple(request):
    search_term = request.GET.get('q', None)
    data = []
    if search_term:
        raw = filter(lambda x: search_term in x['name'], DATABASE)
        for item in raw:
            data.append({'value': item['pk'], 'label': item['name']})
    result = {'data': data}
    return HttpResponse(json.dumps(result))
