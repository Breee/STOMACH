from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Recipe

def index(request):
    latest_recipes_list = Recipe.objects.order_by('-pub_date')[:5]
    context = {'latest_recipes_list': latest_recipes_list}
    return render(request, 'html/index.html', context)