from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^home$', views.home, name='home'),
    url(r'^recipes$', views.recipes, name='recipes'),
    url(r'^recipes/user$', views.recipe_user, name='user_recipes'),
    # ex: /stomach/5/
    url(r'^recipes/(?P<recipe_id>[0-9]+)/$', views.recipe_detail, name='recipe_detail'),
    url(r'^recipes/new/$',views.recipe_new, name='recipe_new'),
    url(r'^recipes/(?P<recipe_id>[0-9]+)/edit/$', views.recipe_edit, name='recipe_edit'),
url(r'^recipes/(?P<recipe_id>[0-9]+)/delete/$', views.recipe_delete, name='recipe_delete'),

]
