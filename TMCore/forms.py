from django import forms
from django.core.mail.message import EmailMessage

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

    def send_email(self):
        email = EmailMessage(
            subject='Este e-mail foi enviado pelo site',
            body=f'Nome: {self.cleaned_data['name']}\nEmail: {self.cleaned_data['email']}\nTelefone: {self.cleaned_data['phone']}\nAssunto: {self.cleaned_data['subject']}\nMensagem: {self.cleaned_data['message']}',
            from_email='acadamuro@yahoo.com.br',
            to=['cadamuro@cetem.net.br'],
            headers={'Reply-To': self.cleaned_data['email']}
        )
        email.send()

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('name'):
            raise forms.ValidationError("O nome é obrigatório.")
        if not cleaned_data.get('email'):
            raise forms.ValidationError("O email é obrigatório.")
        return cleaned_data