==================
Fields and Widgets
==================

If you're using the "stock" agnocomplete fields, they'll cover your general usage. The default autocomplete widget is :class:`agnocomplete.widgets.AgnocompleteSelect`. It's a normal Select widget, with autocomplete-super-powers.

The jquery-autocomplete case
============================

For some reasons, you can't use a regular ``<select>`` with ``jquery-autocomplete``, it must be a classic text input. We're providing the :class:`agnocomplete.widgets.AgnocompleteTextInput`. If you need to use select2 (or any other library that can't support regular select boxes), you're describing your autocomplete field using the regular :class:`AgnocompleteChoices` or :class:`AgnocompleteModel` class, and you simply use the wanted widget that overrides the default.

Example extracted from the demo site:

.. code-block:: python

    class SearchFormTextInput(forms.Form):
        search_color = fields.AgnocompleteField(
            AutocompleteColor, widget=widgets.AgnocompleteTextInput)
        search_person = fields.AgnocompleteModelField(
            AutocompletePerson, widget=widgets.AgnocompleteTextInput)

Multiple selection
==================

You may need to implement a multiple selection with autocompletion (one common case is for tagging documents, articles, etc).

The designated field for this feature is :class:`agnocomplete.fields.AgnocompleteMultipleField`. It has to modes: with or without "create".

If you allow the user to add *new* values in the autocomplete, you should provide the ``create`` argument set to ``True``. Otherwise, all the values to be selected are bound to the list of source values.

Usage example:

.. code-block:: python

    class SearchColorMulti(forms.Form):
        search_multi_color = fields.AgnocompleteMultipleField(
            AutocompleteColorShort)
        search_multi_color_create = fields.AgnocompleteMultipleField(
            AutocompleteColorShort,
            create=True,
        )

In the first field, the user can type ahead *"gre"* to see suggestions like *"green"* or *"grey"*, but won't be able to add "green yellow" suggestion, since it's not in the ``demo.common.COLORS`` list.

In the second field, the users can use the search feature to look after "green" or "grey" suggestions, but also can add values of their own ; values that will be transmitted when the form is submitted.

It's the backend responsability to handle these values when the view will receive the submitted form.

.. _model-multiple-selection:

Model Multiple Selection
========================

The field :class:`agnocomplete.fields.AgnocompleteModelMultipleField` supports the multiselection based on models, like this:

.. code-block:: python

    class TagModelForm(forms.ModelForm):
        person = fields.AgnocompleteModelField(AutocompletePersonShort)
        tags = fields.AgnocompleteModelMultipleField(AutocompleteTag)

        class Meta:
            model = PersonTag
            fields = '__all__'

In this example, you're not allowed to create new "tag" values. You would only be able to select previously created tag items in your "tag table".

Creation mode for Model Multiple Selectors
------------------------------------------

The "create" mode with model-based fields is a bit different from the regular one. At the moment, ``agnocomplete`` is supporting a "one-field-model instance creation" only. And there are no plans yet to upgrade this.

Here is the reason why: in your interface, you can search for one string, for example: "hello" and either this string corresponds to a known value in your database or not. This string is your "identifier" on the front-end that you'll pass to your backend to create a new item if this one doesn't exist yet. This will just work for small models, like :class:`Tag`s. A primary key, a name, and that's it. If the tag name you're typing in your search field is unknown, your backend will be able to perform a basic Django creation like this:

.. code-block:: python

    Tag.objects.create(name='the-tag-i-ve-searched')

If you have more than one field, you won't be able to provide their values in your UI. If your :class:`Tag` model has more than one field (example: ``is_active`` or ``color``), you **must** provide a default value for them.

Example
~~~~~~~

In this example we're using the :class:`Tag` model defined in ``demo.models``.
You can see that we're not providing a `create` argument for the :class:`AgnocompleteModelMultipleField`, but a ``create_field`` argument. This value is the field that will receive the new values.

.. code-block:: python

    class PersonTagModelFormWithCreate(PersonTagModelForm):
        person = fields.AgnocompleteModelField(AutocompletePersonShort)
        tags = fields.AgnocompleteModelMultipleField(
            AutocompleteTag,
            create_field="name"
        )

        class Meta:
            model = PersonTag
            fields = '__all__'

We're half way here: the view needs to know that, when the form & fields will be validated, it must add the new values inserted into the database.

.. code-block:: python

    from django.utils.decorators import method_decorator

    class PersonTagModelViewWithCreate(PersonTagModelView):
        form_class = PersonTagModelFormWithCreate

        @method_decorator(allow_create)
        def form_valid(self, form):
            return super(PersonTagModelViewWithCreate, self).form_valid(form)

.. important::

    You **must** override ``form_valid()``, there's no other method that will guarantee that these new values will be added to the database **and** linked to the current record.

    We know... it doesn't look very elegant.
