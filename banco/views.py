from django.shortcuts import render
from .models import Account, Transaction
from .forms import CadastroUsuarioForm, TransferenciaentrecontasForm 
from django.shortcuts import redirect
import random
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages 
from django.db import transaction # Importante para segurança financeira

# View simples para listar contas
@login_required
def account_list(request):
    # O Pulo do Gato: Filtramos as contas onde o 'user' é o usuário logado
    if request.user.is_staff:
        # 1. Pegamos todas as contas
        # 2. Excluímos (.exclude) as contas que pertencem ao usuário que está logado agora
        # 3. (Opcional) Também excluímos outros staffs para a lista ficar só com clientes
        accounts = Account.objects.all().exclude(user=request.user).filter(user__is_staff=False).order_by('user__nome_completo')
    else:
        # Se for cliente comum, vê apenas as DELE (Corrente e Poupança)
        accounts = Account.objects.filter(user=request.user)
    
    return render(request, 'banco/account_list.html', {'accounts': accounts})

# View simples para listar transações
@login_required
def transaction_list(request, account_id=None):  # <--- Adicione o '=None'
    if account_id:
        # Se veio um ID (clique no botão do Staff ou do Usuário)
        if request.user.is_staff:
            transactions = Transaction.objects.filter(account_id=account_id).order_by('-timestamp')
        else:
            transactions = Transaction.objects.filter(
                account_id=account_id, 
                account__user=request.user
            ).order_by('-timestamp')
    else:
        # Se NÃO veio ID (acesso direto pela URL /transactions/)
        # Mostra todas as transações de TODAS as contas do usuário logado
        transactions = Transaction.objects.filter(account__user=request.user).order_by('-timestamp')

    return render(request, 'banco/transaction_list.html', {'transactions': transactions})

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            # 1. Salva o usuário
            usuario = form.save()
            
            # Função interna para gerar número único (evita repetição de código)
            def gerar_numero_unico():
                numero = str(random.randint(100000, 999999))
                while Account.objects.filter(number=numero).exists():
                    numero = str(random.randint(100000, 999999))
                return numero
            
            # 2. Cria a Conta Corrente
            Account.objects.create(
                user=usuario,
                number=gerar_numero_unico(),
                account_type='corrente',
                balance=0.00
            )
            
            # 3. Cria a Conta Poupança
            Account.objects.create(
                user=usuario,
                number=gerar_numero_unico(),
                account_type='poupanca',
                balance=0.00
            )
            
            return redirect('login')
    else:
        form = CadastroUsuarioForm()
    
    return render(request, 'banco/cadastrar_usuario.html', {'form': form})


@login_required
def extrato(request):
    if request.user.is_staff:
        # Admin vê todas as transações de todos
        transactions = Transaction.objects.all().order_by('-date')
    else:
        # Cliente vê apenas as transações da sua conta
        transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    
    return render(request, 'banco/transaction_list.html', {'transactions': transactions})




def entrance(request):
    return render(request, 'banco/entrance.html')



@login_required
def transferir(request):
    if request.user.is_staff:
        messages.warning(request, "Administradores não realizam transferências.")
        return redirect('account_list')

    if request.method == 'POST':
        form = TransferenciaentrecontasForm(request.POST, user=request.user)
        if form.is_valid():
            dados = form.cleaned_data
            conta_origem = dados['conta_origem']
            valor = dados['valor']

            try:
                conta_destino = Account.objects.get(
                    number=dados['numero_conta_destino'],
                    account_type=dados['tipo_conta_destino'],
                    user__cpf=dados['cpf_destino']
                )

                if conta_origem == conta_destino:
                    messages.warning(request, "Você não pode transferir para a mesma conta de origem.")
                
                elif conta_origem.balance < valor:
                    messages.warning(request, "Saldo insuficiente para esta transferência.")
                    return render(request, 'banco/transferir.html', {'form': form})

                else:
                    # TUDO OK! Iniciamos a transação bancária
                    with transaction.atomic():
                        # 1. Atualização dos Saldos
                        conta_origem.balance -= valor
                        conta_origem.save()

                        conta_destino.balance += valor
                        conta_destino.save()

                        # 2. REGISTRO NO EXTRATO DE QUEM ENVIOU (Peter Pan)
                        Transaction.objects.create(
                            account=conta_origem,
                            transaction_type='SAQUE',  # Ou 'TRANSFERENCIA_ENVIADA'
                            amount=valor,
                            description=f"Transferência enviada para {conta_destino.user.nome_completo or conta_destino.user.username}"
                        )

                        # 3. REGISTRO NO EXTRATO DE QUEM RECEBEU (Destinatário)
                        # É aqui que a mágica acontece para o outro usuário ver no extrato dele!
                        Transaction.objects.create(
                            account=conta_destino,
                            transaction_type='DEPOSITO',  # Ou 'TRANSFERENCIA_RECEBIDA'
                            amount=valor,
                            description=f"Transferência recebida de {conta_origem.user.nome_completo or conta_origem.user.username}"
                        )
                    
                    messages.success(request, f"Sucesso! R$ {valor} enviados para {conta_destino.user.nome_completo}.")
                    return redirect('account_list')

            except Account.DoesNotExist:
                messages.error(request, "Destinatário não encontrado. Confira CPF, Número e Tipo da conta.")
    else:
        form = TransferenciaentrecontasForm(user=request.user)

    return render(request, 'banco/transferir.html', {'form': form})