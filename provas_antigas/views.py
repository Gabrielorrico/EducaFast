from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .models import Prova


@login_required
def index(request):
    provas = Prova.objects.all()

    # PEGAR FILTROS
    ano = request.GET.get('ano')
    edicao = request.GET.get('edicao')
    tipo = request.GET.get('tipo')
    area = request.GET.get('area_conhecimento')

    # APLICAR FILTROS
    if ano:
        provas = provas.filter(ano=ano)

    if edicao:
        provas = provas.filter(edicao=edicao)

    if tipo:
        provas = provas.filter(tipo=tipo)

    if area:
        provas = provas.filter(area_conhecimento=area)

    # ORDENAÇÃO (importante para UX)
    provas = provas.order_by('-ano')

    # PROVAS POPULARES (simples por enquanto)
    provas_populares = Prova.objects.order_by('-ano')[:4]

    # DADOS PARA FILTROS
    anos_disponiveis = (
        Prova.objects
        .values_list('ano', flat=True)
        .distinct()
        .order_by('-ano')
    )

    areas_disponiveis = (
        Prova.objects
        .values_list('area_conhecimento', flat=True)
        .distinct()
    )

    context = {
        'provas': provas,
        'provas_populares': provas_populares,
        'anos_disponiveis': anos_disponiveis,
        'areas_disponiveis': areas_disponiveis,
    }

    return render(request, 'provas_antigas/index.html', context)


@login_required
def detalhe(request, pk):
    prova = get_object_or_404(Prova, pk=pk)

    return render(request, 'provas_antigas/detalhe.html', {
        'prova': prova
    })


# 🔥 OPCIONAL (recomendado): DOWNLOAD CONTROLADO
@login_required
def baixar_prova(request, pk):
    prova = get_object_or_404(Prova, pk=pk)

    if prova.pdf_prova:
        return FileResponse(
            prova.pdf_prova.open(),
            as_attachment=True,
            filename=f'ENEM_{prova.ano}_{prova.edicao}.pdf'
        )

    return render(request, 'provas_antigas/detalhe.html', {
        'prova': prova,
        'erro': 'Arquivo não disponível'
    })