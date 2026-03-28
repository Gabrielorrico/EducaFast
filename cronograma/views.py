from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cronograma

@login_required
def listar_cronogramas(request):
    cronogramas = Cronograma.objects.all()
    return render(request, 'cronograma/cronograma.html', {
        'cronogramas': cronogramas
    })