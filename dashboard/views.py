from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from sessaodeestudos.models import SessaoDeEstudos
from flashcards.models import Flashcard
from gamificacao.models import PerfilGamificacao

@login_required
def dashboard(request):

    ultimas_sessoes = SessaoDeEstudos.objects.filter(
        usuario=request.user
    ).order_by('-iniciada_em')[:5]

    total_segundos = SessaoDeEstudos.objects.filter(
        usuario=request.user
    ).aggregate(total=Sum('duracao_segundos'))['total'] or 0

    horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60

    tempo_formatado = f"{horas}h {minutos}m"

    flashcards_estudados = request.user.flashcards_estudados.count()

    # GAMIFICAÇÃO
    perfil, _ = PerfilGamificacao.objects.get_or_create(
        usuario=request.user
    )

    xp_total = perfil.xp_total

    nivel = (xp_total // 100) + 1
    xp_no_nivel_atual = xp_total % 100
    percentual_nivel = xp_no_nivel_atual

    context = {
        'ultimas_sessoes': ultimas_sessoes,
        'tempo_total': tempo_formatado,
        'flashcards_estudados': flashcards_estudados,

        # gamificação
        'xp_total': xp_total,
        'nivel': nivel,
        'xp_no_nivel_atual': xp_no_nivel_atual,
        'percentual_nivel': percentual_nivel,
    }

    return render(request, 'dashboard/index.html', context)