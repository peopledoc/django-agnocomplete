"""
The different agnocomplete classes to be discovered
"""
from copy import copy

from django.db.models import Q
from django.utils.encoding import force_text as text
from django.conf import settings

from .constants import AGNOCOMPLETE_DEFAULT_PAGESIZE
from .constants import AGNOCOMPLETE_MIN_PAGESIZE
from .constants import AGNOCOMPLETE_MAX_PAGESIZE


def load_settings_sizes():
    """
    Load sizes from settings or fallback to the module constants
    """
    page_size = AGNOCOMPLETE_DEFAULT_PAGESIZE
    settings_page_size = getattr(
        settings, 'AGNOCOMPLETE_DEFAULT_PAGESIZE', None)
    page_size = settings_page_size or page_size

    page_size_min = AGNOCOMPLETE_MIN_PAGESIZE
    settings_page_size_min = getattr(
        settings, 'AGNOCOMPLETE_MIN_PAGESIZE', None)
    page_size_min = settings_page_size_min or page_size_min

    page_size_max = AGNOCOMPLETE_MAX_PAGESIZE
    settings_page_size_max = getattr(
        settings, 'AGNOCOMPLETE_MAX_PAGESIZE', None)
    page_size_max = settings_page_size_max or page_size_max

    return (page_size, page_size_min, page_size_max)


class AgnocompleteBase(object):
    """
    Base class for Agnocomplete tools.
    """
    # To be overridden by settings, or constructor arguments
    page_size = None
    page_size_max = None
    page_size_min = None

    def __init__(self, page_size=None):
        # Load from settings or fallback to constants
        settings_page_size, settings_page_size_min, settings_page_size_max = \
            load_settings_sizes()
        # Use the class attributes or fallback to settings
        self._conf_page_size = self.page_size or settings_page_size
        self._conf_page_size_min = self.page_size_min or settings_page_size_min
        self._conf_page_size_max = self.page_size_max or settings_page_size_max

        # Use instance constructor parameters to eventually override defaults
        page_size = page_size or self._conf_page_size
        if page_size > self._conf_page_size_max \
                or page_size < self._conf_page_size_min:
            page_size = self._conf_page_size
        # Finally set this as the wanted page_size
        self._page_size = page_size

    def get_page_size(self):
        """
        Return the computed page_size

        It takes into account:

        * constructor arguments,
        * settings
        * fallback to the module constants if needed.

        """
        return self._page_size

    def get_choices(self):
        raise NotImplementedError(
            "Developer: your class needs at least a 'get_choices()' method")

    def items(self, query=None):
        raise NotImplementedError(
            "Developer: Your class needs at least a items() method")

    def selected(self, ids):
        """
        Return the values (as a tuple of pairs) for the ids provided
        """
        raise NotImplementedError(
            "Developer: Your class needs at least a selected() method")

    @property
    def name(self):
        return self.__class__.__name__


class AgnocompleteChoices(AgnocompleteBase):
    """
    Usage Example::

        class AgnocompleteColor(AgnocompleteChoices):
            choices = ['red', 'green', 'blue']

    """
    choices = []

    def get_choices(self):
        return tuple(zip(self.choices, self.choices))

    def items(self, query=None):
        if not query:
            return []
        result = copy(self.choices)
        if query:
            result = tuple(filter(lambda x: x.startswith(query), result))

        result = [dict(value=item, label=item) for item in result]
        return result[:self.get_page_size()]

    def selected(self, ids):
        """
        Return the selected options as a list of tuples
        """
        result = copy(self.choices)
        result = filter(lambda x: x in ids, result)
        result = ((item, item) for item in result)
        return list(result)


class AgnocompleteModel(AgnocompleteBase):
    """

    Example::

        class AgnocompletePeople(AgnocompleteModel):
            model = People
            fields = ['first_name', 'last_name']

    """

    @property
    def model(self):
        raise NotImplementedError(
            "Integrator: You must have a `model` property")

    @property
    def fields(self):
        raise NotImplementedError(
            "Integrator: You must have a `fields` property")

    def _construct_qs_filter(self, field_name):
        """
        Using a field name optionnaly prefixed by `^`, `=`, `@`, return a
        case-insensitive filter condition name usable as a queryset `filter()`
        keyword argument.
        """
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__iexact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    def get_model_queryset(self):
        return self.model.objects.all()
    get_choices = get_model_queryset

    def get_queryset(self, query=None):
        """
        Return the filtered queryset
        """
        # Cut this, we don't need no empty query
        if not query:
            return self.model.objects.none()

        qs = self.get_model_queryset()
        conditions = Q()
        for field_name in self.fields:
            conditions |= Q(**{
                self._construct_qs_filter(field_name): query
            })
        qs = qs.filter(conditions)
        return qs

    def items(self, query=None):
        """
        Return the items to be sent to the client
        """
        # Cut this, we don't need no empty query
        if not query:
            return self.model.objects.none()
        qs = self.get_queryset(query)
        result = []
        for item in qs:
            result.append({
                "value": text(item.pk),
                "label": text(item)
            })
        return result[:self.get_page_size()]

    def selected(self, ids):
        """
        Return the selected options as a list of tuples
        """
        # cleanup the id list
        ids = filter(lambda x: "{}".format(x).isdigit(), copy(ids))
        # Prepare the QS
        qs = self.get_model_queryset().filter(pk__in=ids)
        result = []
        for item in qs:
            result.append(
                (text(item.pk), text(item))
            )
        return result
