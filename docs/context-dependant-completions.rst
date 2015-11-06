=============================
Context-dependant completions
=============================

There's a common usecase: "Please display the items depending on the user context".

In a multi-site context, you **have** to define a preemptive filter to gather informations based on the current context. **And** you also have to validate form data against this context. A malevolent user could forge a POST request with a data field that would be off-context.

On the Autocomplete class side
==============================

That's the reason why the ``django-agnocomplete`` views carry the request user into the Autocomplete class. This instance variable is ``self.user``. If you're using a custom authentication profile, it'll be an instance of your ``AUTH_USER_MODE`` class, hence it'll have access to its properties and methods.

.. code-block:: python

    class AutocompletePersonQueryset(AgnocompleteModel):
        fields = ['first_name', 'last_name']
        requires_authentication = True
        model = Person

        def get_queryset(self):
            email = self.user.email
            _, domain = email.split('@')
            return Person.objects.filter(email__endswith=domain)

    class AutocompletePersonSameSite(AgnocompleteModel):
        fields = ['first_name', 'last_name']
        requires_authentication = True
        model = Person

        def get_queryset(self):
            return Person.objects.filter(site=self.user.site)

.. important::

    You may have noticed that these two classes have a ``model`` property and a ``requires_authentication`` property set to ``True``. Because we're using a user-based context, the ``requires_authentication`` will allow the general "out-of-context code" (form class creation) to instanciate the Agnocomplete class without the context, but will disallow it to return results based on the ``query``. This way, you can filter out unauthorized uses of the autocomplete, as you could do it with the ``@login_required`` decorator in
    your views.

On the Form side
================

Nothing special to do. Just declare your fields exactly the same way.

.. code-block:: python

    class SearchContextForm(UserContextForm):
        search_person = fields.AgnocompleteModelField(
            'AutocompletePersonSameSite')


On the view side
================

Views that take care of the context to handle form display and form process need to be aware that they'll have to carry the user context to the form and that, when the ``POST`` request has to be processed using this context.

We're providing a Mixin named :class:`UserContextFormMixin`:

.. code-block:: python

    class SearchContextFormView(UserContextFormMixin, FormView):
        form_class = SearchContextForm

That's it. The view will pass the context to the fields, and this context will be used by the Agnocomplete field to validate against the queryset.

If the POST data pushed to your form don't comply with the context (e.g., choosing a Category that doesn't belong to the user context), then the ``form.is_valid()`` method will return False.

No need to redeclare the queryset, no need to override the ``clean_<field>()`` method.
