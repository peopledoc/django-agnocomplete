from django.db import models
from django.utils.encoding import force_str

from .common import COLORS


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return " ".join((self.first_name, self.last_name))

    @property
    def is_active(self):
        # Property needed by the authentication backend
        return True

    @property
    def is_authenticated(self):
        return True

    def save(self, *args, **kwargs):
        # Last login is a Django User model specific field,
        # no need to handle it
        if "update_fields" in kwargs:
            if 'last_login' in kwargs['update_fields']:
                kwargs['update_fields'].remove('last_login')
        return super().save(*args, **kwargs)


class FavoriteColor(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    color = models.CharField(max_length=100, choices=COLORS)

    def __str__(self):
        return "{}'s favorite color is {}".format(self.person, self.color)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PersonTag(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return "{} is tagged: {}".format(
            self.person,
            ", ".join([force_str(t) for t in self.tags.all()]) or "Nothing"
        )


class ContextTag(models.Model):
    name = models.CharField(max_length=50)
    domain = models.CharField(max_length=100)

    def __str__(self):
        return "[{}] {}".format(
            self.domain,
            self.name
        )


class PersonContextTag(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    tags = models.ManyToManyField(ContextTag)

    def __str__(self):
        return "{} is tagged: {}".format(
            self.person,
            ", ".join([force_str(t) for t in self.tags.all()]) or "Nothing"
        )
