"""
The different agnocomplete classes to be discovered
"""
from copy import copy
from six import with_metaclass
from abc import abstractmethod, ABCMeta
import logging

from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_str as text
from django.conf import settings
import requests

from .constants import AGNOCOMPLETE_DEFAULT_PAGESIZE
from .constants import AGNOCOMPLETE_MIN_PAGESIZE
from .constants import AGNOCOMPLETE_MAX_PAGESIZE
from .constants import AGNOCOMPLETE_DEFAULT_QUERYSIZE
from .constants import AGNOCOMPLETE_MIN_QUERYSIZE
from .exceptions import AuthenticationRequiredAgnocompleteException
from .exceptions import SkipItem
from .exceptions import ItemNotFound


logger = logging.getLogger(__name__)


class ClassPropertyDescriptor(object):
    """
    Toolkit class used to instanciate a class property.
    """
    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        """
        Setter: the decorated method will become a class property.
        """
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    """
    Decorator: the given function will become a class property.

    e.g::

        class SafeClass(object):

            @classproperty
            def safe(cls):
                return True

        class UnsafeClass(object):

            @classproperty
            def safe(cls):
                return False

    """
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)


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


class AgnocompleteBase(with_metaclass(ABCMeta, object)):
    """
    Base class for Agnocomplete tools.
    """

    # To be overridden by settings, or constructor arguments
    page_size = None
    page_size_max = None
    page_size_min = None
    query_size = None
    query_size_min = None
    url = None

    def __init__(self, user=None, page_size=None, url=None):
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

        # Eventual custom URL
        self._url = url

    def set_agnocomplete_field(self, field):
        self.agnocomplete_field = field

    @classproperty
    def slug(cls):
        """
        Return the key used in the register, used as a slug for the URL.

        You can override this by adding a class property.
        """
        return cls.__name__

    def get_url(self):
        return self._url or self.url

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

    @abstractmethod
    def get_choices(self):
        pass

    @abstractmethod
    def items(self, query=None, **kwargs):
        pass

    @abstractmethod
    def selected(self, ids):
        """
        Return the values (as a tuple of pairs) for the ids provided
        """
        pass

    def is_valid_query(self, query):
        """
        Return True if the search query is valid.

        e.g.:
        * not empty,
        * not too short,
        """
        # No query, no item
        if not query:
            return False
        # Query is too short, no item
        if len(query) < self.get_query_size_min():
            return False
        return True


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

    def item(self, current_item):
        value, label = current_item
        return dict(value=value, label=label)

    def items(self, query=None, **kwargs):
        if not self.is_valid_query(query):
            return []

        result = copy(self.choices)
        if query:
            result = filter(lambda x: x[1].lower().startswith(query), result)
            result = tuple(result)

        # Slicing before rendering
        result = result[:self.get_page_size()]
        return [self.item(item) for item in result]

    def selected(self, ids):
        """
        Return the selected options as a list of tuples
        """
        result = copy(self.choices)
        result = filter(lambda x: x[0] in ids, result)
        # result = ((item, item) for item in result)
        return list(result)


class AgnocompleteModelBase(with_metaclass(ABCMeta, AgnocompleteBase)):

    model = None
    requires_authentication = False

    @abstractmethod
    def get_queryset(self):
        pass

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
        except Exception:
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

    def get_field_name(self):
        """
        Return the model field name to be used as a value, or 'pk' if unset
        """
        if hasattr(self, 'agnocomplete_field') and \
           hasattr(self.agnocomplete_field, 'to_field_name'):
            return self.agnocomplete_field.to_field_name or 'pk'
        return 'pk'


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

    def __init__(self, *args, **kwargs):
        super(AgnocompleteModel, self).__init__(*args, **kwargs)
        self.__final_queryset = None

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

    def paginate(self, qs):
        """
        Paginate a given Queryset
        """
        return qs[:self.get_page_size()]

    @property
    def _final_queryset(self):
        """
        Paginated final queryset
        """
        if self.__final_queryset is None:
            return None
        return self.paginate(self.__final_queryset)
    # final_queryset alias
    final_queryset = _final_queryset

    @property
    def final_raw_queryset(self):
        return self.__final_queryset

    def serialize(self, queryset):
        result = []
        for item in self.paginate(queryset):
            result.append(self.item(item))
        return result

    def item(self, current_item):
        """
        Return the current item.

        @param current_item: Current item
        @type  param: django.models

        @return: Value and label of the current item
        @rtype : dict
        """
        return {
            'value': text(getattr(current_item, self.get_field_name())),
            'label': self.label(current_item)
        }

    def label(self, current_item):
        """
        Return a label for the current item.

        @param current_item: Current item
        @type  param: django.models

        @return: Label of the current item
        @rtype : text
        """
        return text(current_item)

    def build_extra_filtered_queryset(self, queryset, **kwargs):
        """
        Apply eventual queryset filters, based on the optional extra arguments
        passed to the query.

        By default, this method returns the queryset "verbatim". You can
        override or overwrite this to perform custom filter on this QS.

        * `queryset`: it's the final queryset build using the search terms.
        * `kwargs`: this dictionary contains the extra arguments passed to the
          agnocomplete class.
        """
        # By default, we're ignoring these arguments and return verbatim QS
        return queryset

    def build_filtered_queryset(self, query, **kwargs):
        """
        Build and return the fully-filtered queryset
        """
        # Take the basic queryset
        qs = self.get_queryset()
        # filter it via the query conditions
        qs = qs.filter(self.get_queryset_filters(query))
        return self.build_extra_filtered_queryset(qs, **kwargs)

    def items(self, query=None, **kwargs):
        """
        Return the items to be sent to the client
        """
        # Cut this, we don't need no empty query
        if not query:
            self.__final_queryset = self.get_model().objects.none()
            return self.serialize(self.__final_queryset)
        # Query is too short, no item
        if len(query) < self.get_query_size_min():
            self.__final_queryset = self.get_model().objects.none()
            return self.serialize(self.__final_queryset)

        if self.requires_authentication:
            if not self.user:
                raise AuthenticationRequiredAgnocompleteException(
                    "Authentication is required to use this autocomplete"
                )
            if not self.user.is_authenticated:
                raise AuthenticationRequiredAgnocompleteException(
                    "Authentication is required to use this autocomplete"
                )

        qs = self.build_filtered_queryset(query, **kwargs)
        # The final queryset is the paginated queryset
        self.__final_queryset = qs
        return self.serialize(qs)

    def selected(self, ids):
        """
        Return the selected options as a list of tuples
        """
        # Cleanup the ID list
        if self.get_field_name() == 'pk':
            ids = filter(lambda x: "{}".format(x).isdigit(), copy(ids))
        else:
            ids = filter(lambda x: len("{}".format(x)) > 0, copy(ids))
        # Prepare the QS
        # TODO: not contextually filtered, check if it's possible at some point
        qs = self.get_model_queryset().filter(
            **{'{}__in'.format(self.get_field_name()): ids})
        result = []
        for item in qs:
            item_repr = self.item(item)
            result.append(
                (item_repr['value'], item_repr['label'])
            )
        return result


class AgnocompleteUrlProxy(with_metaclass(ABCMeta, AgnocompleteBase)):
    """
    This class serves as a proxy between your application and a 3rd party
    URL (typically a REST HTTP API).
    """
    value_key = 'value'
    label_key = 'label'
    method = 'get'
    data_key = 'data'

    def get_search_url(self):
        raise NotImplementedError(
            "Integrator: You must implement a `get_search_url` method"
            " or have a `search_url` property in this class.")

    @property
    def search_url(self):
        return self.get_search_url()

    def get_item_url(self, pk):
        raise NotImplementedError(
            "Integrator: You must implement a `get_item_url` method")

    def get_choices(self):
        return []

    def get_http_method_arg_name(self):
        """
        Return the HTTP function to call and the params/data argument name
        """
        if self.method == 'get':
            arg_name = 'params'
        else:
            arg_name = 'data'
        return getattr(requests, self.method), arg_name

    def http_call(self, url=None, **kwargs):
        """
        Call the target URL via HTTP and return the JSON result
        """
        if not url:
            url = self.search_url
        http_func, arg_name = self.get_http_method_arg_name()
        # Build the argument dictionary to pass in the http function
        _kwargs = {
            arg_name: kwargs,
        }
        # The actual HTTP call
        response = http_func(
            url=url.format(**kwargs),
            headers=self.get_http_headers(),
            **_kwargs
        )
        # Error handling
        if response.status_code != 200:
            logger.warning('Invalid Request for `%s`', response.url)
            # Raising a "requests" exception
            response.raise_for_status()
        return response.json()

    def item(self, current_item):
        return dict(
            value=text(current_item[self.value_key]),
            label=text(current_item[self.label_key]),
        )

    def get_http_headers(self):
        """
        Return a dictionary that will be added to the HTTP request to the API

        You can overwrite this method, that return an empty dict by default.
        """
        return {}

    def get_http_result(self, http_result):
        """
        Return an iterable with all the result items in.

        You can override/overwrite this method to adapt it to the payload
        returned by the 3rd party API.
        """
        return http_result.get(self.data_key, [])

    def get_http_call_kwargs(self, query, **kwargs):
        """
        Return the HTTP query arguments.

        You can override this method to pass further arguments corresponding
        to your search_url.
        """
        return {'q': query}

    def items(self, query=None, **kwargs):
        if not self.is_valid_query(query):
            return []
        # Call to search URL
        http_result = self.http_call(
            **self.get_http_call_kwargs(query, **kwargs)
        )
        # In case of error, on the API side, the error is raised and handled
        # in the view.
        http_result = self.get_http_result(http_result)
        result = []
        for item in http_result:
            # Eventual result reshaping.
            try:
                result.append(self.item(item))
            except SkipItem:
                continue
        return result

    def selected(self, ids):
        data = []
        # Filter out "falsy IDs" (empty string, None, 0...)
        ids = filter(lambda x: x, ids)
        for _id in ids:
            if _id:
                # Call to the item URL
                result = self.http_call(url=self.get_item_url(pk=_id))
                if self.data_key in result and len(result[self.data_key]):
                    for item in result[self.data_key]:
                        data.append(
                            (
                                text(item[self.value_key]),
                                text(item[self.label_key])
                            )
                        )
        return data

    def validate(self, value):
        """
        From a value available on the remote server, the method returns the
        complete item matching the value.
        If case the value is not available on the server side or filtered
        through :meth:`item`, the class:`agnocomplete.exceptions.ItemNotFound`
        is raised.
        """

        url = self.get_item_url(value)
        try:
            data = self.http_call(url=url)
        except requests.HTTPError:
            raise ItemNotFound()

        data = self.get_http_result(data)

        try:
            self.item(data)
        except SkipItem:
            raise ItemNotFound()

        return value
