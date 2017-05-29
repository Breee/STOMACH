import re

def clean(request):
    # convert post data from a querydict to a dict where values are lists.
    dataDict = dict(request.POST.lists())
    print(dataDict)

    name = ""
    cook_time = ""
    person_amount = ""
    description = ""
    public = True
    ingredients = dict()
    categories = []
    matcher = re.compile(r'form-(\d+)-(.*)')
    for key,value in dataDict.items():
        if key == 'name':
            name=value[0]
        elif key == 'person_amount':
            person_amount = value[0]
        elif key == 'description':
            description = value[0]
        elif key == 'cook_time':
            cook_time = value[0]
        elif matcher.match(key):
            matches = matcher.findall(key)
            ID = matches[0][0]
            name = matches[0][1]
            print(matches)

            if name == 'name':
                if ID not in ingredients:
                    ingredients[ID] = dict()
                ingredients[ID][name] = value
            elif name == 'amount':
                if ID not in ingredients:
                    ingredients[ID] = dict()
                ingredients[ID][name] = value
            elif name == 'unit':
                if ID not in ingredients:
                    ingredients[ID] = dict()
                ingredients[ID][name] = value
            elif name == 'category':
                categories.append(value)

    print(ingredients)
    print(categories)

