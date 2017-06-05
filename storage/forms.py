from django import forms

from .models import *

class StorageForm(forms.ModelForm):

    class Meta:
        model = Storage
        exclude = ('user_ID','visible','created_date')