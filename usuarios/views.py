from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            return render(request, 'usuarios/index.html', {'erro': 'Login inválido'})

    return render(request, 'usuarios/index.html')