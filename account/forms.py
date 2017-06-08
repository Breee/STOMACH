from django import forms
from .models import *


class SettingsForm(forms.ModelForm):
    username = forms.CharField(max_length=25)
    class Meta:
        model = Settings
        exclude = ('user', 'visible', 'created_date')
