from django.contrib import admin
from .models import Person, FavoriteColor


class PersonAdmin(admin.ModelAdmin):
    pass


class FavoriteColorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Person, PersonAdmin)
admin.site.register(FavoriteColor, FavoriteColorAdmin)
