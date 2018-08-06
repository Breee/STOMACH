from django.conf import settings
from django.db import models
from django.utils import timezone

from recipe.models import Ingredient, Unit

"""
#####################################################################
######################## STORAGE SECTION ############################
#####################################################################
"""


# class that defines a Storage model where users can index their ingredients available.
class Storage(models.Model):
    user_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    visible = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name + " (ID: %d)" % self.id


# class that defines a mapping [storage] -> [ingredients]
class Storage_Ingredient(models.Model):
    storage_ID = models.ForeignKey(Storage,on_delete=models.DO_NOTHING)
    # ingredient id
    ing_ID = models.ForeignKey(Ingredient,on_delete=models.DO_NOTHING)
    # amount of the ingredient
    amount = models.PositiveIntegerField(default=0)
    # unit of the ingredient
    unit = models.ForeignKey(Unit,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.ing_ID.name + " (STORAGE ID: %d)" % self.storage_ID.id
