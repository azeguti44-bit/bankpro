from django.urls import path
from . import views

urlpatterns = [
    path('accounts/', views.account_list, name='account_list'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('extrato/<int:account_id>/', views.transaction_list, name='transaction_list'),
    path('transferir/', views.transferir, name='transferir'),
    path('usuario/excluir/<int:user_id>/', views.excluir_usuario, name='excluir_usuario'),
    
    
]