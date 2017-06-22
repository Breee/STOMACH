from django.shortcuts import *
import utils.postDataProcessor as PostProcessor
from recipe.initial_data.InitialValueManager import InitialValueManager
from recipe.forms import *
from storage.models import *
from django.db.models import Count


def get_recipe_details(recipe_id, user_id, is_superuser):
    """
    Function that gets a recipes details.
    :param recipe_id: 
    :param user_id: 
    :param is_superuser:
    :return: context that contains recipe information 'recipe', 'ingredients','tags','categories', 'userIsCreator',
    'isPublic'
    """
    # superuser can see hidden recipes.
    if is_superuser:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
    else:
        recipe = get_object_or_404(Recipe, pk=recipe_id, visible=True)
    ingredients = Ing_Recipe.objects.all().filter(recipe_ID=recipe_id)
    tags = Tag_Recipe.objects.all().filter(recipe_ID=recipe_id)
    categories = Category_Recipe.objects.all().filter(recipe_ID=recipe_id)
    # check if user is the creator or admin of the recipe in order to enable an edit function.
    # Superusers can do whatever they want, whenever they want.
    if not is_superuser:
        # no 404 -> user is creator and can edit.
        get_object_or_404(Creator_Recipe, recipe_ID=recipe_id, creator_ID=user_id)
    user_can_edit = True
    recipe_is_public = get_object_or_404(Creator_Recipe, recipe_ID=recipe_id).public
    if user_can_edit or (not user_can_edit and recipe_is_public):
        context = {
            'recipe':        recipe, 'ingredients': ingredients, 'tags': tags, 'categories': categories,
            'user_can_edit': user_can_edit, 'recipe_is_public': recipe_is_public
        }
    else:
        context = None
    return context


def get_user_recipes(request):
    """
    Function that returns a queryset that contains all recipes that belong to a user.
    :param request: 
    :return: Queryset that contains Recipe objects.
    """
    user_recipes = Creator_Recipe.objects.filter(creator_ID=request.user.id).values_list('recipe_ID')
    recipes = Recipe.objects.filter(pk__in=user_recipes, visible=True)
    return recipes


def get_recipe_list(request, active_filters=None, user_recipe=False):
    """
    Function that returns a list of recipes, filters and selected filters.
    :param request: request
    :param active_filters: list of active filters
    :param user_recipe: boolean if you want to fetch user-only recipes
    :return: queryset of recipes, queryset of available filters, queryset of selected filters
    """
    # Haystack Searchform takes the field "q" from the get request.
    form = RecipeSearchForm(request.GET)
    recipes = form.search()
    completions = form.autocomplete(request)

    # get all public recipes
    public_recipes = recipes.filter(public=True).values_list('rec_id', flat=True)
    # get all user recipes
    user_recipes = recipes.filter(creator=request.user.id).values_list('rec_id', flat=True)
    # differ between user and public recipes view
    if user_recipe:
        recipe_list = recipes.filter(rec_id__in=user_recipes, visible=True).order_by('published_date')
    else:
        # union public and user recipes
        public_user = public_recipes | user_recipes
        recipe_list = recipes.filter(rec_id__in=public_user | user_recipes, visible=True).order_by('published_date')
    # TODO: (Bree) Use haystack's search facets for the filters.
    # TODO: They are calculated anyway by haystack, so we do not have to fetch them on our own.
    # initialize selected filters to prevent errors.
    selected_filters = Category.objects.none()
    # the active filters are a list of category ids,
    if active_filters is not None:
        # filter category_recipe objects by active filters.
        cat_rec = Category_Recipe.objects.filter(category_ID__in=active_filters) \
            .values('recipe_ID') \
            .annotate(count=Count('recipe_ID')) \
            .filter(count=len(active_filters)).values_list('recipe_ID', flat=True)
        # filter recipes by all recipes related to the active filters.
        recipe_list = recipe_list.filter(rec_id__in=cat_rec).order_by('published_date')
        # selected filters is a queryset of categories, where the category id appears in the active_filters
        selected_filters = Category.objects.filter(pk__in=active_filters)
    else:
        active_filters = Category.objects.none()
    # filters are determined as follows, we filter by the recipes in the recipe_list, we exclude active filters to
    # prevent duplicates,
    # we annotate the queryset with a value count, which equals the amount of appearences of a category_id.
    # ---> a queryset {(category_id_1,category_id__name_1,count_1),...,(category_id_n,category_id_name_n ,count_n) }
    available_filters = Category_Recipe.objects.filter(recipe_ID__in=recipe_list.values_list('rec_id', flat=True)) \
        .exclude(category_ID__in=active_filters) \
        .values('category_ID', 'category_ID__name') \
        .annotate(count=Count('category_ID')).order_by('-count')
    return recipe_list, available_filters, selected_filters, completions


def create_new_recipe(request):
    """
    Function that creates a new recipe.
    :param request: 
    :return: id of new recipe
    """
    creator_id = request.user.id

    # process post request data
    cleaned_data = PostProcessor.clean_post_data(request)

    # create new recipe
    new_recipe = Recipe.objects.create(name=cleaned_data['name'], description=cleaned_data['description'],
                                       cook_time=cleaned_data['cook_time'],
                                       person_amount=cleaned_data['person_amount'])
    new_recipe.publish()

    # create Creator_Recipe relation
    Creator_Recipe.objects.create(recipe_ID_id=new_recipe.id, creator_ID_id=creator_id, public=cleaned_data['public'])

    # create new ingredients + ing_recipe relations
    # also add a tag for each ingredient's name.
    for value in cleaned_data['ingredients'].values():
        # ingredient name + unit + amount
        name = value['name']
        unit = value['unit']
        amount = value['amount']

        # new ingredient
        if Ingredient.objects.all().filter(name=name).count() == 0:
            new_ingredient = Ingredient.objects.create(name=name)
        else:
            new_ingredient = Ingredient.objects.all().get(name=name)

        # new ing_recipe relation
        Ing_Recipe.objects.create(unit=Unit.objects.get(id=unit), amount=amount, recipe_ID_id=new_recipe.id,
                                  ing_ID_id=new_ingredient.id)

        # new tag where the name equals the name of the ingredient.
        new_tag = Tag.objects.create(name=name)

        # new tag_recipe relation
        Tag_Recipe.objects.create(recipe_ID_id=new_recipe.id, tag_ID_id=new_tag.id)

    # create category_Recipe relation
    for cat_id in cleaned_data['categories']:
        Category_Recipe.objects.create(recipe_ID_id=new_recipe.id, category_ID_id=cat_id)
    new_recipe.save()
    return new_recipe.id


def hide_recipe(recipe_id):
    """
    Function to set a recipe invisible to all users.
    :param recipe_id: 
    :return: 
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.visible = False
    recipe.save()


def create_unit(name, short, language):
    Unit.objects.create(name=name, short=short, language=language)


def delete_all_units():
    Unit.objects.all().delete()


def create_category(name, language):
    Category.objects.create(name=name, language=language)


def delete_all_categories():
    Category.objects.all().delete()


def create_new_storage(request):
    creator_id = request.user.id

    # process post request data
    cleaned_data = PostProcessor.clean_post_data(request)

    # create new storage
    new_storage = Storage.objects.create(name=cleaned_data['name'], user_ID_id=creator_id)

    # create new ingredients and Storage_Ingredient relations
    for ing_id, value in cleaned_data['ingredients'].items():
        # ingredient name + unit + amount
        name = value['name']
        unit = value['unit']
        amount = value['amount']

        # new ingredient
        if Ingredient.objects.all().filter(name=name).count() == 0:
            new_ingredient = Ingredient.objects.create(name=name)
        else:
            new_ingredient = Ingredient.objects.all().get(name=name)

        # new Storage_Ingredient relation
        Storage_Ingredient.objects.create(unit=Unit.objects.get(id=unit), amount=amount, ing_ID_id=new_ingredient.id,
                                          storage_ID_id=new_storage.id)

    return new_storage.id


def hide_storage(storage_id):
    storage = get_object_or_404(Storage, pk=storage_id)
    storage.visible = False
    storage.save()


def get_storage_details(storage_id, user_id, is_superuser):
    """
    Function that returns details of a storage.
    :param storage_id: 
    :param user_id: 
    :param is_superuser: 
    :return: map which contains information about the storage and ingredients.
    """
    # superuser can see hidden recipes.
    if is_superuser:
        storage = get_object_or_404(Storage, pk=storage_id, user_ID=user_id)
    else:
        storage = get_object_or_404(Storage, pk=storage_id, user_ID=user_id, visible=True)

    ingredients = Storage_Ingredient.objects.all().filter(storage_ID=storage_id)
    context = {
        'storage': storage, 'ingredients': ingredients,
        }

    return context


"""
INIT STUFF
"""
# TODO: should be in an extra python script. (some kind of installation thing)
def create_units_from_csv():
    delete_all_units()
    im = InitialValueManager()
    im.read_unit_csv('recipe/initial_data/units_EN_US.csv', 'EN_US')
    for unit in im.get_unit_dict().values():
        create_unit(unit.get_name(), unit.get_short(), unit.get_language())

def create_categories_from_csv():
    delete_all_categories()
    im = InitialValueManager()
    im.read_category_csv('recipe/initial_data/categories_EN_US.csv', 'EN_US')
    for category in im.get_category_dict().values():
        create_category(category.get_name(), category.get_language())
