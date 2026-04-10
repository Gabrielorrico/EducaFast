import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST
from datetime import date

from .models import Cronograma, Disciplina, SessaoEstudo

DIAS = [0, 1, 2, 3, 4]   # segunda a sexta
NUM_SLOTS = 4             # quantidade de linhas da grade 


@login_required
def listar_cronogramas(request):
    cronograma_ativo = Cronograma.objects.filter(
        aluno=request.user, ativo=True
    ).first()

    if not cronograma_ativo:
        cronograma_ativo = Cronograma.objects.create(
            aluno=request.user,
            titulo='Meu Cronograma',
            data_inicio=date.today(),
            data_fim=date.today().replace(month=12, day=31),
            ativo=True,
        )

    return redirect('cronograma:detalhe', cronograma_id=cronograma_ativo.id)


@login_required
def detalhe_cronograma(request, cronograma_id):
    cronograma = get_object_or_404(Cronograma, id=cronograma_id, aluno=request.user)

    sessoes_qs = (
        SessaoEstudo.objects
        .filter(cronograma=cronograma)
        .select_related('disciplina')
        .order_by('dia_semana', 'slot_horario')
    )

    sessoes_map = {
        (s.dia_semana, s.slot_horario): s for s in sessoes_qs
    }
    grade = []
    for slot in range(NUM_SLOTS):
        linha = []
        for dia in DIAS:
            linha.append(sessoes_map.get((dia, slot), None))
        grade.append({'slot': slot, 'celulas': linha})

    dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']

    return render(request, 'cronograma/detalhe.html', {
        'cronograma': cronograma,
        'grade': grade,
        'dias_semana': dias_semana,
        'disciplinas': Disciplina.objects.all().order_by('nome'),
        'num_slots': range(NUM_SLOTS),
        'tipo_choices': SessaoEstudo.TIPO_CHOICES,
        'prioridade_choices': SessaoEstudo.PRIORIDADE_CHOICES,
    })


@login_required
@require_POST
def criar_sessao(request, cronograma_id):
    cronograma = get_object_or_404(Cronograma, id=cronograma_id, aluno=request.user)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)

    dia = data.get('dia_semana')
    slot = data.get('slot_horario')
    if dia is None or slot is None:
        return JsonResponse({'erro': 'dia_semana e slot_horario são obrigatórios'}, status=400)

    if SessaoEstudo.objects.filter(cronograma=cronograma, dia_semana=dia, slot_horario=slot).exists():
        return JsonResponse({'erro': 'Já existe uma sessão nesse slot'}, status=409)

    sessao = SessaoEstudo.objects.create(
        cronograma=cronograma,
        disciplina_id=data.get('disciplina_id'),
        dia_semana=dia,
        slot_horario=slot,
        descricao_atividade=data.get('descricao_atividade', ''),
        tipo=data.get('tipo', 'exercicio'),
        prioridade=data.get('prioridade'), 
    )

    return JsonResponse({
        'id': sessao.id,
        'dia_semana': sessao.dia_semana,
        'slot_horario': sessao.slot_horario,
        'disciplina': sessao.disciplina.nome if sessao.disciplina else None,
        'cor_hex': sessao.disciplina.cor_hex if sessao.disciplina else '#888888',
        'descricao_atividade': sessao.descricao_atividade,
        'tipo': sessao.get_tipo_display(),
        'concluida': sessao.concluida,
        'prioridade': sessao.prioridade,
    }, status=201)


@login_required
@require_http_methods(['PATCH'])
def concluir_sessao(request, sessao_id):
    sessao = get_object_or_404(
        SessaoEstudo, id=sessao_id, cronograma__aluno=request.user
    )
    sessao.concluida = not sessao.concluida
    sessao.save(update_fields=['concluida'])
    return JsonResponse({'id': sessao.id, 'concluida': sessao.concluida})


@login_required
@require_http_methods(['DELETE'])
def deletar_sessao(request, sessao_id):
    sessao = get_object_or_404(
        SessaoEstudo, id=sessao_id, cronograma__aluno=request.user
    )
    sessao.delete()
    return JsonResponse({'status': 'deletado'})