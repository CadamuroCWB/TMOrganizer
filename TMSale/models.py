from django.db import models
from django.forms import ValidationError

from stdimage.models import StdImageField  # images

from validate_docbr import CPF, CNPJ

from TMCore.models import Base, Person

# functions
def validate_cpf(value):
    if not value:
        return  # Aceita vazio/nulo
    if not is_valid_cpf(value):
        raise ValidationError('CPF inválido')

def is_valid_cpf(cpf):
    cpf_validator = CPF()
    return cpf_validator.validate(cpf)

def validate_cnpj(value):
    if not value:
        return  # Aceita vazio/nulo
    if not is_valid_cnpj(value):
        raise ValidationError('CNPJ inválido')

def is_valid_cnpj(cnpj):
    cnpj_validator = CNPJ()
    return cnpj_validator.validate(cnpj)

# class
class Client(Person):
    # Escolhas para regime tributário
    TAX_REGIME_CHOICES = [
        ('simples_nacional', 'Simples Nacional'),
        ('lucro_presumido', 'Lucro Presumido'),
        ('lucro_real', 'Lucro Real'),
        ('mei', 'Microempreendedor Individual (MEI)'),
        ('isento', 'Isento'),
    ]
    
    cnpj = models.CharField('CNPJ', max_length=14, unique=True, validators=[validate_cnpj])
    start_date = models.DateField('Data de abertura', blank=True, null=True)
    tax_regime = models.CharField('Regime tributário', max_length=50, choices=TAX_REGIME_CHOICES, blank=True, null=True)
    legal_nature = models.CharField('Natureza jurídica', max_length=100, blank=True, null=True)
    end_consumer = models.BooleanField('Consumidor final', default=False)
    subject_protest = models.BooleanField('Sujeito a protesto', default=False)
    logo = StdImageField('Logo', upload_to='client_logos/', blank=True, null=True, variations={'thumbnail': {'width': 200, 'height': 200}})
    isic = models.ManyToManyField('TMCore.ISIC', verbose_name='CNAE', blank=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['name']

    def __str__(self):
        return self.name

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
