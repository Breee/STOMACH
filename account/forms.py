from django import forms
from .models import *


class UserSettingsForm(forms.ModelForm):
    username = forms.CharField(max_length=25)

    class Meta:
        model = Settings
        exclude = ('isActiveStorage', 'user', 'visible', 'created_date')

    def process(self):
        return self.cleaned_data


class AppSettingsForm(forms.ModelForm):
    isActiveStorage = forms.BooleanField(required=False)

    class Meta:
        model = Settings
        fields = ['isActiveStorage']

    def process(self):
        return self.cleaned_data
