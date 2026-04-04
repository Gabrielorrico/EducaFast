from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Perfil
from .forms import PerfilForm


@login_required
def perfil(request):
    perfil_obj, created = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil:perfil')
    else:
        form = PerfilForm(instance=perfil_obj)

    materia_preferida = perfil_obj.get_materia_preferida()

    return render(request, 'perfil/index.html', {
        'form': form,
        'perfil': perfil_obj,
        'materia_preferida': materia_preferida,
    })