from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
urlpatterns = [
    url(r'^login/$', auth_views.login,{'template_name': 'html/registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page': '/stomach/home' }, name='logout'),
    url(r'^stomach/', include('stomach_src.urls')), #this line added
    url(r'^admin/', admin.site.urls),
]