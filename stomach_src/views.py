from django.shortcuts import *

from django.forms import formset_factory

import stomach_src.utils.stomachDatabaseUtils as DBUtils

from .models import *
from .forms import *


def home(request):
    return render(request, 'html/home.html', {})


def recipes(request):
    recipes_list = Recipe.objects.order_by('-published_date')
    # context is a map with elements of the form (id -> iterable)
    # where the id is the name accessible in html templates.
    context = {'latest_recipes_list': recipes_list}
    # render will replace the python code in the template with whatever you defined.
    return render(request, 'html/recipe/recipe_list.html', context)


def recipe_detail(request, recipe_id):
    context = DBUtils.getRecipeDetails(recipe_id, request.user.id)
    return render(request, 'html/recipe/recipe_detail.html', context)

def recipe_user(request):
    userRecipes = Creator_Recipe.objects.filter(creator_ID=request.user.id).values_list('recipe_ID', flat=True)
    recipes = Recipe.objects.filter(pk__in=set(userRecipes))
    context = {'latest_recipes_list': recipes}
    # render will replace the python code in the template with whatever you defined.
    return render(request, 'html/recipe/recipe_list.html', context)

def recipe_new(request):
    if request.method == "POST":
        DBUtils.createNewRecipe(request)
        message = "Thanks, new recipe added"
        context = {'success': message}
        return render(request,
                      'html/recipe/recipe_edit.html',
                      context)
    else:
        if request.user.is_authenticated:
            recipeForm = RecipeForm()
            ingredientFormSet = formset_factory(IngredientForm)
            categoryFormSet = formset_factory(CategoryForm)
            context = {'form': recipeForm, 'ingredientFormset': ingredientFormSet, 'categoryFormset': categoryFormSet,
                       'edit': False}
            return render(request,
                          'html/recipe/recipe_edit.html',
                          context)
        else:
            recipes_list = Recipe.objects.order_by('-published_date')
            message = "Only logged in users can create new recipes."
            context = {'notAuthorized': message, 'latest_recipes_list': recipes_list}
            return render(request, 'html/recipe/recipe_list.html', context)

def recipe_edit(request, recipe_id):
    recipecontext = DBUtils.getRecipeDetails(recipe_id, request.user.id)
    recipe = recipecontext['recipe']
    ingredients = recipecontext['ingredients']
    categories = recipecontext['categories']
    public = recipecontext['isPublic']

    if request.method == "POST":
        Recipe.objects.filter(id=recipe_id).delete()
        DBUtils.createNewRecipe(request)
        message = "Thanks, your recipe was edited"
        context = {'success': message}

        return render(request,
                      'html/recipe/recipe_edit.html',
                      context)
    else:
        ingredientFormSet = formset_factory(IngredientForm, extra=0)
        categoryFormSet = formset_factory(CategoryForm, extra=0)

        filledRecipe = RecipeForm(
            initial={'name': recipe.name, 'description': recipe.description, 'cook_time': recipe.cook_time,
                     'person_amount': recipe.person_amount, 'public': public})
        filledIng = ingredientFormSet(
            initial=[{'unit': x.unit, 'name': x.ing_ID, 'amount': x.amount} for x in ingredients])
        filledCategories = categoryFormSet(initial=[{'category': x.category_ID} for x in categories])

        context = {'form': filledRecipe, 'ingredientFormset': filledIng, 'categoryFormset': filledCategories,
                   'edit': True}

        return render(request,
                      'html/recipe/recipe_edit.html',
                      context)

def recipe_delete(request, recipe_id):
    Recipe.objects.filter(id=recipe_id).delete()
    return recipes(request)
