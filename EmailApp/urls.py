from django.conf.urls import url
from EmailApp import views

from django.conf import settings

urlpatterns=[
    url(r'^emailinfo$',views.emailInfoApi),
    url(r'^emailinfo/([0-9]+)$',views.emailInfoApi),
]