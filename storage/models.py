from recipe.models import *


"""
#####################################################################
######################## STORAGE SECTION ############################
#####################################################################
"""

# class that defines a Storage model where users can index their ingredients available.
class Storage(models.Model):
    user_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " (ID: %d)" % self.id

# class that defines a mapping [storage] -> [ingredients]
class Storage_Ingredient(models.Model):
    storage_ID = models.ForeignKey(Storage)
    # ingredient id
    ing_ID = models.ForeignKey(Ingredient)
    # amount of the ingredient
    amount = models.PositiveIntegerField(default=0)
    # unit of the ingredient
    unit = models.ForeignKey(Unit)

    def __str__(self):
        return self.ing_ID.name + " (STORAGE ID: %d)" % self.storage_ID.id
