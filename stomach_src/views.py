from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import *
from django.template import RequestContext
from django.urls import reverse
from django.forms import formset_factory

from stomach_src.models import Ing_Recipe
from .models import Recipe
from .models import Ing_Recipe
from .models import Tag_Recipe
from .models import Category_Recipe

from .forms import RecipeForm
from .forms import IngredientForm
from .forms import CategoryForm

def home(request):
    return render(request, 'html/home.html',{})

def recipes(request):
    recipes_list = Recipe.objects.order_by('-published_date')
    # context is a map with elements of the form (id -> iterable)
    # where the id is the name accessible in html templates.
    context = {'latest_recipes_list': recipes_list}
    # render will replace the python code in the template with whatever you defined.
    return render(request, 'html/recipe_list.html', context)

def detail(request,recipe_id):

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = Ing_Recipe.objects.all().filter(recipe_ID=recipe_id)
    tags = Tag_Recipe.objects.all().filter(recipe_ID=recipe_id)
    categories = Category_Recipe.objects.all().filter(recipe_ID=recipe_id)
    context = {'recipe': recipe,'ingredients': ingredients,'tags': tags, 'categories':categories}

    return render(request, 'html/detail.html', context)

def recipe_new(request):
    if request.method == "POST":
        # post data
        name = request.POST["name"]
        description = request.POST["description"]
        cook_time = request.POST["cook_time"]
        person_amount = request.POST["person_amount"]
        ing_names = request.POST["form-0-name"]
        ing_unit_IDs = request.POST["form-0-unit"]
        ing_amounts = request.POST["form-0-amount"]
        category_IDs = request.POST["form-0-category"]
        # creator
        creator_ID = request.user.id
        print(request.POST)
        message = "Thanks, new recipe added"
        context = {'success': message}
        return render(request,
                      'html/recipe_edit.html',
                      context)
    else:
        if request.user.is_authenticated:
            recipeForm = RecipeForm()
            ingredientFormSet = formset_factory(IngredientForm)
            categoryFormSet = formset_factory(CategoryForm)
            context = {'form': recipeForm, 'ingredientFormset': ingredientFormSet, 'categoryFormset': categoryFormSet}
            return render(request,
                          'html/recipe_edit.html',
                          context)
        else:
            recipes_list = Recipe.objects.order_by('-published_date')
            message = "Only logged in users can create new recipes."
            context = {'notAuthorized' : message,'latest_recipes_list': recipes_list}
            return render(request, 'html/recipe_list.html', context )