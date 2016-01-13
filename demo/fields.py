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
