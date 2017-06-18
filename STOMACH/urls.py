from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
import recipe.views

urlpatterns = [
    url(r'^login/', auth_views.login,
        {'template_name': 'html/registration/login.html'}, name='login'),
    url(r'^logout/', auth_views.logout,
        {'next_page': '/recipes'},
        name='logout'),
    url(r'^signup/', include('signup.urls')),
    url(r'^recipes/', include('recipe.urls')),
    url(r'^storage/', include('storage.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('account.urls')),
    url(r'^', recipe.views.redirect_to_recipes_list),
]
