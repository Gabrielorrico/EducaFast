from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_cronogramas, name='listar_cronogramas'),
]