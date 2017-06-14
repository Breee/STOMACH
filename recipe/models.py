from django.conf import settings
from django.db import models
from django.utils import timezone


"""
#####################################################################
######################## RECIPE SECTION ############################
#####################################################################
"""

# class for units like gram,litre,cups,ounces
class Unit(models.Model):
    name = models.CharField(max_length=50, default="gram")
    short = models.CharField(max_length=10, default="g")
    language = models.CharField(max_length=50,default="EN_US")

    def __str__(self):
        return self.name + "(%s)" % self.short


# class for categories like breakfast, lunch, dinner...
class Category(models.Model):
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=50,default="EN_US")

    def __str__(self):
        return self.name



# class for tags which shall be attached to recipes_list, e.g. flour, oven..
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




# class for recipes_list
class Recipe(models.Model):
    # name of the recipe
    name = models.CharField(max_length=200)
    # date on which the recipe is created/published.
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,)
    # description of the recipe (how to cook xxx..)
    description = models.CharField(max_length=1000)
    # time to prepare/cook the recipe.
    cook_time = models.PositiveIntegerField(default=1)
    # amount of persons.
    person_amount = models.PositiveIntegerField(default=1)
    # visibility
    visible = models.BooleanField(default=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name + " (ID: %d)" % self.id



# class for defines an ingredient
class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# class that defines a mapping [ingredient] -> [recipe]
class Ing_Recipe(models.Model):
    # recipe id
    recipe_ID = models.ForeignKey(Recipe,on_delete=models.CASCADE, related_name='recipe_ingredient')
    # ingredient id
    ing_ID = models.ForeignKey(Ingredient, related_name='ingredient_relation')
    # amount of the ingredient
    amount = models.PositiveIntegerField(default=1)
    # unit of the ingredient
    unit = models.ForeignKey(Unit)

    def __str__(self):
        return "%s(%d) -> %s(%d)" % (self.recipe_ID.name,self.recipe_ID.id,self.ing_ID.name,self.ing_ID.id)


# class that defines a mapping [category] -> [recipe]
class Category_Recipe(models.Model):
    category_ID = models.ForeignKey(Category)
    recipe_ID = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='recipe_category')


# class that defines a mapping [tag] -> [recipe]
class Tag_Recipe(models.Model):
    tag_ID = models.ForeignKey(Tag)
    recipe_ID = models.ForeignKey(Recipe,on_delete=models.CASCADE)

# class that defines a mapping [user] -> [recipe]
class User_Recipe(models.Model):
    user_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe_ID = models.ForeignKey(Recipe,on_delete=models.CASCADE)

# class that defines a mapping [Creator] -> [recipe]
class Creator_Recipe(models.Model):
    creator_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe_ID = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='recipe_creator')
    public = models.BooleanField(default=True)


class Recipe_Versions(models.Model):
    parent_ID = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='parent_recipe')
    recipe_ID = models.ForeignKey(Recipe, on_delete=models.CASCADE,related_name='child_recipe')
    version = models.PositiveIntegerField(default=0)