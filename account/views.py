from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def emptyview(request):
    return HttpResponse(request.user.id)
