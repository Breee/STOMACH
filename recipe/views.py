from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import *
import utils.stomachDatabaseUtils as DBUtils
from .forms import *
from django.db.models.query import QuerySet
from haystack.query import SearchQuerySet
import json
from django.http import JsonResponse
from utils.CustomDjangoJSONEncoder import CustomDjangoJSONEncoder

"""
#########################################################
################### Recipe Views ########################
#########################################################
"""


def recipes_list(request, message="", user_recipe=False):
    """
    view for the recipes list/search. 
    :param request: 
    :param message: 
    :param user_recipe: 
    :return: recipe_list.html rendered or just a json-response.
    """
    # A get request looks as follows usually:
    # "GET /recipes/?q=flour&initialized=1&filter=60 HTTP/1.1"
    query = request.GET.get('q') if request.GET.get('q') is not None else ''
    initialized = True if request.GET.get('initialized') == '1' else False
    filters = request.GET.getlist('filter')

    recipe_list, filter, selected_filters,completions = DBUtils.get_recipe_list(request, None if len(filters) == 0 else filters,
                                                                    user_recipe)

    context = {
        'latest_recipes_list': recipe_list, "message": message, 'filters': filter, 'selected_filters': selected_filters,
        'query': query, 'completions':completions
        }

    print(recipe_list)

    # We only want to render the site once, in order to have a fast and interactive search.
    # the render function simply takes too much time and feels slow.
    if initialized:
        # context to json
        # 3 cases because Django, Haydtack and non-django-stuff is converted to json differently.
        # TODO: this code could be at another place maybe, find out if this is really the best way.
        for key, value in context.items():
            if isinstance(value, QuerySet):
                context[key] = json.dumps(list(value), cls=CustomDjangoJSONEncoder, default=lambda o: o.__dict__,
                                          sort_keys=True, indent=4)
            elif isinstance(value, SearchQuerySet):
                context[key] = json.dumps(list(map(lambda x: x.get_stored_fields(), value)),
                                          cls=CustomDjangoJSONEncoder)
            else:
                context[key] = json.dumps(value, cls=CustomDjangoJSONEncoder)
        # Simple json response, which can be processed easy at the frontend with JS.
        return JsonResponse(context)
    else:
        return render(request,
                      'html/recipe/recipe_list.html',
                      context)


def recipe_detail(request, recipe_id):
    context = DBUtils.get_recipe_details(recipe_id, request.user.id, request.user.is_superuser)
    if context is None:
        return not_authorized()

    return render(request,
                  'html/recipe/recipe_detail.html',
                  context)


@login_required
def recipes_user(request):
    return recipes_list(request, "", user_recipe=True)


def recipe_new(request):
    if request.method == "POST":
        recipe_id = DBUtils.create_new_recipe(request)
        message = "Thanks, new recipe added"
        context = {'success': message, 'id': recipe_id}
        return render(request,
                      'html/recipe/recipe_edit.html',
                      context)
    else:
        recipeForm = RecipeForm()

        ingredientFormSet = formset_factory(IngredientForm, extra=1)
        ingredientFormSet = ingredientFormSet(prefix='ingredient')

        categoryFormSet = formset_factory(CategoryForm, extra=1)
        categoryFormSet = categoryFormSet(prefix='category')

        context = {
                'recipe_formset':   recipeForm, 'ingredient_formset': ingredientFormSet,
                'category_formset': categoryFormSet,
                'edit':             False
                }
        return render(request,
                          'html/recipe/recipe_edit.html',
                          context)


def recipe_edit(request, recipe_id):
    recipecontext = DBUtils.get_recipe_details(recipe_id, request.user.id, request.user.is_superuser)

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
        context = {'success': message, 'id': newID}

        return render(request,
                      'html/recipe/recipe_edit.html',
                      context)
    else:
        ingredientFormSet = formset_factory(IngredientForm, extra=0)
        categoryFormSet = formset_factory(CategoryForm, extra=0)

        # fill recipe form.
        filled_recipe = RecipeForm(
                initial={
                    'name':          recipe.name, 'description': recipe.description, 'cook_time': recipe.cook_time,
                    'person_amount': recipe.person_amount, 'public': public
                    })

        # fill ingredient forms.
        filled_ing = ingredientFormSet(
                initial=[{'unit': x.unit, 'name': x.ing_ID, 'amount': x.amount} for x in ingredients],
                prefix='ingredient')

        # fill category forms.
        filled_categories = categoryFormSet(initial=[{'category': x.category_ID} for x in categories],
                                            prefix='category')

        context = {
            'recipe_formset': filled_recipe, 'ingredient_formset': filled_ing, 'category_formset': filled_categories,
            'edit':           True
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
