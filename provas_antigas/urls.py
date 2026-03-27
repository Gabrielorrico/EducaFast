# provas_antigas/urls.py

from django.urls import path
from . import views

app_name = 'provas_antigas'

urlpatterns = [
    path('', views.index, name='index'),
]

