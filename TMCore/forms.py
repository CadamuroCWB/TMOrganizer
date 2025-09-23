from django import forms
from django.core.mail import EmailMessage
from datetime import date, timedelta

from TMCore.models import Company  # Usar classe Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'cnpj', 'alias', 'phone', 'email', 'logo', 'home_directory']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Razão Social'}),
            'cnpj': forms.TextInput(attrs={'placeholder': 'CNPJ'}),
            'alias': forms.TextInput(attrs={'placeholder': 'Nome Fantasia'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Telefone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
            'logo': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'home_directory': forms.TextInput(attrs={'placeholder': 'Diretório Base'}),
        }
        
class ContactUsForm(forms.Form):
    name = forms.CharField(
        max_length=60, label=("Nome"))
    email = forms.EmailField(
        max_length=254, label=("Email"))
    phone = forms.CharField(
        max_length=15, required=False, label=("Telefone"))
    subject = forms.CharField(
        max_length=100, label=("Assunto"))
    message = forms.CharField(
        widget=forms.Textarea, label=("Mensagem"))

    def send_mail(self):
        msg = EmailMessage(
            subject='Email enviado pelo site Techno Mania - Contato',
            body=f'Nome: {self.cleaned_data['name']}\nEmail: {self.cleaned_data['email']}\nTelefone: {self.cleaned_data['phone']}\nAssunto: {self.cleaned_data['subject']}\nMensagem: {self.cleaned_data['message']}',
            from_email='acadamuro@yahoo.com.br',
            to=['cadamuro@cetem.net.br'],
            #headers={'Reply-To': 'acadamuro@yahoo.com.br'}
        )
        msg.send()

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('name'):
            raise forms.ValidationError("O nome é obrigatório.")
        if not cleaned_data.get('email'):
            raise forms.ValidationError("O email é obrigatório.")
        return cleaned_data




def get_current_week_dates():
    today = date.today()
    dow = today.weekday()  # segunda=0, ..., domingo=6
    
    # Ajustar para domingo (sempre voltar até o domingo anterior)
    # Se hoje é domingo (dow=6), volta 6 dias
    sunday = today - timedelta(days=(dow + 1) % 7)

    return [(sunday + timedelta(days=i)) for i in range(7)]

print(get_current_week_dates())
