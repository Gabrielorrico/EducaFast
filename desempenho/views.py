from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date, timedelta

from sessaodeestudos.models import SessaoDeEstudos
from flashcards.models import Flashcard

from gamificacao.models import PerfilGamificacao


def _formatar_tempo(segundos):
    """Converte segundos em string legível: '3h 05min' ou '45min'."""
    if not segundos:
        return '0min'
    h = segundos // 3600
    m = (segundos % 3600) // 60
    if h > 0:
        return f'{h}h {m:02d}min'
    return f'{m}min'


def _calcular_dias_consecutivos(usuario):
    """
    Calcula a sequência atual de dias consecutivos com pelo menos
    uma sessão de estudos registrada.
    Usa o campo iniciada_em do modelo SessaoDeEstudos — sem precisar
    de nenhuma coluna extra no banco de dados.
    """
    datas = set(
        SessaoDeEstudos.objects
        .filter(usuario=usuario)
        .values_list('iniciada_em__date', flat=True)
        .distinct()
    )

    if not datas:
        return 0

    hoje = date.today()
    # Se o usuário ainda não estudou hoje, a sequência começa em ontem
    inicio = hoje if hoje in datas else hoje - timedelta(days=1)

    contador = 0
    dia = inicio
    while dia in datas:
        contador += 1
        dia -= timedelta(days=1)

    return contador


# ──────────────────────────────────────────
# View
# ──────────────────────────────────────────

@login_required
def index(request):
    usuario = request.user
    perfil_gam, _ = PerfilGamificacao.objects.get_or_create(usuario=usuario)

    # ── Métricas gerais ───────────────────────────────────────────────────
    total_segundos = (
        SessaoDeEstudos.objects
        .filter(usuario=usuario)
        .aggregate(total=Sum('duracao_segundos'))['total'] or 0
    )
    tempo_total        = _formatar_tempo(total_segundos)
    total_sessoes      = SessaoDeEstudos.objects.filter(usuario=usuario).count()
    dias_consecutivos  = _calcular_dias_consecutivos(usuario)
    flashcards_estudados = usuario.flashcards_estudados.count()
    total_flashcards   = Flashcard.objects.count()

    # ── Tempo por matéria ─────────────────────────────────────────────────
    materias_qs = (
        SessaoDeEstudos.objects
        .filter(usuario=usuario)
        .values('materia__nome', 'materia__icone', 'materia__cor')
        .annotate(segundos=Sum('duracao_segundos'))
        .order_by('-segundos')
    )

    max_segundos = materias_qs[0]['segundos'] if materias_qs else 1

    tempo_por_materia = [
        {
            'nome':       m['materia__nome'],
            'icone':      m['materia__icone'],
            'cor':        m['materia__cor'],
            'formatado':  _formatar_tempo(m['segundos']),
            # percentual relativo ao maior valor (para a barra ficar proporcional)
            'percentual': round(m['segundos'] / max_segundos * 100),
        }
        for m in materias_qs
    ]

    # ── Últimas 5 sessões ─────────────────────────────────────────────────
    ultimas_sessoes = (
        SessaoDeEstudos.objects
        .filter(usuario=usuario)
        .select_related('materia')
        .order_by('-iniciada_em')[:5]
    )

    return render(request, 'desempenho/index.html', {
        'tempo_total':          tempo_total,
        'total_sessoes':        total_sessoes,
        'dias_consecutivos':    dias_consecutivos,
        'flashcards_estudados': flashcards_estudados,
        'total_flashcards':     total_flashcards,
        'tempo_por_materia':    tempo_por_materia,
        'ultimas_sessoes':      ultimas_sessoes,
        'xp_total': perfil_gam.xp_total,
        'nivel':    perfil_gam.nivel,
        'percentual_nivel': perfil_gam.percentual_nivel,
    })
