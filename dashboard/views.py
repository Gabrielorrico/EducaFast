from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sessaodeestudos.models import SessaoDeEstudos
from django.db.models import Sum

@login_required
def index(request):
    return render(request, 'dashboard/index.html')

def dashboard(request):
    # Últimas sessões de estudo
    ultimas_sessoes = SessaoDeEstudos.objects.filter(
        usuario=request.user
    ).select_related('materia').order_by('-iniciada_em')[:5]

    # Tempo total geral estudado pelo usuário
    tempo_total = SessaoDeEstudos.objects.filter(
        usuario=request.user
    ).aggregate(total=Sum('duracao_segundos'))['total'] or 0

    context = {
        # contexto existente 
        'ultimas_sessoes': ultimas_sessoes,
        'tempo_total_estudo': tempo_total,
    }
    return render(request, 'dashboard/dashboard.html', context)

