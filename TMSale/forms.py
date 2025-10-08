from django import forms
from django.core.exceptions import ValidationError
from datetime import date

from TMSale.models import Contact, Client


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'cpf', 'alias', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'cpf': forms.TextInput(attrs={'placeholder': 'CPF'}),
            'alias': forms.TextInput(attrs={'placeholder': 'Apelido'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Telefone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
        }


class ClientForm(forms.ModelForm):
    """Formulário personalizado para Client com validações avançadas"""
    
    class Meta:
        model = Client
        fields = [
            'name', 'alias', 'cnpj', 'email', 'phone', 'address',
            'start_date', 'tax_regime', 'legal_nature', 'end_consumer',
            'subject_protest', 'logo', 'isic', 'home_directory'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da empresa',
                'required': True
            }),
            'alias': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome fantasia'
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00.000.000/0000-00',
                'pattern': r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}',
                'title': 'Formato: 00.000.000/0000-00'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@empresa.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'address': forms.Select(attrs={
                'class': 'form-control'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tax_regime': forms.Select(attrs={
                'class': 'form-control'
            }),
            'legal_nature': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Sociedade Limitada'
            }),
            'end_consumer': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'subject_protest': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'isic': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': '5'
            }),
            'home_directory': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Diretório principal'
            })
        }
        labels = {
            'name': 'Razão Social',
            'alias': 'Nome Fantasia',
            'cnpj': 'CNPJ',
            'email': 'E-mail',
            'phone': 'Telefone',
            'address': 'Endereço',
            'start_date': 'Data de Abertura',
            'tax_regime': 'Regime Tributário',
            'legal_nature': 'Natureza Jurídica',
            'end_consumer': 'Consumidor Final',
            'subject_protest': 'Sujeito a Protesto',
            'logo': 'Logo da Empresa',
            'isic': 'CNAE',
            'home_directory': 'Diretório Principal'
        }
        help_texts = {
            'cnpj': 'Formato: 00.000.000/0000-00',
            'start_date': 'Data de abertura da empresa',
            'end_consumer': 'Marque se a empresa é consumidor final',
            'subject_protest': 'Marque se a empresa está sujeita a protesto',
            'logo': 'Formatos aceitos: JPG, PNG, GIF (máx. 2MB)',
            'isic': 'Selecione uma ou mais atividades econômicas'
        }
    
    def clean_cnpj(self):
        """Validação personalizada do CNPJ"""
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj:
            # Remove formatação
            cnpj_numbers = ''.join(filter(str.isdigit, cnpj))
            
            # Verifica se tem 14 dígitos
            if len(cnpj_numbers) != 14:
                raise ValidationError('CNPJ deve ter 14 dígitos.')
            
            # Verifica se já existe (exceto para o próprio objeto)
            existing = Client.objects.filter(cnpj=cnpj)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError('Este CNPJ já está cadastrado.')
        
        return cnpj
    
    def clean_start_date(self):
        """Validação da data de abertura"""
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date > date.today():
            raise ValidationError('A data de abertura não pode ser futura.')
        return start_date
    
    def clean_email(self):
        """Validação do email"""
        email = self.cleaned_data.get('email')
        if email:
            # Verifica se já existe (exceto para o próprio objeto)
            existing = Client.objects.filter(email=email)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError('Este e-mail já está cadastrado.')
        
        return email


class ClientSearchForm(forms.Form):
    """Formulário de busca para clientes"""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome, CNPJ, alias ou email...',
            'autocomplete': 'off'
        }),
        label='Buscar'
    )
    
    tax_regime = forms.ChoiceField(
        label='Regime Tributário',
        choices=[('', 'Todos')] + Client.TAX_REGIME_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    end_consumer = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('true', 'Consumidor Final'),
            ('false', 'Não Consumidor Final')
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Tipo de Cliente'
    )