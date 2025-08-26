from django.db import models
from django.forms import ValidationError

from stdimage.models import StdImageField  # images

from validate_docbr import CPF

# functions
def validate_cpf(value):
    if not value:
        return  # Aceita vazio/nulo
    if not is_valid_cpf(value):
        raise ValidationError('CPF inválido')

def is_valid_cpf(cpf):
    cpf_validator = CPF()
    return cpf_validator.validate(cpf)

# class
class Base(models.Model):
    current_status = models.BooleanField('Situação', default=True)
    created_at = models.DateTimeField('Data inclusão', auto_now_add=True)
    updated_at = models.DateTimeField('Data alteração', auto_now=True)
    class Meta:
        abstract = True

class Contact(Base):
    name = models.CharField('Nome', max_length=100, unique=True)
    cpf = models.CharField('CPF', max_length=14, unique=True, validators=[validate_cpf], blank=True, null=True)
    alias = models.CharField('Apelido', max_length=50, unique=True, null=True)
    phone = models.CharField('Telefone', max_length=15, blank=True, null=True)
    email = models.EmailField('e-mail', blank=True, null=True)
    #image = StdImageField('Foto', upload_to='contacts', variations={'thumb': {'width': 480, 'height': 480, 'crop': True}}, blank=True, null=True)
    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
        ordering = ['name']
    def __str__(self):
        return self.name
