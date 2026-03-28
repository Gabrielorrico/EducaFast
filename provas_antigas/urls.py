from django.urls import path
from . import views

app_name = 'provas_antigas'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detalhe, name='detalhe'),
    path('baixar/<int:pk>/', views.baixar_prova, name='baixar_prova'),
]