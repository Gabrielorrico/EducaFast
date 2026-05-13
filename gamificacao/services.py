from .models import PerfilGamificacao

XP_POR_FLASHCARD = 10       # XP ganho por flashcard marcado
XP_POR_SESSAO = 50          # XP ganho por sessão válida
TEMPO_MINIMO_SEGUNDOS = 300  # 5 minutos mínimos para ganhar XP


def conceder_xp_flashcard(usuario):
    """
    Chamada quando o usuário marca um flashcard como estudado.
    Retorna o novo total de XP
    """
    perfil, _ = PerfilGamificacao.objects.get_or_create(usuario=usuario)
    perfil.xp_total += XP_POR_FLASHCARD
    perfil.save()
    return perfil.xp_total


def conceder_xp_sessao(usuario, duracao_segundos):

    """
    Chamada quando o usuário finaliza uma sessão de estudos.
    Só concede XP se a duração for maior que o mínimo.
    Retorna (xp_concedido, mensagem)
    """
    if duracao_segundos < TEMPO_MINIMO_SEGUNDOS:
        return 0, 'Sessão muito curta. Estude pelo menos 5 minutos para ganhar XP.'

    perfil, _ = PerfilGamificacao.objects.get_or_create(usuario=usuario)
    perfil.xp_total += XP_POR_SESSAO
    perfil.save()
    return XP_POR_SESSAO, f'+{XP_POR_SESSAO} XP ganhos!'