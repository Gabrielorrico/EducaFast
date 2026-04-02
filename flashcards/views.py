from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# ⚠️  Ajuste o caminho abaixo se a sua Materia estiver em outro app
from sessaodeestudos.models import Materia
from .models import Assunto, Flashcard


@login_required
def index(request):
    """Renderiza a página principal do app de flashcards."""
    materias = Materia.objects.all().order_by('nome')
    return render(request, 'flashcards/index.html', {'materias': materias})


@login_required
def api_assuntos(request, materia_id):
    """
    API: retorna os assuntos de uma matéria, com suporte a busca por query string.
    GET /flashcards/api/assuntos/<materia_id>/?q=<termo>
    """
    try:
        materia = Materia.objects.get(pk=materia_id)
    except Materia.DoesNotExist:
        return JsonResponse({'erro': 'Matéria não encontrada.'}, status=404)

    q = request.GET.get('q', '').strip()
    assuntos_qs = Assunto.objects.filter(materia=materia)

    if q:
        assuntos_qs = assuntos_qs.filter(nome__icontains=q)

    assuntos_data = [
        {
            'id': a.id,
            'nome': a.nome,
            'total': a.flashcards.count(),
        }
        for a in assuntos_qs
    ]

    return JsonResponse({
        'materia': {
            'id': materia.id,
            'nome': materia.nome,
            'icone': materia.icone,
            'cor': materia.cor,
        },
        'assuntos': assuntos_data,
        'busca': q,
    })


@login_required
def api_flashcards(request, assunto_id):
    """
    API: retorna o resumo e todos os flashcards de um assunto.
    GET /flashcards/api/flashcards/<assunto_id>/
    """
    try:
        assunto = Assunto.objects.select_related('materia').prefetch_related('flashcards').get(pk=assunto_id)
    except Assunto.DoesNotExist:
        return JsonResponse({'erro': 'Assunto não encontrado.'}, status=404)

    cards = list(assunto.flashcards.values('id', 'frente', 'verso', 'ordem'))

    if not cards:
        return JsonResponse(
            {'erro': f'Ainda não há flashcards disponíveis para "{assunto.nome}".'},
            status=404,
        )

    return JsonResponse({
        'assunto': {
            'id': assunto.id,
            'nome': assunto.nome,
            'resumo': assunto.resumo,
        },
        'materia': {
            'nome': assunto.materia.nome,
            'icone': assunto.materia.icone,
            'cor': assunto.materia.cor,
        },
        'flashcards': cards,
    })