from django.urls import path
from . import views

app_name = 'flashcards'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/assuntos/<int:materia_id>/', views.api_assuntos, name='api_assuntos'),
    path('api/flashcards/<int:assunto_id>/', views.api_flashcards, name='api_flashcards'),
]