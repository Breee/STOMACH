from django.shortcuts import *
from django.http import HttpResponseRedirect
from .models import *
from .forms import *


def account_form(request):

    if request.method == 'POST':
        # save shit
        form = SettingsForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('myaccount')
    else:
        username = get_object_or_404(Settings, user_id=request.user.id).user.username
        print(username)
        mysettings = SettingsForm(initial={'username': username})
        context = {'mysettings': mysettings}
        return render(request, 'html/account/account_view.html', context)
