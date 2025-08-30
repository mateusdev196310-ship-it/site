from django.urls import path
from . import views

app_name = 'controle'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('registro/', views.registro_usuario, name='registro'),
    
    # Categorias
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nova/', views.nova_categoria, name='nova_categoria'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/excluir/<int:pk>/', views.excluir_categoria, name='excluir_categoria'),
    
    # Contas
    path('contas/', views.lista_contas, name='lista_contas'),
    path('contas/nova/', views.nova_conta, name='nova_conta'),
    path('contas/editar/<int:pk>/', views.editar_conta, name='editar_conta'),
    path('contas/excluir/<int:pk>/', views.excluir_conta, name='excluir_conta'),
    
    # Transações
    path('transacoes/', views.lista_transacoes, name='lista_transacoes'),
    path('transacoes/nova/', views.nova_transacao, name='nova_transacao'),
    path('transacoes/editar/<int:pk>/', views.editar_transacao, name='editar_transacao'),
    path('transacoes/excluir/<int:pk>/', views.excluir_transacao, name='excluir_transacao'),
    
    # Relatórios
    path('relatorios/mensal/', views.relatorio_mensal, name='relatorio_mensal'),
    
    # AJAX
    path('ajax/criar-categoria/', views.ajax_criar_categoria, name='ajax_criar_categoria'),
    path('ajax/criar-conta/', views.ajax_criar_conta, name='ajax_criar_conta'),
]