from django.conf.urls import include, url
from account.views import *

urlpatterns = [
    url(r'^', account_form, name='myaccount'),
]
