"""
Agnocomplete decorators
"""
from functools import wraps
from django.forms import Form, ModelForm


def allow_create(function):
    """
    Decorate the `form_valid` method in a Create/Update class to create new
    values if necessary.

    .. warning::

        Make sure that this decorator **only** decorates the ``form_valid()``
        method and **only** this one.

    """
    @wraps(function)
    def _wrapped_func(*args, **kwargs):
        form = args[0]
        # If this argument is not a form, there are a lot of chances that
        # you didn't decorate the right method.
        # This decorator is only to be used decorating "form_valid()"
        if isinstance(form, (Form, ModelForm)):
            # If the form is not valid, don't try to create new values
            if not form.is_valid():
                return function(*args, **kwargs)

            for k, field in form.fields.items():
                if getattr(field, 'create', False) \
                        and getattr(field, '_new_values', None):
                    new_values = field.create_new_values()
                    # update the field value
                    form.cleaned_data[k] = form.cleaned_data[k] | new_values

        return function(*args, **kwargs)
    return _wrapped_func
