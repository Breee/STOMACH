from django.shortcuts import *

import utils.postDataProcessor as PostProcessor
from recipe.initial_data.InitialValueManager import InitialValueManager
from recipe.models import *
from storage.models import *
from django.db.models import Count
from django.db.models import Q


def get_recipe_versions(recipe_ID, user_ID):
    relatedRecipes = Recipe_Versions.objects.filter(parent_ID=recipe_ID).values_list('recipe_ID')
    print(relatedRecipes)
    id_recipe = dict()
    for recipe in relatedRecipes:
        id_recipe[recipe[0]] = (get_recipe_details(recipe[0], user_ID))
    return id_recipe


def get_recipe_details(recipe_id, user_ID):
    recipe = get_object_or_404(Recipe, pk=recipe_id, visible=True)
    ingredients = Ing_Recipe.objects.all().filter(recipe_ID=recipe_id)
    tags = Tag_Recipe.objects.all().filter(recipe_ID=recipe_id)
    categories = Category_Recipe.objects.all().filter(recipe_ID=recipe_id)
    # check if user is the creator of the recipe in order to enable an edit function.
    try:
        Creator_Recipe.objects.get(recipe_ID=recipe_id, creator_ID=user_ID)
        isCreator = True
    except:
        isCreator = False

    try:
        isPublic = Creator_Recipe.objects.get(recipe_ID=recipe_id).public
    except:
        raise KeyError("recipe with id: " + recipe_id + " does not exist.")

    if (isCreator) or (not isCreator and isPublic):
        context = {
            'recipe':        recipe, 'ingredients': ingredients, 'tags': tags, 'categories': categories,
            'userIsCreator': isCreator, 'isPublic': isPublic
            }
    else:
        context = None
    return context


def get_user_recipes(request):
    userRecipes = Creator_Recipe.objects.filter(creator_ID=request.user.id).values_list('recipe_ID')
    recipes = Recipe.objects.filter(pk__in=userRecipes, visible=True)
    return recipes


def get_recipe_list(request, active_filters=None):
    # get all public recipes
    public_recipes = Creator_Recipe.objects.filter(public=True).values_list('recipe_ID')
    # get all user recipes
    user_recipes = get_user_recipes(request).values_list('id')
    # union public and user recipes
    public_user = public_recipes.union(user_recipes)
    recipe_list = Recipe.objects.filter(pk__in=public_user, visible=True).order_by('-published_date')

    # initialize selected filters to prevent errors.
    selected_filters = Category.objects.none()

    # the active filters are a list of category ids,
    if active_filters is not None:
        # filter category_recipe objects by active filters.
        cat_rec = Category_Recipe.objects.filter(category_ID__in=active_filters)\
            .values('recipe_ID')\
            .annotate(count=Count('recipe_ID'))\
            .filter(count=len(active_filters)).values('recipe_ID')
        # filter recipes by all recipes related to the active filters.
        recipe_list = recipe_list.filter(pk__in=cat_rec)
        # selected filters is a queryset of categories, where the category id appears in the active_filters
        selected_filters = Category.objects.filter(pk__in=active_filters)
    else:
        active_filters = Category.objects.none()

    # filters are determined as follows, we filter by the recipes in the recipe_list, we exclude active filters to
    # prevent duplicates,
    # we annotate the queryset with a value count, which equals the amount of appeare nces of a category_id.
    # ---> a queryset {(category_id_1,category_id__name_1,count_1),...,(category_id_n,category_id_name_n ,count_n) }
    filters = Category_Recipe.objects.filter(recipe_ID__in=recipe_list.values_list('id'))\
                                     .exclude(category_ID__in=active_filters)\
                                     .values('category_ID', 'category_ID__name')\
                                     .annotate(count=Count('category_ID'))
    return recipe_list, filters, selected_filters


def create_new_recipe(request):
    creator_ID = request.user.id

    # process post request data
    cleanedData = PostProcessor.clean_recipe_post_data(request)

    # create new recipe
    newRecipe = Recipe.objects.create(name=cleanedData['name'], description=cleanedData['description'],
                                      cook_time=cleanedData['cook_time'],
                                      person_amount=cleanedData['person_amount'])
    newRecipe.publish()

    # create Creator_Recipe relation
    Creator_Recipe.objects.create(recipe_ID_id=newRecipe.id, creator_ID_id=creator_ID, public=cleanedData['public'])
    # related recipe
    Recipe_Versions.objects.create(parent_ID_id=newRecipe.id, recipe_ID_id=newRecipe.id, version=1)

    # create new ingredients + ing_recipe relations
    # also add a tag for each ingredient's name.
    for id, value in cleanedData['ingredients'].items():
        # ingredient name + unit + amount
        name = value['name']
        unit = value['unit']
        amount = value['amount']

        # new ingredient
        if Ingredient.objects.all().filter(name=name).count() == 0:
            newIngredient = Ingredient.objects.create(name=name)
        else:
            newIngredient = Ingredient.objects.all().get(name=name)

        # new ing_recipe relation
        Ing_Recipe.objects.create(unit=Unit.objects.get(id=unit), amount=amount, recipe_ID_id=newRecipe.id,
                                  ing_ID_id=newIngredient.id)

        # new tag where the name equals the name of the ingredient.
        newTag = Tag.objects.create(name=name)

        # new tag_recipe relation
        Tag_Recipe.objects.create(recipe_ID_id=newRecipe.id, tag_ID_id=newTag.id)

    # create category_Recipe relation
    for id in cleanedData['categories']:
        try:
            Category_Recipe.objects.create(recipe_ID_id=newRecipe.id, category_ID_id=id)
        except:
            print("No categories set")

    return newRecipe.id


def hide_recipe(recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        recipe.visible = False
        recipe.save()
    except:
        raise ValueError("recipe with id %d does not exist" % recipe_id)


def create_unit(name, short, language):
    Unit.objects.create(name=name, short=short, language=language)


def delete_all_units():
    Unit.objects.all().delete()


def create_category(name, language):
    Category.objects.create(name=name, language=language)


def delete_all_categories():
    Category.objects.all().delete()


def create_new_storage(request):
    creator_ID = request.user.id

    # process post request data
    cleanedData = PostProcessor.clean_recipe_post_data(request)

    # create new storage
    newStorage = Storage.objects.create(name=cleanedData['name'], user_ID_id=creator_ID)

    # create new ingredients and Storage_Ingredient relations
    for id, value in cleanedData['ingredients'].items():
        # ingredient name + unit + amount
        name = value['name']
        unit = value['unit']
        amount = value['amount']

        # new ingredient
        if Ingredient.objects.all().filter(name=name).count() == 0:
            newIngredient = Ingredient.objects.create(name=name)
        else:
            newIngredient = Ingredient.objects.all().get(name=name)

        # new Storage_Ingredient relation
        Storage_Ingredient.objects.create(unit=Unit.objects.get(id=unit), amount=amount, ing_ID_id=newIngredient.id,
                                          storage_ID_id=newStorage.id)

    return newStorage.id


def hide_storage(storage_id):
    try:
        storage = Storage.objects.get(id=storage_id)
        storage.visible = False
        storage.save()
    except:
        raise ValueError("storage with id %d does not exist" % storage_id)


"""
INIT STUFF
"""


def create_units_from_csv():
    delete_all_units()
    im = InitialValueManager()
    im.read_unit_csv('recipe/initial_data/units_GER.csv', 'GER')
    for unit in im.get_unit_dict().values():
        create_unit(unit.get_name(), unit.get_short(), unit.get_language())


def create_categories_from_csv():
    delete_all_categories()
    im = InitialValueManager()
    im.read_category_csv('recipe/initial_data/categories_EN_US.csv', 'EN_US')
    for category in im.get_category_dict().values():
        create_category(category.get_name(), category.get_language())
