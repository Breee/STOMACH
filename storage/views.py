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
            storage_form = StorageForm()
            ingredient_formset = formset_factory(IngredientForm)
            context = {
                'storage_form': storage_form, 'ingredient_formset': ingredient_formset,
                'edit': False
            }
            return render(request,
                          'html/storage/storage_new.html',
                          context)
        else:
            message = "Only logged in users can create new storages."
            context = {'notAuthorized': message}
            return render(request,
                          'html/storage/storage_view.html',
                          context)


def storage_edit(request, storage_id):
    storagecontext = DBUtils.get_storage_details(storage_id,request.user.id,request.user.is_superuser)

    storage = storagecontext['storage']
    ingredients = storagecontext['ingredients']

    if request.method == "POST":
        DBUtils.hide_storage(storage_id)
        newID = DBUtils.create_new_storage(request)
        message = "Thanks, your storage was edited"
        context = {'success': message, 'id': newID}

        return render(request,
                      'html/storage/storage_new.html',
                      context)
    else:

        storage_form = StorageForm(initial={'name':storage.name})
        ingredient_formset = formset_factory(IngredientForm, extra=0)


        # fill ingredient forms.
        filled_ing = ingredient_formset(
            initial=[{'unit': x.unit, 'name': x.ing_ID, 'amount': x.amount} for x in ingredients])


        context = {
            'storage_form':storage_form, 'ingredient_formset': filled_ing, 'edit': True
        }

        return render(request,
                      'html/storage/storage_new.html',
                      context)


def storage_list(request):
    storage_list = Storage.objects.filter(user_ID=request.user.id, visible=True)
    context = {'storage_list': storage_list}
    return render(request,
                  'html/storage/storage_view.html',
                  context)


def storage_detail(request, storage_id):
    storage = get_object_or_404(Storage, id=storage_id, user_ID=request.user, visible=True)
    ingredients = Storage_Ingredient.objects.filter(storage_ID=storage_id)
    context = {'storage': storage, 'ingredients': ingredients}
    return render(request,
                  'html/storage/storage_detail.html',
                  context)


def storage_hide(request, storage_id):
    DBUtils.hide_storage(storage_id)
    return redirect_to_storage_list(request)


def redirect_to_storage_list(request):
    return redirect('user_storage')
