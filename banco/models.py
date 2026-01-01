from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    # Opcional: Você pode sobrescrever ou adicionar um campo de nome completo
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")

    def __str__(self):
        return f"{self.nome_completo} ({self.cpf})"


class Account(models.Model):
    TIPOS_CONTA = [
        ('corrente', 'Conta Corrente'),
        ('poupanca', 'Conta Poupança'),
    ]

    # Mudamos de OneToOneField para ForeignKey
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='contas')
    number = models.CharField(max_length=10, unique=True, verbose_name="Número da Conta")
    account_type = models.CharField(max_length=10, choices=TIPOS_CONTA, default='corrente')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.nome_completo} - {self.get_account_type_display()}"

# 3. Classe para o histórico de movimentações
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'deposito'),
        ('withdrawal', 'Saque'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transacoes')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, null=True, blank=True) # Adicione esta linha