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


def recipes_list(request, message="", user_recipe=False):

    query = request.GET.get('q') if request.GET.get('q') is not None else ''
    # filters are get requests
    # there are two queries related to filters, ?filter=xxx and ?removefilter=xxx
    # ?filter=xxx will apply a filter and ?removefilter=xxx will remove it.
    filters = request.GET.getlist('filter')
    removed_filters = request.GET.getlist('removefilter')
    # remove filters which have been deselected.
    filters = [x for x in filters if x not in removed_filters]
    recipe_list, filter, selected_filters = DBUtils.get_recipe_list(request, None if len(filters) == 0 else filters, user_recipe)
    # build a filter string to preserve applied filters.
    filter_string = build_filter_string(selected_filters)

    context = {
        'latest_recipes_list': recipe_list, "message": message, 'filters': filter, 'selected_filters': selected_filters,
        'filter_string': filter_string, 'query':query
    }
    return render(request,
                  'html/recipe/recipe_list.html',
                  context)


def build_filter_string(selected_filters):
    """
    Function that will build a string out of selected_filters in the form of a typical get
    e.g selected filter ids may be 1,15.. the string produced is ?filter=1&filter=15
    in the frontend these strings are appended to the href of the filters.
    :param selected_filters: 
    :return: 
    """
    filter_string = ''
    for filter in selected_filters:
        if filter_string == '':
            filter_string += '?'
        else:
            filter_string += '&'
        filter_string += 'filter=%s' % filter.id
    return filter_string


def recipe_detail(request, recipe_id):
    context = DBUtils.get_recipe_details(recipe_id, request.user.id,request.user.is_superuser)
    if context is None:
        return not_authorized()

    return render(request,
                  'html/recipe/recipe_detail.html',
                  context)


@login_required
def recipes_user(request):
    return recipes_list(request,"",user_recipe=True)

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
            ingredientFormSet  = ingredientFormSet(prefix='ingredient')

            categoryFormSet = formset_factory(CategoryForm, extra=1)
            categoryFormSet = categoryFormSet(prefix='category')

            context = {
                'recipe_formset': recipeForm, 'ingredient_formset': ingredientFormSet, 'category_formset': categoryFormSet,
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

    if recipecontext == None or recipecontext['user_can_edit'] == False:
        return not_authorized()

    recipe = recipecontext['recipe']
    ingredients = recipecontext['ingredients']
    categories = recipecontext['categories']
    public = recipecontext['recipe_is_public']

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

        # fill recipe form.
        filled_recipe = RecipeForm(
                initial={
                    'name': recipe.name, 'description': recipe.description, 'cook_time': recipe.cook_time,
                    'person_amount': recipe.person_amount, 'public': public
                    })

        # fill ingredient forms.
        filled_ing = ingredientFormSet(
                initial=[{'unit': x.unit, 'name': x.ing_ID, 'amount': x.amount} for x in ingredients],prefix='ingredient')

        # fill category forms.
        filled_categories = categoryFormSet(initial=[{'category': x.category_ID} for x in categories],prefix='category')

        context = {
            'recipe_formset': filled_recipe, 'ingredient_formset': filled_ing, 'category_formset': filled_categories,
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
