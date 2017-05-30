from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import *

import utils.stomachDatabaseUtils as DBUtils
from .forms import *

"""
#########################################################
################### Recipe Views ########################
#########################################################
"""


def recipes_list(request, message=""):
    # get all public recipes
    public_recipes = Creator_Recipe.objects.filter(public=True).values_list('recipe_ID')
    # get all user recipes
    user_recipes = DBUtils.get_user_recipes(request).values_list('id')
    # union public and user recipes
    public_user = public_recipes.union(user_recipes)
    recipe_list = Recipe.objects.filter(pk__in=public_user, visible=True).order_by('-published_date').filter(
        visible=True)
    # context is a map with elements of the form (id -> iterable)
    # where the id is the name accessible in html templates.
    context = {'latest_recipes_list': recipe_list, "message": message}
    # render will replace the python code in the template with whatever you defined.
    return render(request,
                  'html/recipe/recipe_list.html',
                  context)


def recipe_detail(request, recipe_id):
    context = DBUtils.get_recipe_details(recipe_id, request.user.id)
    if context is None:
        return not_authorized()

    return render(request,
                  'html/recipe/recipe_detail.html',
                  context)


@login_required
def recipes_user(request):
    recipes = DBUtils.get_user_recipes(request)
    context = {'recipes': recipes}
    return render(request,
                  'html/recipe/recipes_user.html',
                  context)

@login_required()
def recipe_new(request):
    if request.method == "POST":
        DBUtils.create_new_recipe(request)
        message = "Thanks, new recipe added"
        context = {'success': message}
        return render(request,
                      'html/recipe/recipe_edit.html',
                      context)
    else:
        if request.user.is_authenticated:
            recipeForm = RecipeForm()
            ingredientFormSet = formset_factory(IngredientForm, extra=1)
            categoryFormSet = formset_factory(CategoryForm, extra=1)
            context = {
                'form': recipeForm, 'ingredientFormset': ingredientFormSet, 'categoryFormset': categoryFormSet,
                'edit': False
            }
            return render(request,
                          'html/recipe/recipe_edit.html',
                          context)
        else:
            recipes_list = Recipe.objects.order_by('-published_date').filter(visible=True)
            message = "Only logged in users can create new recipes."
            context = {'notAuthorized': message, 'latest_recipes_list': recipes_list}
            return render(request,
                          'html/recipe/recipe_list.html',
                          context)

@login_required()
def recipe_edit(request, recipe_id):
    recipecontext = DBUtils.get_recipe_details(recipe_id, request.user.id)
    if recipecontext == None or recipecontext['userIsCreator'] == False:
        return not_authorized()

    recipe = recipecontext['recipe']
    ingredients = recipecontext['ingredients']
    categories = recipecontext['categories']
    public = recipecontext['isPublic']

    if request.method == "POST":
        DBUtils.hide_recipe(recipe_id)
        DBUtils.create_new_recipe(request)
        message = "Thanks, your recipe was edited"
        context = {'success': message}

        return render(request,
                      'html/recipe/recipe_edit.html',
                      context)
    else:
        ingredientFormSet = formset_factory(IngredientForm, extra=0)
        categoryFormSet = formset_factory(CategoryForm, extra=0)

        filledRecipe = RecipeForm(
                initial={
                    'name':          recipe.name, 'description': recipe.description, 'cook_time': recipe.cook_time,
                    'person_amount': recipe.person_amount, 'public': public
                })
        filledIng = ingredientFormSet(
                initial=[{'unit': x.unit, 'name': x.ing_ID, 'amount': x.amount} for x in ingredients])
        filledCategories = categoryFormSet(initial=[{'category': x.category_ID} for x in categories])

        context = {
            'form': filledRecipe, 'ingredientFormset': filledIng, 'categoryFormset': filledCategories,
            'edit': True
        }

        return render(request,
                      'html/recipe/recipe_edit.html',
                      context)


def recipe_hide(request, recipe_id):
    DBUtils.hide_recipe(recipe_id)
    return redirect_to_recipes_list(request)


def redirect_to_recipes_list(request):
    return redirect('recipes_list')


"""
UTILS
"""
def not_authorized():
    return HttpResponse("You are not authorized to do that.")


"""
###############################################################
################### INITIALIZATION VIEWS ######################
###############################################################
"""

def initialize_Units(request):
    if request.user.is_superuser:
       DBUtils.create_units_from_csv()
       return HttpResponse("units initialized")


def initialize_Categories(request):
    if request.user.is_superuser:
       DBUtils.create_categories_from_csv()
       return HttpResponse("Categories initialized")

