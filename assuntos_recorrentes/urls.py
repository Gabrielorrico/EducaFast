from django.urls import path

from . import views

app_name = "assuntos_recorrentes"

urlpatterns = [
    # Página principal – lista todas as matérias e tópicos
    path("", views.assuntos_recorrentes, name="index"),

    # Endpoint AJAX – marca ou desmarca um tópico (POST)
    path("toggle/", views.toggle_topico, name="toggle_topico"),
]