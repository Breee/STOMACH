import csv

from recipe.recipe_calculator.category import Category

from recipe.recipe_calculator.unit import Unit


class InitialValueManager(object):
    def __init__(self):
        self.__unit_dict = dict()
        self.__category_dict = dict()

    def read_unit_csv(self, csvFile, language):
        with open(csvFile, mode='r') as infile:
            reader = csv.reader(infile)
            unit_id = 0
            header = []
            for row in reader:
                print(row)
                if unit_id == 0:
                    header = row
                else:
                    self.__unit_dict[unit_id] = Unit(unit_id, language, row[0], row[1], row[2], row[3])
                unit_id += 1

    def read_category_csv(self, csvFile, language):
        with open(csvFile, mode='r') as infile:
            reader = csv.reader(infile)
            category_id = 0
            header = []
            for row in reader:
                print(row)
                if category_id == 0:
                    header = row
                else:
                    self.__category_dict[category_id] = Category(category_id, row[0], language)
                category_id += 1

    def get_unit_dict(self):
        return self.__unit_dict

    def get_category_dict(self):
        return self.__category_dict
