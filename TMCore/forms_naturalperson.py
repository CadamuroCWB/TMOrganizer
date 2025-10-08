from django import forms
from TMCore.models import NaturalPerson

class NaturalPersonForm(forms.ModelForm):
    class Meta:
        model = NaturalPerson
        fields = [
            'cpf', 'birth_date', 'photo', 'father_name', 'mother_name', 'sex',
            'nationality', 'marital_status', 'profession', 'rg', 'issuing_agency',
            'voter_registration', 'reservist_certificate', 'user', 'owner_company'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'sex': forms.Select(),
            'photo': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'owner_company': forms.Select(),
            'user': forms.Select(),
        }
