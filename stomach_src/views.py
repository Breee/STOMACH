from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Recipe

def index(request):
    # simply gets the 5 most recent created recipes and orders them by publishing date
    latest_recipes_list = Recipe.objects.order_by('-pub_date')[:5]

    # context is a map with elements of the form (id -> iterable)
    # where the id is the name accessible in html templates.
    context = {'latest_recipes_list': latest_recipes_list}

    # render will replace the python code in the template with whatever you defined.
    return render(request, 'html/index.html', context)