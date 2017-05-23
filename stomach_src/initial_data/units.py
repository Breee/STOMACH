from stomach_src.recipe_calculator.unit import Unit
import csv


UNIT_DICT = None


def read_unit_csv(csvFile, language):
    with open(csvFile, mode='r') as infile:
        reader = csv.reader(infile)
        unit_id = 0
        header = []
        for row in reader:
            if unit_id == 0:
                header = row
            else:
                UNIT_DICT[unit_id] = Unit(unit_id,language,row[0],row[1],row[2],row[3])



read_unit_csv('units_GER.csv', 'GER')


