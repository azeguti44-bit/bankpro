#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instalar as dependências
# Tentamos primeiro o pip (padrão)
pip install --upgrade pip
pip install -r requirements.txt

# 2. Comandos do Django
python manage.py collectstatic --no-input
python manage.py migrate

# 3. Script de criação de usuários
python manage.py shell << END
from django.contrib.auth import get_user_model
from django.apps import apps
import random

User = get_user_model()
Account = apps.get_model('banco', 'Account')

def criar_cliente(username, nome, cpf, email, senha):
    if not User.objects.filter(username=username).exists() and not User.objects.filter(cpf=cpf).exists():
        u = User.objects.create_user(
            username=username, 
            nome_completo=nome, 
            cpf=cpf, 
            email=email, 
            password=senha
        )
        Account.objects.create(user=u, number=str(random.randint(100000, 999999)), account_type='corrente', balance=5000)
        Account.objects.create(user=u, number=str(random.randint(1000000, 9999999)), account_type='poupanca', balance=5000)
        print(f"Usuario {username} criado.")
    else:
        print(f"Usuario {username} ou CPF {cpf} ja existem.")

if not User.objects.filter(username='supervisor').exists():
    User.objects.create_superuser(username='supervisor', nome_completo='Admin', cpf='00000000000', email='a@a.com', password='admin_senha123')

criar_cliente('peter', 'Cliente Um', '29730565864', 'peter@gmail.com', 'senha123')
criar_cliente('hook', 'Cliente Dois', '55566677788', 'hook@gmail.com', 'senha123')
END