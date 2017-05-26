class RecipeCalculator(object):

    def recalculate_recipe(self, ingredients, defining_ingredient):
        """
        Function that recalculates a recipe according to a defining ingredient.
        ingredients is a dictiorary of the form {ing_0: value_1, ...,ing_n: value_n}
        The defining ingredient is a tuple of the form (ing,val)
        
        :param ingredients: 
        :param defining_ingredient: 
        :return:
          
         >>> rc = RecipeCalculator()
         >>> ingredients = {'flour':500, 'eggs': 4}
         >>> defining_ingredient = ('eggs',2)
         >>> sorted(rc.recalculate_recipe(ingredients,defining_ingredient).items())
         [('eggs', 2.0), ('flour', 250.0)]
         
        """
        factor = self.calculate_factor(ingredients, defining_ingredient)

        return self.recalculate_ingredients(ingredients, factor)

    def calculate_factor(self, ingredients, defining_ingredient):
        """
        function that calculates a factor which is the relation between 
        the original value of an ingredient and the new one.
        :param ingredients: 
        :param defining_ingredient: 
        :return:
        >>> rc = RecipeCalculator()
        >>> ingredients = {'flour':500, 'eggs': 4}
        >>> defining_ingredient = ('eggs',2)
        >>> rc.calculate_factor(ingredients,defining_ingredient)
        2.0
        """

        defining_name = defining_ingredient[0]
        defining_value = defining_ingredient[1]

        try:
            original_value = ingredients[defining_name]
        except:
            raise KeyError("dictionary does not contain the key %s" % defining_name)

        return original_value / defining_value


    def recalculate_ingredients(self, ingredients, factor):
        """
        function that will divide all ingredient value by a factor
        :param ingredients: 
        :param factor: 
        :return: 
        >>> rc = RecipeCalculator()
        >>> ingredients = {'flour':500, 'eggs': 4}
        >>> sorted(rc.recalculate_ingredients(ingredients,2.0).items())
        [('eggs', 2.0), ('flour', 250.0)]
        """
        result = dict()
        for ing, val in ingredients.items():
            result[ing] = val / factor

        return result
