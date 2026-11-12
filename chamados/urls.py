from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='chamados/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('meus-chamados/', views.lista_chamados_solicitante, name='lista_chamados_solicitante'),
    path('novo/', views.novo_chamado_solicitante, name='novo_chamado_solicitante'),
    path('fila/', views.fila_chamados_tecnico, name='fila_chamados_tecnico'),
    path('assumir/<int:chamado_id>/', views.assumir_chamado, name='assumir_chamado'),
    path('resolver/<int:chamado_id>/', views.resolver_chamado, name='resolver_chamado'),
    path('noc/dashboard/', views.dashboard_noc, name='dashboard_noc'),

    #CRUD Equipamentos
    path('noc/equipamentos/', views.lista_equipamentos, name='lista_equipamentos'),
    path('noc/equipamentos/novo/', views.novo_equipamento, name='novo_equipamento'),
    path('noc/equipamentos/editar/<int:id>/', views.editar_equipamento, name='editar_equipamento'),
    path('noc/equipamentos/excluir/<int:id>/', views.excluir_equipamento, name='excluir_equipamento'),

    # CRUD Locais
    path('noc/locais/', views.lista_locais, name='lista_locais'),
    path('noc/locais/novo/', views.novo_local, name='novo_local'),
    path('noc/locais/editar/<int:id>/', views.editar_local, name='editar_local'),
    path('noc/locais/excluir/<int:id>/', views.excluir_local, name='excluir_local'),

    # CRUD Tipos de Ocorrência
    path('noc/tipos/', views.lista_tipos, name='lista_tipos'),
    path('noc/tipos/novo/', views.novo_tipo, name='novo_tipo'),
    path('noc/tipos/editar/<int:id>/', views.editar_tipo, name='editar_tipo'),
    path('noc/tipos/excluir/<int:id>/', views.excluir_tipo, name='excluir_tipo'),
]   