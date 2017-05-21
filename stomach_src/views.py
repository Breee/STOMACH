from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import *
from django.template import RequestContext
from django.urls import reverse
from django.forms import formset_factory

from stomach_src.models import Ing_Recipe
from .models import Recipe
from .models import Ingredient

from .models import Creator_Recipe
from .models import Ing_Recipe

from .models import Unit

from .models import Tag
from .models import Tag_Recipe

from .models import Category_Recipe

from .forms import RecipeForm
from .forms import IngredientForm
from .forms import CategoryForm


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
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = Ing_Recipe.objects.all().filter(recipe_ID=recipe_id)
    tags = Tag_Recipe.objects.all().filter(recipe_ID=recipe_id)
    categories = Category_Recipe.objects.all().filter(recipe_ID=recipe_id)
    context = {'recipe': recipe, 'ingredients': ingredients, 'tags': tags, 'categories': categories}

    return render(request, 'html/recipe/recipe_detail.html', context)


def recipe_new(request):
    if request.method == "POST":

        creator_ID = request.user.id
        # convert post data from a querydict to a dict where values are lists.
        dataDict = dict(request.POST.lists())

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

        # create new ingredients + ing_recipe relations
        # also add a tag for each ingredient's name.
        for i in range(0,len(ing_names)):
            # ingredient name + unit + amount
            # TODO: check for duplicates, should probably already happen on the frontend side.
            name = ing_names[i]
            unit = ing_unit_IDs[i]
            amount = ing_amounts[i]

            # new ingredient
            if Ingredient.objects.all().filter(name=name).count() == 0:
                newIngredient = Ingredient.objects.create(name=name)
                newIngredient.save()
            else:
                newIngredient = Ingredient.objects.all().get(name=name)

            # new ing_recipe relation
            newIngRecipe = Ing_Recipe.objects.create(unit=Unit.objects.get(id=unit), amount=amount, recipe_ID_id=newRecipe.id,
                                                     ing_ID_id=newIngredient.id)
            newIngRecipe.save()

            # new tags
            newTag = Tag.objects.create(name=name)
            newTag.save()

            # new tag_recipe relation
            newTagRecipe = Tag_Recipe.objects.create(recipe_ID_id=newRecipe.id, tag_ID_id=newTag.id)
            newTagRecipe.save()

        # create category_Recipe relation
        for id in category_IDs:
            newCategoryRecipe = Category_Recipe.objects.create(recipe_ID_id=newRecipe.id, category_ID_id=id)
            newCategoryRecipe.save()

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
            context = {'form': recipeForm, 'ingredientFormset': ingredientFormSet, 'categoryFormset': categoryFormSet}
            return render(request,
                          'html/recipe/recipe_edit.html',
                          context)
        else:
            recipes_list = Recipe.objects.order_by('-published_date')
            message = "Only logged in users can create new recipes."
            context = {'notAuthorized': message, 'latest_recipes_list': recipes_list}
            return render(request, 'html/recipe/recipe_list.html', context)
