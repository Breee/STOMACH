from django.shortcuts import *

def home(request):
    return render(request,
                  'html/home.html',
                  {})

