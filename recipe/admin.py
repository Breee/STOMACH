from django.contrib import admin
from recipe.models import *


class IngredientInline(admin.TabularInline):
    model = Ing_Recipe

class CategoryInline(admin.TabularInline):
    model = Category_Recipe

class TagInline(admin.TabularInline):
    model = Tag_Recipe


class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,               {'fields': ['name', 'description', 'cook_time','person_amount','visible']}),
            ('Date information', {'fields': ['published_date'], 'classes': ['collapse']}),
                ]
    inlines = [IngredientInline,TagInline,CategoryInline]

admin.site.register(Recipe,RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Ing_Recipe)
admin.site.register(Category_Recipe)
admin.site.register(Tag_Recipe)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(User_Recipe)
admin.site.register(Creator_Recipe)