#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell << END
from django.contrib.auth import get_user_model
from django.apps import apps
import random

User = get_user_model()
Account = apps.get_model('banco', 'Account')

def criar_cliente(username, nome, cpf, email, senha):
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username=username, nome_completo=nome, cpf=cpf, email=email, password=senha)
        Account.objects.create(user=u, number=str(random.randint(100, 999)), account_type='corrente', balance=5000)
        Account.objects.create(user=u, number=str(random.randint(1000, 9999)), account_type='poupanca', balance=5000)

if not User.objects.filter(username='supervisor').exists():
    User.objects.create_superuser(username='supervisor', nome_completo='Admin', cpf='00000000000', email='a@a.com', password='admin_senha_123')

criar_cliente('usuario1', 'Cliente Um', '11122233344', 'u1@e.com', 'senha123')
criar_cliente('usuario2', 'Cliente Dois', '55566677788', 'u2@e.com', 'senha123')
END