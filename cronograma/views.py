from django.shortcuts import render
from .models import Cronograma

def listar_cronogramas(request):
    cronogramas = Cronograma.objects.all()
    return render(request, 'cronograma/cronograma.html', {
        'cronogramas': cronogramas
    })