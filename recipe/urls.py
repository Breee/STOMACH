from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^initUnit/$', views.initialize_Units, name='initUnits'),
    url(r'^initCategories/$', views.initialize_Categories, name='initCategories'),
    # recipe related stuff
    url(r'^$', views.recipes_list, name='recipes_list'),
    url(r'^user/$', views.recipes_user, name='recipes_user'),
    # ex: /stomach/5/
    url(r'^(?P<recipe_id>[0-9]+)/$', views.recipe_detail, name='recipe_detail'),
    url(r'^new/$', views.recipe_new, name='recipe_new'),
    url(r'^(?P<recipe_id>[0-9]+)/edit/$', views.recipe_edit, name='recipe_edit'),
    url(r'^(?P<recipe_id>[0-9]+)/remove/$', views.recipe_hide, name='recipe_hide'),
    url(r'^$', views.redirect_to_recipes_list, name='redirect_to_recipes_list'),
]


