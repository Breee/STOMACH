from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import *

import utils.stomachDatabaseUtils as DBUtils
from recipe.forms import *
from .forms import *

"""
#########################################################
################### Storage Views #######################
#########################################################
"""

@login_required()
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

@login_required()
def storage_edit(request, storage_id):
    return HttpResponse("not implemented yet")

@login_required()
def storage_list(request):
    storage_list = Storage.objects.filter(user_ID=request.user.id, visible=True)
    context = {'storage_list': storage_list}
    return render(request,
                  'html/storage/storage_view.html',
                  context)

@login_required()
def storage_detail(request, storage_id):
    storage = get_object_or_404(Storage, id=storage_id, user_ID=request.user, visible=True)
    ingredients = Storage_Ingredient.objects.filter(storage_ID=storage_id)
    context = {'storage': storage, 'ingredients': ingredients}
    return render(request,
                  'html/storage/storage_detail.html',
                  context)

@login_required()
def storage_hide(request, storage_id):
    DBUtils.hide_storage(storage_id)
    return redirect_to_storage_list(request)


def redirect_to_storage_list(request):
    return redirect('user_storage')


"""
UTILS
"""
def not_authorized():
    return HttpResponse("You are not authorized to do that.")

