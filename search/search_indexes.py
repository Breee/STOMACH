import datetime
from haystack import indexes
from recipe.models import *

class RecipeIndex(indexes.SearchIndex,indexes.Indexable):

    text = indexes.CharField(document=True,use_template=True)
    name = indexes.CharField(model_attr='name')
    rec_id = indexes.IntegerField(model_attr='pk')
    description = indexes.CharField(model_attr='description')
    published_date = indexes.DateTimeField(model_attr='published_date')
    public = indexes.BooleanField(model_attr='recipe_creator__public')
    visible = indexes.BooleanField(model_attr='visible')
    categories = indexes.MultiValueField(null=True, faceted=True)

    def prepare_categories(self, obj):
        return [cat.category_ID.id for cat in obj.recipe_category.all()] or None

    def get_updated_field(self):
        return "updated_at"

    def get_model(self):
        return Recipe
