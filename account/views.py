from django.shortcuts import *
from django.http import HttpResponseRedirect
from .models import *
from .forms import *


def account_form(request):

    if request.method == 'POST':
        userForm = UserSettingsForm(data=request.POST, instance=request.user)
        storSetting = Settings.objects.get(user_id=request.user.id)
        appForm = AppSettingsForm(data=request.POST, instance=storSetting)
        if userForm.is_valid() and appForm.is_valid():
            newUserSett = userForm.save()
            newAppSett = appForm.save(commit=False)
            newAppSett.user_id = newUserSett.id
            newAppSett.save()
            return HttpResponseRedirect(reverse('myaccount'))
    else:
        username = get_object_or_404(Settings,
                                     user_id=request.user.id).user.username
        isActiveStorage = get_object_or_404(Settings,
                                            user_id=request.user.id).isActiveStorage

        myStorageSettings = AppSettingsForm(initial={'isActiveStorage': isActiveStorage})
        myUserSettings = UserSettingsForm(initial={'username': username})

        context = {'myUserSettings': myUserSettings, 'myStorageSettings': myStorageSettings}
        return render(request, 'html/account/account_view.html', context)
