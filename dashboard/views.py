from django.shortcuts import render
from django.db.models import Sum
from sessaodeestudos.models import SessaoDeEstudos

def dashboard(request):
    # últimas sessões (já ordenado no model, mas garantimos)
    ultimas_sessoes = SessaoDeEstudos.objects.filter(
        usuario=request.user
    ).order_by('-iniciada_em')[:5]

    # soma total de tempo estudado
    total_segundos = SessaoDeEstudos.objects.filter(
        usuario=request.user
    ).aggregate(total=Sum('duracao_segundos'))['total'] or 0

    # converter para horas/minutos
    horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60

    tempo_formatado = f"{horas}h {minutos}m"

    context = {
        'ultimas_sessoes': ultimas_sessoes,
        'tempo_total': tempo_formatado,
    }

    return render(request, 'dashboard/index.html', context)