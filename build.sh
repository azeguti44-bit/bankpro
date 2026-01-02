#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
sup, created = User.objects.get_or_create(
    username='supervisor', 
    defaults={'nome_completo': 'Admin', 'cpf': '00000000000', 'is_staff': True, 'is_superuser': True}
)
if created:
    sup.set_password('admin_senha123')
    sup.save()
END