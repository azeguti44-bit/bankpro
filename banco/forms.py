from django import forms
from .models import Account, Transaction, Usuario
from django.contrib.auth.forms import UserCreationForm

# Formulário para criar o Usuário
class CadastroUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('nome_completo', 'cpf', 'email')

# ESTA CLASSE DEVE FICAR NA MARGEM ESQUERDA (SEM ESPAÇOS ANTES DO 'class')
class TransferenciaentrecontasForm(forms.Form):
    # Dados da Origem
    conta_origem = forms.ModelChoiceField(
        queryset=None, 
        label="Sair da minha conta",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Dados do Destino
    cpf_destino = forms.CharField(
        max_length=14, 
        label="CPF do Destinatário", 
        widget=forms.TextInput(attrs={
            'class': 'form-control mask-cpf', 
            'placeholder': '000.000.000-00'
        })
    )
    
    numero_conta_destino = forms.CharField(
        max_length=10, 
        label="Número da Conta", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    tipo_conta_destino = forms.ChoiceField(
        choices=Account.TIPOS_CONTA, 
        label="Tipo de Conta", 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # IMPORTANTE: Mudado para TextInput e adicionada a vírgula que faltava
    valor = forms.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        min_value=0.01, 
        widget=forms.TextInput(attrs={
            'class': 'form-control mask-money',
            'placeholder': '0,00'
        })
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['conta_origem'].queryset = Account.objects.filter(user=user)