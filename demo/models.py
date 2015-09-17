from django.db import models
from .common import COLORS


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __unicode__(self):
        return " ".join((self.first_name, self.last_name))
    __str__ = __unicode__


class FavoriteColor(models.Model):
    person = models.ForeignKey(Person)
    color = models.CharField(max_length=100, choices=COLORS)

    def __unicode__(self):
        return "{}'s favorite color is {}".format(self.person, self.color)
    __str__ = __unicode__
