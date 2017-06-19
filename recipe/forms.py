from django import forms

from .models import *

from haystack.forms import SearchForm
from haystack.inputs import AutoQuery

class RecipeSearchForm(SearchForm):
    def no_query_found(self):
        return self.searchqueryset.all()

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()
        print("QUERY: %s" %self.cleaned_data['q'])
        sqs = self.searchqueryset.filter(content__contains=AutoQuery(self.cleaned_data['q']))

        if self.load_all:
            sqs = sqs.load_all()

        return sqs


class RecipeForm(forms.ModelForm):
    description = forms.CharField(max_length=1000,
                                  widget=forms.Textarea(attrs={
                                      'placeholder': 'how to prepare this recipe?'
                                      }), required=False)
    public = forms.BooleanField(widget=forms.CheckboxInput, required=False)

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['cook_time'].widget.attrs['min'] = 1
        self.fields['person_amount'].widget.attrs['min'] = 1

    class Meta:
        model = Recipe
        fields = ('name', 'cook_time', 'person_amount')
        labels = {
            'cook_time': 'Cook time in minutes'
            }


class IngredientForm(forms.Form):
    name = forms.CharField(max_length=200,
                           widget=forms.TextInput(attrs={
                               'placeholder': 'ingredient name'
                               }), required=True, empty_value='')
    amount = forms.IntegerField(min_value=0, required=True)
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), empty_label=None, required=True)


class CategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
