from django.urls import path
from . import views

urlpatterns = [
    path('meus-chamados/', views.lista_chamados_solicitante, name='lista_chamados_solicitante'),
    path('novo/', views.novo_chamado_solicitante, name='novo_chamado_solicitante'),
]   