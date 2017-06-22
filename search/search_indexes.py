import datetime
from haystack import indexes
from recipe.models import *


class RecipeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    name = indexes.EdgeNgramField(model_attr='name', null=True)
    rec_id = indexes.IntegerField(model_attr='pk', null=True)
    description = indexes.EdgeNgramField(model_attr='description', null=True)
    published_date = indexes.DateTimeField(model_attr='published_date', null=True)
    public = indexes.BooleanField(model_attr='recipe_creator__public', null=True)
    creator = indexes.BooleanField(model_attr='recipe_creator__creator_ID', null=True)
    visible = indexes.BooleanField(model_attr='visible', null=True)
    # index categories + ingredients, such that the RealTimeSignalProcessor updates the index for them when a new rec is added.
    categories = indexes.MultiValueField(null=True, faceted=True)
    ingredients = indexes.MultiValueField(null=True, faceted=True)

    def prepare_categories(self, obj):
        return [cat.category_ID.id for cat in obj.recipe_category.all()] or None

    def prepare_ingredients(self, obj):
        return [ing.ing_ID.id for ing in obj.recipe_ingredient.all()] or None

    def get_updated_field(self):
        return "updated_at"

    def get_model(self):
        return Recipe

class IngredientIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.EdgeNgramField(document=True, use_template=True)
    name = indexes.EdgeNgramField(model_attr='name', null=True)

    def get_updated_field(self):
        return "updated_at"

    def get_model(self):
        return Ingredient