import re

def clean_post_data(request):
    """
    this is what post data (e.g. of a storage) looks like.
    {
      'form-MAX_NUM_FORMS': ['1000'],
      'form-0-name': ['yeast'],
      'form-TOTAL_FORMS': ['5'],
      'form-0-amount': ['50'],
      'form-1-unit': ['20'],
      'form-4-amount': ['100'],
      'form-0-unit': ['48'],
      'form-1-name': ['sugar'],
      'form-2-name': ['salt'],
      'form-3-name': ['flour'],
      'form-3-amount': ['20000'],
      'name': ['MyFancyStorage'],
      'form-MIN_NUM_FORMS': ['0'],
      'form-2-unit': ['20'],
      'form-4-unit': ['47'],
      'form-INITIAL_FORMS': ['5'],
      'form-2-amount': ['1000'],
      'form-1-amount': ['10000'],
      'form-4-name': ['onions'],
      'form-3-unit': ['20'],
      'csrfmiddlewaretoken': ['NiiwWECGd9YHFV6c5wXg72YzmgUI6KPkPcNPiur8AfghD0I3JhB0tqDzp07Nil8Y']
    }
    
    We convert it to a map of the following form:
    {
      'categories': set(),
      'public': False,
      'ingredients': {
                      '3': {'unit': '20', 'amount': '20000', 'name': 'flour'},
                      '4': {'unit': '47', 'name': 'onions', 'amount': '100'},
                      '0': {'unit': '48', 'amount': '50', 'name': 'yeast'},
                      '1': {'unit': '20', 'amount': '10000', 'name': 'sugar'},
                      '2': {'unit': '20', 'amount': '1000', 'name': 'salt'}
                      },
      'name': 'MyFancyStorage'
    }
    
    NOTE: there is for sure a django way to do it. yet i did not found a good way to do so for multiple forms.
    probably it is possible to send all forms separated. 
    anyway, the post data is so small that it does not really matter how it is processed for the moment.
    """

    # convert post data from a querydict to a dict where values are lists.
    dataDict = dict(request.POST.lists())
    print(dataDict)
    result = dict()
    result['public'] = False
    ingredients = dict()
    categories = set()
    # regex matcher with 2 groups, where (\d+) is an ID and (.*) a field name.
    # e.g. a match on ingredient-1-name would deliver the groups 1,name.
    matcher = re.compile(r'(?:category|ingredient)-(\d+)-(.*)')
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
            if value[0] == 'on':
                result['public'] = True
            else:
                result['public'] = False
        elif matcher.match(key):
            matches = matcher.findall(key)
            ID = matches[0][0]
            name = matches[0][1].lower()
            if name == '':
                continue
            elif name == 'category':
                categories.add(value[0])
            else:
                if ID not in ingredients:
                    ingredients[ID] = dict()
                ingredients[ID][name] = value[0]
    result['ingredients'] = ingredients
    result['categories'] = categories
    print(result)
    return result
