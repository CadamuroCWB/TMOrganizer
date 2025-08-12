from django import forms

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
