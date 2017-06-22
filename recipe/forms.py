from django import forms

from .models import *

from haystack.forms import SearchForm
from haystack.inputs import AutoQuery
import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet

class RecipeSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()
        print("QUERY: %s" %self.cleaned_data['q'])
        sqs = self.searchqueryset.filter(text=AutoQuery(self.cleaned_data['q']))

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

    def autocomplete(self,request):
        q = request.GET.get('q', '')
        if q:
            sqs = self.searchqueryset.autocomplete(text=q)[:20]
            suggestions = []
            ing_count = 0
            rec_count = 0
            for x in sqs:
                if x.model.__name__ == Ingredient.__name__:
                    ing_count += 1
                    if ing_count > 5: continue
                elif x.model.__name__ == Recipe.__name__:
                    rec_count += 1
                    if rec_count > 5: continue
                category = x.model.__name__ + 's which contain the query "%s"' % q
                suggestions.append({'label':x.name,'category': category})
        else:
            return []
        print(suggestions)
        return suggestions


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
