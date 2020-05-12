# -*- encoding=utf-8 -*-

from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'.+', views.GateWay.as_view()),
]
