from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Prova

@login_required
def index(request):
    provas = Prova.objects.all()


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

    provas_populares = Prova.objects.order_by('-ano')[:4]

    context = {
        'provas': provas,
        'provas_populares': provas_populares, 
        'anos_disponiveis': Prova.objects.values_list('ano', flat=True).distinct().order_by('-ano'),
        'areas_disponiveis': Prova.objects.values_list('area_conhecimento', flat=True).distinct(),
    }

    return render(request, 'provas_antigas/index.html', context)

def detalhe(request, pk):
    prova = Prova.objects.get(pk=pk)
    return render(request, 'provas_antigas/detalhe.html', {'prova': prova})