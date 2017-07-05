"""
Custom fields
"""
from agnocomplete import fields


class ModelMultipleDomainField(fields.AgnocompleteModelMultipleField):
    """
    Demo field with context injection
    """
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


class ModelMultipleObjectsField(fields.AgnocompleteModelMultipleField):
    """
    Demo field with a create method that allows duplicates
    """
    def create_item(self, **kwargs):
        """
        Return the created model instance.
        """
        return self.queryset.model.objects.create(**kwargs)
