from django.urls import path
from . import views

app_name = 'cronograma'

urlpatterns = [
    path('', views.listar_cronogramas, name='listar_cronogramas'),
]