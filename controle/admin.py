from django.contrib import admin
from .models import Categoria, Conta, Transacao

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'usuario')
    list_filter = ('tipo', 'usuario')
    search_fields = ('nome',)

@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'saldo', 'usuario')
    list_filter = ('usuario',)
    search_fields = ('nome',)

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'categoria', 'conta', 'usuario')
    list_filter = ('data', 'categoria', 'conta', 'usuario')
    search_fields = ('descricao', 'observacao')
    date_hierarchy = 'data'
