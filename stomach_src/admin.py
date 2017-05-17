from django.contrib import admin
from .models import Recipe,Ingredient,Ing_Recipe


class IngredientInline(admin.TabularInline):
    model = Ing_Recipe
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,               {'fields': ['name', 'description', 'category','cook_time','person_amount']}),
            ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
                ]
    inlines = [IngredientInline]

admin.site.register(Recipe,RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Ing_Recipe)

# Register your models here.
