from django.shortcuts import *
from django.contrib.auth.decorators import login_required

from django.forms import formset_factory

import recipe.utils.stomachDatabaseUtils as DBUtils

from .models import *
from .forms import *
from recipe.forms import *


"""
#########################################################
################### Storage Views #######################
#########################################################
"""


def storage_new(request):
    if request.method == "POST":
        DBUtils.create_new_storage(request)
        message = "Thanks, new storage added"
        context = {'success': message}
        return render(request,
                      'html/storage/storage_new.html',
                      context)
    else:
        if request.user.is_authenticated:
            storageForm = StorageForm()
            ingredientFormSet = formset_factory(IngredientForm)
            context = {
                'form': storageForm, 'ingredientFormset': ingredientFormSet,
                'edit': False
            }
            return render(request,
                          'html/storage/storage_new.html',
                          context)
        else:
            message = "Only logged in users can create new recipes."
            context = {'notAuthorized': message}
            return render(request,
                          'html/storage/storage_view.html',
                          context)


def storage_edit(request, storage_id):
    return HttpResponse("not implemented yet")


def storage_list(request):
    storage_list = Storage.objects.filter(user_ID=request.user.id)
    # context is a map with elements of the form (id -> iterable)
    # where the id is the name accessible in html templates.
    context = {'storage_list': storage_list}
    # render will replace the python code in the template with whatever you defined.
    return render(request,
                  'html/storage/storage_view.html',
                  context)


def storage_detail(request, storage_id):
    storage = get_object_or_404(Storage, id=storage_id, user_ID=request.user)
    ingredients = Storage_Ingredient.objects.filter(storage_ID=storage_id)
    context = {'storage': storage, 'ingredients': ingredients}
    return render(request,
                  'html/storage/storage_detail.html',
                  context)


def storage_delete(request, storage_id):
    try:
        Storage.objects.get(id=storage_id, user_ID=request.user.id).delete()
        message = "Storage %s has been deleted successfully"
    except:
        message = ""
    return redirect_storage_list(request)


def redirect_storage_list(request):
    return redirect('storage_list')


"""
UTILS
"""


def not_authorized():
    return HttpResponse("You are not authorized to do that.")

