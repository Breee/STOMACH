from django.shortcuts import *
from django.http import HttpResponseRedirect
from .models import *
from .forms import *

'''
These Views are Handling the Forms of the Account Site.
- Changing Username
- Activate/Deactivate stuff.
'''
def account_form(request):

    if request.method == 'POST':
        # Get the Data layout for the Forms to be saveable in the Database
        userForm = UserSettingsForm(data=request.POST, instance=request.user)
        storSetting = Settings.objects.get(user_id=request.user.id)
        appForm = AppSettingsForm(data=request.POST, instance=storSetting)
        # Validate the Forms and save them when they are valid to the Database
        if userForm.is_valid() and appForm.is_valid():
            newUserSett = userForm.save()
            # Get Data, don't save to DB
            newAppSett = appForm.save(commit=False)
            # set Foreign Key
            newAppSett.user_id = newUserSett.id
            # then save
            newAppSett.save()
            return HttpResponseRedirect(reverse('myaccount'))
    else:
        #
        # set the current data to the Forms.
        #
        mySettings = get_object_or_404(Settings, user_id=request.user.id)
        username = mySettings.user.username
        isActiveStorage = mySettings.isActiveStorage
        myStorageSettings = AppSettingsForm(
            initial={'isActiveStorage': isActiveStorage})
        myUserSettings = UserSettingsForm(initial={'username': username})

        context = {'myUserSettings': myUserSettings,
                   'myStorageSettings': myStorageSettings}
        return render(request, 'html/account/account_view.html', context)
