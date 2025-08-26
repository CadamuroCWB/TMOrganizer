from django import forms

from TMSale.models import Contact

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