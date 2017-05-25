from django.shortcuts import *
from django.contrib.auth.decorators import login_required

from django.forms import formset_factory

import stomach_src.utils.stomachDatabaseUtils as DBUtils

from .models import *
from .forms import *


def home(request):
    return render(request,
                  'html/home.html',
                  {})


"""
#########################################################
################### Recipe Views ########################
#########################################################
"""

def recipes_list(request, message=""):
    recipes_list = Recipe.objects.order_by('-published_date').filter(visible=True)
    # context is a map with elements of the form (id -> iterable)
    # where the id is the name accessible in html templates.
    context = {'latest_recipes_list': recipes_list, "message": message}
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
    userRecipes = Creator_Recipe.objects.filter(creator_ID=request.user.id).values_list('recipe_ID')
    print("USER")
    print(userRecipes)
    recipes = Recipe.objects.filter(pk__in=userRecipes, visible=True)
    print(recipes)
    context = {'recipes': recipes}
    return render(request,
                  'html/recipe/recipes_user.html',
                  context)

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
            ingredientFormSet = formset_factory(IngredientForm,extra=1)
            categoryFormSet = formset_factory(CategoryForm,extra=1)
            context = {'form': recipeForm, 'ingredientFormset': ingredientFormSet, 'categoryFormset': categoryFormSet,
                       'edit': False}
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


def recipe_edit(request, recipe_id):
    recipecontext = DBUtils.get_recipe_details(recipe_id, request.user.id)
    if recipecontext == None or recipecontext['userIsCreator'] == False:
        return not_authorized()


    recipe = recipecontext['recipe']
    ingredients = recipecontext['ingredients']
    categories = recipecontext['categories']
    public = recipecontext['isPublic']

    if request.method == "POST":
        Recipe.objects.filter(id=recipe_id).delete()
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




def recipe_hide(request, recipe_id):
    DBUtils.hide_recipe(recipe_id)
    return redirect_to_recipes_list(request)


def redirect_to_recipes_list(request):
    return redirect('recipes_list')


"""
#########################################################
################### Storage Views #######################
#########################################################
"""


def storage_new(request):
    if request.method == "POST":
        DBUtils.create_new_storage(request)
        message = "Thanks, new storage added"
        context = {'success': message}
        return render(request,
                      'html/storage/storage_new.html',
                      context)
    else:
        if request.user.is_authenticated:
            storageForm = StorageForm()
            ingredientFormSet = formset_factory(IngredientForm)
            context = {'form': storageForm, 'ingredientFormset': ingredientFormSet,
                       'edit': False}
            return render(request,
                          'html/storage/storage_new.html',
                          context)
        else:
            message = "Only logged in users can create new recipes."
            context = {'notAuthorized': message}
            return render(request,
                          'html/storage/storage_view.html',
                          context)


def storage_edit(request, storage_id):
    return HttpResponse("not implemented yet")


def storage_list(request):
    storage_list = Storage.objects.filter(user_ID=request.user.id)
    # context is a map with elements of the form (id -> iterable)
    # where the id is the name accessible in html templates.
    context = {'storage_list': storage_list}
    # render will replace the python code in the template with whatever you defined.
    return render(request,
                  'html/storage/storage_view.html',
                  context)


def storage_detail(request, storage_id):
    storage = get_object_or_404(Storage, id=storage_id, user_ID=request.user)
    ingredients = Storage_Ingredient.objects.filter(storage_ID=storage_id)
    context = {'storage': storage, 'ingredients': ingredients}
    return render(request,
                  'html/storage/storage_detail.html',
                  context)


def storage_delete(request, storage_id):
    try:
        Storage.objects.get(id=storage_id, user_ID=request.user.id).delete()
        message = "Storage %s has been deleted successfully"
    except:
        message = ""
    return redirect_storage_list(request)


def redirect_storage_list(request):
    return redirect('storage_list')


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
    DBUtils.create_units_from_csv()

def initialize_Categories(request):
    DBUtils.create_categories_from_csv()