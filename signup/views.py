from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from account.models import *

from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            Settings.objects.create(user=user.id)
            return redirect('recipes_list')
    else:
        form = SignUpForm()
    return render(request, 'html/registration/signup.html', {'form': form})