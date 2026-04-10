import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import Materia, Topico, TopicoMarcado


@login_required
def assuntos_recorrentes(request):

    materias = Materia.objects.prefetch_related("topicos").all()

    ids_marcados = set(
        TopicoMarcado.objects.filter(usuario=request.user).values_list(
            "topico_id", flat=True
        )
    )

    return render(
        request,
        "assuntos_recorrentes/index.html",
        {
            "materias": materias,
            "ids_marcados": ids_marcados,
        },
    )


@login_required
@require_POST
def toggle_topico(request):

    try:
        data = json.loads(request.body)
        topico_id = int(data["topico_id"])
    except (KeyError, ValueError, json.JSONDecodeError):
        return JsonResponse({"erro": "Dados inválidos."}, status=400)

    # Verifica se o tópico existe
    try:
        topico = Topico.objects.get(pk=topico_id)
    except Topico.DoesNotExist:
        return JsonResponse({"erro": "Tópico não encontrado."}, status=404)

    marcacao, criado = TopicoMarcado.objects.get_or_create(
        usuario=request.user, topico=topico
    )

    if not criado:
        marcacao.delete()
        return JsonResponse({"marcado": False})

    return JsonResponse({"marcado": True})