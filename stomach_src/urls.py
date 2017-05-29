from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^initUnit/$', views.initialize_Units, name='initUnits'),
    url(r'^initCategories/$', views.initialize_Categories, name='initCategories'),
    # recipe related stuff
    url(r'^recipes/$', views.recipes_list, name='recipes_list'),
    url(r'^recipes/(?P<message>\w+)$', views.recipes_list, name='recipes_list'),
    url(r'^recipes/user/$', views.recipes_user, name='recipes_user'),
    # ex: /stomach/5/
    url(r'^recipes/(?P<recipe_id>[0-9]+)/$', views.recipe_detail, name='recipe_detail'),
    url(r'^recipes/new/$', views.recipe_new, name='recipe_new'),
    url(r'^recipes/(?P<recipe_id>[0-9]+)/edit/$', views.recipe_edit, name='recipe_edit'),
    url(r'^recipes/(?P<recipe_id>[0-9]+)/remove/$', views.recipe_hide, name='recipe_hide'),
    url(r'^recipes/$', views.redirect_to_recipes_list, name='redirect_to_recipes_list'),
    # storage related stuff
    url(r'^storage/$', views.storage_list, name='user_storage'),
    url(r'^storage/new/$', views.storage_new, name='storage_new'),
    url(r'^storage/(?P<storage_id>[0-9]+)$', views.storage_detail, name='storage_detail'),
    url(r'^storage/(?P<storage_id>[0-9]+)/edit/$', views.storage_edit, name='storage_edit'),
    url(r'^storage/(?P<storage_id>[0-9]+)/delete/$', views.storage_delete, name='storage_delete'),

]

