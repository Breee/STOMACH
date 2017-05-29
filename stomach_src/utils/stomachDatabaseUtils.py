from stomach_src.initial_data.InitialValueManager import InitialValueManager
import stomach_src.utils.postDataProcessor as PostProcessor
from django.shortcuts import *
from stomach_src.models import *


def get_recipe_versions(recipe_ID, user_ID):
    relatedRecipes = Recipe_Versions.objects.filter(parent_ID=recipe_ID).values_list('recipe_ID')
    print(relatedRecipes)
    id_recipe = dict()
    for recipe in relatedRecipes:
         id_recipe[recipe[0]] = (get_recipe_details(recipe[0],user_ID))
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
        context = {'recipe': recipe, 'ingredients': ingredients, 'tags': tags, 'categories': categories,
               'userIsCreator': isCreator, 'isPublic': isPublic}
    else:
        context =  None
    return context


def create_new_recipe(request):

    creator_ID = request.user.id

    # convert post data from a querydict to a dict where values are lists.
    dataDict = dict(request.POST.lists())
    print(dataDict)

    PostProcessor.clean(request)


    # post data
    name = dataDict["name"][0]
    description = dataDict["description"][0]
    cook_time = dataDict["cook_time"][0]
    person_amount = dataDict["person_amount"][0]
    ing_names = dataDict["form-0-name"]
    ing_unit_IDs = dataDict["form-0-unit"]
    ing_amounts = dataDict["form-0-amount"]
    category_IDs = dataDict["form-0-category"]

    # create new recipe
    newRecipe = Recipe.objects.create(name=name, description=description, cook_time=cook_time,
                                      person_amount=person_amount)
    newRecipe.publish()

    # create Creator_Recipe relation
    newCreatorRecipe = Creator_Recipe.objects.create(recipe_ID_id=newRecipe.id, creator_ID_id=creator_ID)
    if "public" in dataDict:
        public = dataDict["public"][0]
        if public == "on":
            newCreatorRecipe.public = True
    else:
        newCreatorRecipe.public = False
    newCreatorRecipe.save()

    # related recipe
    Recipe_Versions.objects.create(parent_ID_id=newRecipe.id,recipe_ID_id=newRecipe.id,version=1)

    # create new ingredients + ing_recipe relations
    # also add a tag for each ingredient's name.
    for i in range(0, len(ing_names)):
        # ingredient name + unit + amount
        # TODO: check for duplicates, should probably already happen on the frontend side.
        name = ing_names[i]
        unit = ing_unit_IDs[i]
        amount = ing_amounts[i]

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
    for id in category_IDs:
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
    Unit.objects.create(name=name,short=short,language=language)

def delete_all_units():
    Unit.objects.all().delete()


def create_category(name,language):
    Category.objects.create(name=name,language=language)

def delete_all_categories():
    Category.objects.all().delete()



def create_new_storage(request):
    creator_ID = request.user.id

    # convert post data from a querydict to a dict where values are lists.
    dataDict = dict(request.POST.lists())

    # post data
    name = dataDict["name"][0]
    ing_names = dataDict["form-0-name"]
    ing_unit_IDs = dataDict["form-0-unit"]
    ing_amounts = dataDict["form-0-amount"]

    # create new storage
    newStorage = Storage.objects.create(name=name, user_ID_id=creator_ID)

    # create new ingredients and Storage_Ingredient relations
    for i in range(0, len(ing_names)):
        # ingredient name + unit + amount
        # TODO: check for duplicates, should probably already happen on the frontend side.
        name = ing_names[i]
        unit = ing_unit_IDs[i]
        amount = ing_amounts[i]

        # new ingredient
        if Ingredient.objects.all().filter(name=name).count() == 0:
            newIngredient = Ingredient.objects.create(name=name)
        else:
            newIngredient = Ingredient.objects.all().get(name=name)

        # new Storage_Ingredient relation
        Storage_Ingredient.objects.create(unit=Unit.objects.get(id=unit), amount=amount, ing_ID_id=newIngredient.id, storage_ID_id=newStorage.id)

    return newStorage.id



"""
INIT STUFF
"""

def create_units_from_csv():
    delete_all_units()
    im = InitialValueManager()
    im.read_unit_csv('stomach_src/initial_data/units_GER.csv', 'GER')
    for unit in im.get_unit_dict().values():
        create_unit(unit.get_name(), unit.get_short(), unit.get_language())

def create_categories_from_csv():
    delete_all_categories()
    im = InitialValueManager()
    im.read_category_csv('stomach_src/initial_data/categories.csv')
    for category in im.get_category_dict().values():
        create_category(category.get_name(), category.get_language())