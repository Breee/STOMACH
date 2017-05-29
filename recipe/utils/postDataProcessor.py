import re
from stomach_src.models import *

def clean_recipe_post_data(request):
    # convert post data from a querydict to a dict where values are lists.
    dataDict = dict(request.POST.lists())
    print(dataDict)
    result = dict()
    result['public'] = False
    ingredients = dict()
    categories = set()
    matcher = re.compile(r'form-(\d+)-(.*)')
    for key,value in dataDict.items():
        if key == 'name':
            result['name'] = value[0]
        elif key == 'person_amount':
            result['person_amount'] = value[0]
        elif key == 'description':
            result['description'] = value[0]
        elif key == 'cook_time':
            result['cook_time'] = value[0]
        elif key == 'public':
            if value == 'on':
                result['public'] = True
            else:
                result['public'] = False
        elif matcher.match(key):
            matches = matcher.findall(key)
            ID = matches[0][0]
            name = matches[0][1]
            print(matches)
            if name == 'category':
                categories.add(value[0])
            else:
                if ID not in ingredients:
                    ingredients[ID] = dict()
                ingredients[ID][name] = value[0]
    result['ingredients'] = ingredients
    result['categories'] = categories
    print(result)
    return result

