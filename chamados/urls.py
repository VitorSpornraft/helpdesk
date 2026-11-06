from django.urls import path
from . import views

urlpatterns = [
    path('meus-chamados/', views.lista_chamados_solicitante, name='lista_chamados_solicitante'),
    path('novo/', views.novo_chamado_solicitante, name='novo_chamado_solicitante'),
    path('fila/', views.fila_chamados_tecnico, name='fila_chamados_tecnico'),
    path('assumir/<int:chamado_id>/', views.assumir_chamado, name='assumir_chamado'),
    path('resolver/<int:chamado_id>/', views.resolver_chamado, name='resolver_chamado'),
]   