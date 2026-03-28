from django.urls import path
from . import views

app_name = 'cronograma'

urlpatterns = [
    path('', views.listar_cronogramas, name='listar'),
    path('<int:cronograma_id>/', views.detalhe_cronograma, name='detalhe'),
    path('<int:cronograma_id>/sessao/criar/', views.criar_sessao, name='criar_sessao'),
    path('sessao/<int:sessao_id>/concluir/', views.concluir_sessao, name='concluir_sessao'),
    path('sessao/<int:sessao_id>/deletar/', views.deletar_sessao, name='deletar_sessao'),
]