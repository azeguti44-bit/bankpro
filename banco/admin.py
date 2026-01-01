from django.contrib import admin
from .models import Account, Transaction, Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # Colunas que aparecerão na lista de usuários
    list_display = ('username', 'nome_completo', 'cpf', 'email', 'is_staff')
    # Permite pesquisar pelo nome ou CPF no topo da página
    search_fields = ('username', 'nome_completo', 'cpf')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('number', 'user', 'account_type', 'balance')
    # Adiciona um filtro lateral por tipo de conta
    list_filter = ('account_type',)
    search_fields = ('number', 'user__nome_completo', 'user__cpf')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'amount', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')
    # Ordena pelas transações mais recentes
    ordering = ('-timestamp',)