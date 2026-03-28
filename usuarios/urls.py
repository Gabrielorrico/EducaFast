from django.urls import path
from .views import login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('',          views.login_view,    name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/',   views.logout_view,   name='logout'),
]