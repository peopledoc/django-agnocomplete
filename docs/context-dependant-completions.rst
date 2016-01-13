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

    from django import forms
    from agnocomplete.forms import UserContextFormMixin

    class SearchContextForm(UserContextForm, forms.Form):
        search_person = fields.AgnocompleteModelField(
            'AutocompletePersonSameSite')


On the view side
================

Views that take care of the context to handle form display and form process need to be aware that they'll have to carry the user context to the form and that, when the ``POST`` request has to be processed using this context.

We're providing a Mixin named :class:`UserContextFormViewMixin`:

.. code-block:: python

    from agnocomplete.views import UserContextFormViewMixin

    class SearchContextFormView(UserContextFormViewMixin, FormView):
        form_class = SearchContextForm

That's it. The view will pass the context to the fields, and this context will be used by the Agnocomplete field to validate against the queryset.

If the POST data pushed to your form don't comply with the context (e.g., choosing a Category that doesn't belong to the user context), then the ``form.is_valid()`` method will return False.

No need to redeclare the queryset, no need to override the ``clean_<field>()`` method.


Context-dependant multiple selects
==================================

In the :ref:`model-multiple-selection` section, we've seen how to create multiple-select inputs, with or without enabling creation mode. It may happen that we want to create new model instances using the current context. Typically, let's imagine that we're on a multiple-client website, each logged user belongs to their own "domain". Now we want to tag items, but each tag catalog has to be isolated from the others. The tags of the *client A* are not the tags of the *client B*.

Here are our models:

.. code-block:: python

    class ContextTag(models.Model):
        name = models.CharField(max_length=50)
        domain = models.CharField(max_length=100)

    class ArticleContextTag(models.Model):
        article = models.ForeignKey(Article)
        tags = models.ManyToManyField(ContextTag)

Here's the corresponding :class:`ModelForm`

.. code-block:: python

    class ArticleContextTagModelForm(UserContextFormMixin,
                                     forms.ModelForm):
        article = fields.AgnocompleteModelField(AutocompleteArticle)
        tags = ModelMultipleDomainField(
            AutocompleteContextTag,
            create_field="name",
            required=False
        )

        class Meta:
            model = ArticleContextTag
            fields = '__all__'

You may have noticed that we have a dedicated :class:`ModelMultipleDomainField`. This specific field class uses the context passed through the form, and then the fields, to build extra arguments when creating the model instance.

Here's the :class:`ModelMultipleDomainField`:

.. code-block:: python

    class ModelMultipleDomainField(fields.AgnocompleteModelMultipleField):
        def extra_create_kwargs(self):
            """
            Inject the domain of the current user in the new model instances.
            """
            user = self.get_agnocomplete_context()
            if user:
                _, domain = user.email.split('@')
                return {
                    'domain': domain
                }
            return {}

When the field will want to create new records in the :class:`ContextTag` table, here's what's going to happen:

* the "name" will take the value of the string inserted into the input,
* the "domain" will take the value of the current user email domain name.

As a consequence, each tag creation could be written like this:

.. code-block:: python

    ContextTag.objects.create(**{
        'name': input_value,
        'domain': user_domain_name,
    })

Of course, you're free to extract whichever information out of the context (or not) and feed the extra_kwargs dictionary (the date and time, the weather, whatever).

.. important::

    Views that will use the :class:`ArticleContextTagModelForm` **must** inherit from the :class:`UserContextFormViewMixin`, exactly as above, otherwise, the context is not transmitted to the different elements of the view.
