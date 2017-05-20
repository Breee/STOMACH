from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^home$', views.home, name='home'),
    url(r'^recipes$', views.recipes, name='recipes'),
    url(r'^$', views.home, name='home'),
    # ex: /stomach/5/
    url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^recipe/new/$',views.recipe_new, name='recipe_new'),

]