from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __unicode__(self):
        return " ".join((self.first_name, self.last_name))
    __str__ = __unicode__
