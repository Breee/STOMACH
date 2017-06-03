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
    # filters are get requests
    # there are two queries related to filters, ?filter=xxx and ?removefilter=xxx
    # ?filter=xxx will apply a filter and ?removefilter=xxx will remove it.
    filters = request.GET.getlist('filter')
    removedFilters = request.GET.getlist('removefilter')
    filters = [x for x in filters if x not in removedFilters]
    recipe_list, filter, selected_filters = DBUtils.get_recipe_list(request, None if len(filters) == 0 else filters)
    filter_string = build_filter_string(selected_filters)
    context = {
        'latest_recipes_list': recipe_list, "message": message, 'filters': filter, 'selected_filters': selected_filters,
        'filter_string': filter_string
    }
    return render(request,
                  'html/recipe/recipe_list.html',
                  context)


def build_filter_string(selected_filters):
    filter_string = ''
    for filter in selected_filters:
        if filter_string == '':
            filter_string += '?'
        else:
            filter_string += '&'
        filter_string += 'filter=%s' % filter.id
    print(filter_string)
    return filter_string


def filter_recipes(request):
    print(request.GET)
    filters = request.GET.getlist('filters')
    print(filters)
    return recipes_list(request)


def recipe_detail(request, recipe_id):
    context = DBUtils.get_recipe_details(recipe_id, request.user.id,request.user.is_superuser)
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


def recipe_new(request):
    if request.method == "POST":
        recipe_id = DBUtils.create_new_recipe(request)
        message = "Thanks, new recipe added"
        context = {'success': message, 'id':recipe_id}
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
            message = "Only logged in users can create new recipes."
            return recipes_list(request, message)


def recipe_edit(request, recipe_id):
    recipecontext = DBUtils.get_recipe_details(recipe_id, request.user.id,request.user.is_superuser)
    if recipecontext == None or recipecontext['userIsCreator'] == False:
        return not_authorized()

    recipe = recipecontext['recipe']
    ingredients = recipecontext['ingredients']
    categories = recipecontext['categories']
    public = recipecontext['isPublic']

    if request.method == "POST":
        DBUtils.hide_recipe(recipe_id)
        newID = DBUtils.create_new_recipe(request)
        message = "Thanks, your recipe was edited"
        context = {'success': message, 'id':newID}

        return render(request,
                      'html/recipe/recipe_edit.html',
                      context)
    else:
        ingredientFormSet = formset_factory(IngredientForm, extra=0)
        categoryFormSet = formset_factory(CategoryForm, extra=0)

        filledRecipe = RecipeForm(
                initial={
                    'name': recipe.name, 'description': recipe.description, 'cook_time': recipe.cook_time,
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
    DBUtils.create_units_from_csv()
    return HttpResponse("units initialized")


def initialize_Categories(request):
    DBUtils.create_categories_from_csv()
    return HttpResponse("Categories initialized")
