python manage.py shell << END
from django.contrib.auth import get_user_model
from django.apps import apps
import random

User = get_user_model()
Account = apps.get_model('banco', 'Account')

def garantir_usuario(username, nome, cpf, email, senha):
    # Procura pelo username. Se achar, atualiza. Se não, cria.
    user, created = User.objects.update_or_create(
        username=username,
        defaults={'nome_completo': nome, 'cpf': cpf, 'email': email}
    )
    user.set_password(senha)
    user.save()

    # Se o usuário foi criado agora, damos o saldo inicial
    if created:
        Account.objects.create(user=user, number=str(random.randint(100, 999)), account_type='corrente', balance=5000)
        Account.objects.create(user=user, number=str(random.randint(1000, 9999)), account_type='poupanca', balance=5000)
        print(f"Usuario {username} criado com saldo.")
    else:
        print(f"Usuario {username} ja existia. Dados e senha atualizados.")

# Garante o Supervisor
sup, _ = User.objects.update_or_create(
    username='supervisor', 
    defaults={'nome_completo': 'Admin', 'cpf': '00000000000', 'is_staff': True, 'is_superuser': True}
)
sup.set_password('admin_senha123')
sup.save()

# Garante os Clientes
garantir_usuario('peter', 'Peter Pan', '29730565864', 'peter@gmail.com', 'senha123')
garantir_usuario('hook', 'Capitão Gancho', '55566677788', 'hook@gmail.com', 'senha123')
END