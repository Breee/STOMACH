from django.conf.urls import include, url
from django.contrib import admin
urlpatterns = [
    url(r'^stomach/', include('stomach_src.urls')), #this line added
    url(r'^admin/', admin.site.urls),
]