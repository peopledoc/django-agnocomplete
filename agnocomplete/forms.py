from .constants import AGNOCOMPLETE_USER_ATTRIBUTE


class UserContextFormMixin(object):
    """
    Form Mixin that passes the user context to its fields.

    This property takes the name of the ``AGNOCOMPLETE_USER_ATTRIBUTE``
    constant value, to avoid conflicting with any other field property.

    This value will be accessed at validation time, and may only concern
    autocomplete fields that are using context-based querysets
    (e.g.: :class:`AgnocompleteModelField`).
    """
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserContextFormMixin, self).__init__(*args, **kwargs)
        if self.user:
            for field in self.fields.values():
                setattr(field, AGNOCOMPLETE_USER_ATTRIBUTE, self.user)
