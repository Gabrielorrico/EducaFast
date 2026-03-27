import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum
from django.utils import timezone

from .models import Materia, SessaoDeEstudos


@login_required
def cronometro(request):
    """
    Renderiza a página principal do cronômetro de estudos.
    Lista todas as matérias disponíveis e as sessões recentes do usuário.
    """
    usuario = request.user

    materias = Materia.objects.all()

    # Últimas 5 sessões do usuário para exibição rápida
    sessoes_recentes = SessaoDeEstudos.objects.filter(
        usuario=usuario
    ).select_related('materia').order_by('-iniciada_em')[:5]

    # Tempo total por matéria (em segundos) para o usuário
    tempo_por_materia = (
        SessaoDeEstudos.objects
        .filter(usuario=usuario)
        .values('materia__nome', 'materia__icone', 'materia__cor')
        .annotate(total_segundos=Sum('duracao_segundos'))
        .order_by('-total_segundos')
    )

    context = {
        'materias': materias,
        'sessoes_recentes': sessoes_recentes,
        'tempo_por_materia': tempo_por_materia,
    }
    return render(request, 'sessaodeestudos/cronometro.html', context)


@login_required
@require_POST
def salvar_sessao(request):
    """
    Endpoint AJAX que recebe os dados da sessão finalizada e salva no banco, 
    ele espera um JSON com: materia_id (int) e duracao_segundos (int) e 
    retorna JSON com sucesso e os dados da sessão salva.
    """
    usuario = request.user

    try:
        dados = json.loads(request.body)
        materia_id = dados.get('materia_id')
        duracao_segundos = int(dados.get('duracao_segundos', 0))

        if not materia_id:
            return JsonResponse({'erro': 'Matéria não informada.'}, status=400)

        if duracao_segundos <= 0:
            return JsonResponse({'erro': 'Duração inválida. O cronômetro precisa marcar ao menos 1 segundo.'}, status=400)

        materia = get_object_or_404(Materia, pk=materia_id)

        sessao = SessaoDeEstudos.objects.create(
            usuario=usuario,
            materia=materia,
            duracao_segundos=duracao_segundos,
            iniciada_em=timezone.now(),
        )

        return JsonResponse({
            'sucesso': True,
            'sessao': {
                'id': sessao.id,
                'materia': materia.nome,
                'icone': materia.icone,
                'duracao': sessao.duracao_formatada,
                'data': sessao.iniciada_em.strftime('%d/%m/%Y %H:%M'),
            }
        })

    except (ValueError, KeyError) as e:
        return JsonResponse({'erro': f'Dados inválidos: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': 'Erro interno. Tente novamente.'}, status=500)


@login_required
def tempo_total_materia(request, materia_id):
    """
    Retorna o tempo total acumulado de um usuário em uma matéria específica.
    """
    usuario = request.user
    materia = get_object_or_404(Materia, pk=materia_id)
    resultado = SessaoDeEstudos.objects.filter(
        usuario=usuario,
        materia=materia
    ).aggregate(total=Sum('duracao_segundos'))

    total_segundos = resultado['total'] or 0
    horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60
    segundos = total_segundos % 60

    return JsonResponse({
        'materia': materia.nome,
        'total_segundos': total_segundos,
        'total_formatado': f'{horas:02d}:{minutos:02d}:{segundos:02d}',
    })


@login_required
def ultimas_sessoes_api(request):
    """
    Retorna as últimas sessões do usuário em JSON — usado pelo dashboard.
    """
    usuario = request.user
    sessoes = SessaoDeEstudos.objects.filter(
        usuario=usuario
    ).select_related('materia').order_by('-iniciada_em')[:10]

    dados = [
        {
            'materia': s.materia.nome,
            'icone': s.materia.icone,
            'duracao': s.duracao_formatada,
            'data': s.iniciada_em.strftime('%d/%m/%Y %H:%M'),
        }
        for s in sessoes
    ]

    return JsonResponse({'sessoes': dados})