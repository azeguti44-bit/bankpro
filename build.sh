#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instala as dependências (Essencial para o Django ser reconhecido)
poetry install

# 2. Coleta arquivos estáticos
python manage.py collectstatic --no-input

# 3. Aplica as migrações
python manage.py migrate

# 4. Cria APENAS o Supervisor
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

# Verifica se o supervisor já existe para não criar duplicado
sup, created = User.objects.get_or_create(
    username='supervisor', 
    defaults={
        'nome_completo': 'Admin Supervisor', 
        'cpf': '00000000000', 
        'is_staff': True, 
        'is_superuser': True,
        'email': 'admin@email.com'
    }
)

if created:
    sup.set_password('admin_senha123')
    sup.save()
    print("Supervisor criado com sucesso!")
else:
    print("Supervisor já existe.")
END