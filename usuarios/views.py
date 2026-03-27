from django.shortcuts import render
from django.contrib.auth import authenticate, login

def login_view(request):
    return render(request, 'usuarios/index.html')