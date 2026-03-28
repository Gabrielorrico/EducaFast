from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


    
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    erro = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

    if request.user.is_authenticated:
        return redirect('dashboard:index')

    erro = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('dashboard:index')
        else:
            erro = 'Usuário ou senha inválidos.'

    return render(request, 'usuarios/index.html', {'erro': erro})


def register_view(request):
    erro = None

    if request.method == 'POST':
        username  = request.POST.get('username')
        email     = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            erro = 'As senhas não coincidem.'
        elif User.objects.filter(username=username).exists():
            erro = 'Este nome de usuário já está em uso.'
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('dashboard:index')

    return render(request, 'usuarios/register.html', {'erro': erro})


def logout_view(request):
    logout(request)
    return redirect('login')


def index_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'usuarios/index.html')
