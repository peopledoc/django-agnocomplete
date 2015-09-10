"""
The different agnocomplete classes to be discovered
"""
from copy import copy

from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text as text
from django.conf import settings

from .constants import AGNOCOMPLETE_DEFAULT_PAGESIZE
from .constants import AGNOCOMPLETE_MIN_PAGESIZE
from .constants import AGNOCOMPLETE_MAX_PAGESIZE
from .constants import AGNOCOMPLETE_DEFAULT_QUERYSIZE
from .constants import AGNOCOMPLETE_MIN_QUERYSIZE
from .exceptions import AuthenticationRequiredAgnocompleteException


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

    # Query sizes
    query_size = AGNOCOMPLETE_DEFAULT_QUERYSIZE
    settings_query_size = getattr(
        settings, 'AGNOCOMPLETE_DEFAULT_QUERYSIZE', None)
    query_size = settings_query_size or query_size

    query_size_min = AGNOCOMPLETE_MIN_QUERYSIZE
    settings_query_size_min = getattr(
        settings, 'AGNOCOMPLETE_MIN_QUERYSIZE', None)
    query_size_min = settings_query_size_min or query_size_min

    return (
        page_size, page_size_min, page_size_max,
        query_size, query_size_min,
    )


class AgnocompleteBase(object):
    """
    Base class for Agnocomplete tools.
    """
    # To be overridden by settings, or constructor arguments
    page_size = None
    page_size_max = None
    page_size_min = None
    query_size = None
    query_size_min = None

    def __init__(self, user=None, page_size=None):
        # Loading the user context
        self.user = user

        # Load from settings or fallback to constants
        settings_page_size, settings_page_size_min, settings_page_size_max, \
            query_size, query_size_min = load_settings_sizes()

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

        # set query sizes
        self._query_size = self.query_size or query_size
        self._query_size_min = self.query_size_min or query_size_min

    def get_page_size(self):
        """
        Return the computed page_size

        It takes into account:

        * class variables
        * constructor arguments,
        * settings
        * fallback to the module constants if needed.

        """
        return self._page_size

    def get_query_size(self):
        """
        Return the computed default query size

        It takes into account:

        * class variables
        * settings,
        * fallback to the module constants
        """
        return self._query_size

    def get_query_size_min(self):
        """
        Return the computed minimum query size

        It takes into account:

        * class variables
        * settings,
        * fallback to the module constants
        """
        return self._query_size_min

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
            choices = (
                ('red', 'Red'),
                ('green', 'Green'),
                ('blue', 'Blue'),
            )

    """
    choices = ()

    def get_choices(self):
        return self.choices

    def items(self, query=None):
        if not query:
            return []
        result = copy(self.choices)
        if query:
            result = filter(lambda x: x[1].lower().startswith(query), result)
            result = tuple(result)

        result = [dict(value=value, label=label) for value, label in result]
        return result[:self.get_page_size()]

    def selected(self, ids):
        """
        Return the selected options as a list of tuples
        """
        result = copy(self.choices)
        result = filter(lambda x: x[0] in ids, result)
        # result = ((item, item) for item in result)
        return list(result)


class AgnocompleteModelBase(AgnocompleteBase):
    model = None
    requires_authentication = False

    def get_queryset(self):
        raise NotImplementedError(
            "Integrator: You must either have a `model` property "
            "or a `get_queryset()` method"
        )

    @property
    def fields(self):
        raise NotImplementedError(
            "Integrator: You must have a `fields` property")

    def get_model(self):
        """
        Return the class Model used by this Agnocomplete
        """
        if hasattr(self, 'model') and self.model:
            return self.model
        # Give me a "none" queryset
        try:
            none = self.get_queryset().none()
            return none.model
        except:
            raise ImproperlyConfigured(
                "Integrator: Unable to determine the model with this queryset."
                " Please add a `model` property")

    def get_model_queryset(self):
        """
        Return an unfiltered complete model queryset.

        To be used for the select Input initialization
        """
        return self.get_model().objects.all()
    get_choices = get_model_queryset


class AgnocompleteModel(AgnocompleteModelBase):
    """
    Example::

        class AgnocompletePeople(AgnocompleteModel):
            model = People
            fields = ['first_name', 'last_name']

        class AgnocompletePersonQueryset(AgnocompleteModel):
            fields = ['first_name', 'last_name']

            def get_queryset(self):
                return People.objects.filter(email__contains='example.com')

    """
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

    def get_queryset(self):
        if not hasattr(self, 'model') or not self.model:
            raise NotImplementedError(
                "Integrator: You must either have a `model` property "
                "or a `get_queryset()` method"
            )
        return self.model.objects.all()

    def get_queryset_filters(self, query):
        """
        Return the filtered queryset
        """
        conditions = Q()
        for field_name in self.fields:
            conditions |= Q(**{
                self._construct_qs_filter(field_name): query
            })
        return conditions

    def items(self, query=None):
        """
        Return the items to be sent to the client
        """
        # Cut this, we don't need no empty query
        if not query:
            return self.get_model().objects.none()

        if self.requires_authentication:
            if not self.user:
                raise AuthenticationRequiredAgnocompleteException(
                    "Authentication is required to use this autocomplete"
                )
            if not self.user.is_authenticated():
                raise AuthenticationRequiredAgnocompleteException(
                    "Authentication is required to use this autocomplete"
                )

        # Take the basic queryset
        qs = self.get_queryset()
        # filter it via the query conditions
        qs = qs.filter(self.get_queryset_filters(query))
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
        # TODO: not contextually filtered, check if it's possible at some point
        qs = self.get_model_queryset().filter(pk__in=ids)
        result = []
        for item in qs:
            result.append(
                (text(item.pk), text(item))
            )
        return result
