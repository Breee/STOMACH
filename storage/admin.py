from django.contrib import admin
from storage.models import *


class IngredientInline(admin.TabularInline):
    model = Storage_Ingredient


class StorageAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,               {'fields': ['name','visible']}),
                ]
    inlines = [IngredientInline]

admin.site.register(Storage,StorageAdmin)
admin.site.register(Storage_Ingredient)