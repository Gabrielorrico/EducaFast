from django.urls import path

from . import views

app_name = "assuntos_recorrentes"

urlpatterns = [
    path("", views.assuntos_recorrentes, name="index"),

    path("toggle/", views.toggle_topico, name="toggle_topico"),
]