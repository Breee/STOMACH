from django.db import models


# class for units like gram,litre,cups,ounces
class Unit(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# class for categories like breakfast, lunch, dinner...
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class for tags which shall be attached to recipes, e.g. flour, oven..
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class for recipes
class Recipe(models.Model):

    # name of the recipe
    name = models.CharField(max_length=200)

    # date on which the recipe is/shall be published.
    pub_date = models.DateTimeField('date published')

    # description of the recipe (how to cook xxx..)
    description = models.CharField(max_length=1000)

    # time to prepare/cook the recipe.
    cook_time = models.PositiveIntegerField(default=0)

    # amount of persons.
    person_amount = models.PositiveIntegerField(default=1)

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
    recipe_ID = models.ForeignKey(Recipe)

    # ingredient id
    ing_ID = models.ForeignKey(Ingredient)

    # amount of the ingredient
    amount = models.PositiveIntegerField(default=1)

    # unit of the ingredient
    unit = models.ForeignKey(Unit)

# class that defines a mapping [category] -> [recipe]
class Category_Recipe(models.Model):
    recipe_ID = models.ForeignKey(Recipe)
    category_ID = models.ForeignKey(Category)

# class that defines a mapping [tag] -> [recipe]
class Tag_Recipe(models.Model):
    recipe_ID = models.ForeignKey(Recipe)
    tag_ID = models.ForeignKey(Tag)

