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

In this example, you're not allowed to create new "tag" values. You would only be able to select previously created tag items.
