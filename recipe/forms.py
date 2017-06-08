from django import forms

from .models import *


class RecipeForm(forms.ModelForm):
    description = forms.CharField(max_length=1000,
                           widget=forms.Textarea(attrs={
                               'placeholder': 'how to prepare this recipe?'
                           }), required=False)
    public =  forms.BooleanField(widget=forms.CheckboxInput,required=False)

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['cook_time'].widget.attrs['min'] = 1
        self.fields['person_amount'].widget.attrs['min'] = 1

    class Meta:
        model = Recipe
        fields = ('name', 'cook_time', 'person_amount')

class IngredientForm(forms.Form):
    name = forms.CharField(max_length=200,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'ingredient name'
                           }), required=True, empty_value='')
    amount = forms.IntegerField(min_value=0, required=True)
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(),empty_label=None, required=True)

class CategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)