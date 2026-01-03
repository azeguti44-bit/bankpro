from django import forms
from .models import Account, Transaction, Usuario
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import Transaction, Account



# NOVO: Formulário para criar o Usuário
class CadastroUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        # Aqui você escolhe quais campos aparecerão no formulário de cadastro
        fields = UserCreationForm.Meta.fields + ('nome_completo', 'cpf', 'email')




class TransferenciaentrecontasForm(forms.Form):
    # Dados da Origem (Sempre do usuário logado)
    conta_origem = forms.ModelChoiceField(
        queryset=None, 
        label="Sair da minha conta",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Dados do Destino (Para buscar outro usuário)
    cpf_destino = forms.CharField(
        max_length=14, 
        label="CPF do Destinatário", 
        widget=forms.TextInput(attrs={
            'class': 'form-control mask-cpf', 
            'placeholder': '000.000.000-00'
            }
        ))
    numero_conta_destino = forms.CharField(
        max_length=10, 
        label="Número da Conta", 
        widget=forms.TextInput(attrs={
        'class': 'form-control' # Apenas o visual do Bootstrap, sem máscara JS
    })
)
    
    valor = forms.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        min_value=0.01, 
        widget=forms.NumberInput(attrs={
            'class': 'form-control mask-money'
            'placeholder': '0,00'
        })
)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filtra apenas as contas do Peter Pan (quem está logado)
            self.fields['conta_origem'].queryset = Account.objects.filter(user=user)
