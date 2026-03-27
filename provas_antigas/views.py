# provas_antigas/views.py
from django.shortcuts import render
from .models import Prova  # ou como você nomeou o model

def index(request):
    provas = Prova.objects.all()

    # Filtros opcionais via GET
    ano = request.GET.get('ano')
    edicao = request.GET.get('edicao')
    tipo = request.GET.get('tipo')
    area = request.GET.get('area_conhecimento')

    if ano:
        provas = provas.filter(ano=ano)
    if edicao:
        provas = provas.filter(edicao=edicao)
    if tipo:
        provas = provas.filter(tipo=tipo)
    if area:
        provas = provas.filter(area_conhecimento=area)

    context = {
        'provas': provas,
        'anos_disponiveis': Prova.objects.values_list('ano', flat=True).distinct().order_by('-ano'),
        'areas_disponiveis': Prova.objects.values_list('area_conhecimento', flat=True).distinct(),
    }

    return render(request, 'provas_antigas/index.html', context)