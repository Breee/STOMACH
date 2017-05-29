from django.conf.urls import url
from . import views

urlpatterns = [
    # storage related stuff
    url(r'^$', views.storage_list, name='user_storage'),
    url(r'^new/$', views.storage_new, name='storage_new'),
    url(r'^(?P<storage_id>[0-9]+)$', views.storage_detail, name='storage_detail'),
    url(r'^(?P<storage_id>[0-9]+)/edit/$', views.storage_edit, name='storage_edit'),
    url(r'^(?P<storage_id>[0-9]+)/delete/$', views.storage_delete, name='storage_delete'),

]

