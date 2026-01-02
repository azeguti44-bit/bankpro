python manage.py shell << END
from django.contrib.auth import get_user_model
from django.apps import apps
import random

User = get_user_model()
Account = apps.get_model('banco', 'Account')

def ajustar_ou_criar(username, nome, cpf, email, senha):
    user = User.objects.filter(username=username).first()
    if not user:
        # Se não existe, cria do zero
        user = User.objects.create_user(username=username, nome_completo=nome, cpf=cpf, email=email, password=senha)
        Account.objects.create(user=user, number=str(random.randint(100000, 999999)), account_type='corrente', balance=5000)
        Account.objects.create(user=user, number=str(random.randint(1000000, 9999999)), account_type='poupanca', balance=5000)
        print(f"Usuario {username} criado.")
    else:
        # Se já existe, apenas força a senha nova para garantir o acesso
        user.set_password(senha)
        user.save()
        print(f"Senha de {username} atualizada.")

# Ajustando o Supervisor
sup = User.objects.filter(username='supervisor').first()
if sup:
    sup.set_password('admin_senha123')
    sup.is_staff = True
    sup.is_superuser = True
    sup.save()
else:
    User.objects.create_superuser(username='supervisor', nome_completo='Admin', cpf='00000000000', email='a@a.com', password='admin_senha123')

# Ajustando os Clientes
ajustar_ou_criar('peter', 'Cliente Um', '29730565864', 'peter@gmail.com', 'senha123')
ajustar_ou_criar('hook', 'Cliente Dois', '55566677788', 'hook@gmail.com', 'senha123')
END