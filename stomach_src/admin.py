from django.contrib import admin
from .models import Recipe
from .models import Ingredient
from .models import Ing_Recipe
from .models import Category
from .models import Category_Recipe
from .models import Tag
from .models import Tag_Recipe
from .models import Unit




class IngredientInline(admin.TabularInline):
    model = Ing_Recipe

class CategoryInline(admin.TabularInline):
    model = Category_Recipe

class TagInline(admin.TabularInline):
    model = Tag_Recipe


class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,               {'fields': ['name', 'description', 'cook_time','person_amount']}),
            ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
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