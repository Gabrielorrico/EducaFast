from django.urls import path
from . import views

app_name = 'sessaodeestudos'

urlpatterns = [
    # Página principal do cronômetro
    path('cronometro/', views.cronometro, name='cronometro'),

    # Endpoint AJAX para salvar sessão finalizada
    path('cronometro/salvar/', views.salvar_sessao, name='salvar_sessao'),

    # Endpoint AJAX para consultar tempo total de uma matéria
    path('cronometro/tempo-total/<int:materia_id>/', views.tempo_total_materia, name='tempo_total_materia'),

    # Endpoint AJAX para listar últimas sessões (para o dashboard)
    path('sessoes/recentes/', views.ultimas_sessoes_api, name='ultimas_sessoes_api'),
]
