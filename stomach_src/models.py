from django.db import models

class Recipe(models.Model):
    BF = "breakfast"
    BR = "brunch"
    LU = "lunch"
    CATEGORY_CHOICES = (
        (BF, "breakfast"),
        (BR, "brunch"),
        (LU, "lunch"))

    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    category = models.CharField(max_length=200,choices=CATEGORY_CHOICES, default=BF)
    description = models.CharField(max_length=1000)
    cook_time = models.PositiveIntegerField(default=0)
    person_amount = models.PositiveIntegerField(default=1)
    #tag_recipe_ID

    def __str__(self):
        return self.name + " (ID: %d)" % self.id

class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Ing_Recipe(models.Model):
    G = "grams(g)"
    KG = "kilograms(kg)"
    L = "litre(l)"
    UNIT_CHOICES = (
        (G, "grams(g)"),
        (KG, "kilograms(kg)"),
        (L, "litre(l)"))
    recipe_ID = models.ForeignKey(Recipe)
    ing_ID = models.ForeignKey(Ingredient)
    value = models.PositiveIntegerField(default=1)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)

