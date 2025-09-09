import uuid

from django.db import models
from django.forms import ValidationError

from stdimage.models import StdImageField  # images

from validate_docbr import CNPJ
from django.core.exceptions import ValidationError

# functions
def validate_cnpj(value):
    if not is_valid_cnpj(value):
        raise ValidationError('CNPJ inválido')

def is_valid_cnpj(cnpj):
    cnpj_validator = CNPJ()
    return cnpj_validator.validate(cnpj)

def clean(self):
    calendar_day = Calendar.objects.filter(date=self.start_datetime.date()).first()
    if calendar_day and not calendar_day.is_working_day:
        raise ValidationError("Não é possível criar eventos em dias não úteis.")

# class
class kindStatus(models.IntegerChoices):
    ACTIVE = 1, 'Ativo'
    INACTIVE = 0, 'Inativo'

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'
    

class Base(models.Model):
    current_status = models.IntegerField('Situação', default=kindStatus.ACTIVE, choices=kindStatus.choices)
    created_at = models.DateTimeField('Data inclusão', auto_now_add=True)
    updated_at = models.DateTimeField('Data alteração', auto_now=True)
    class Meta:
        abstract = True

class Type(Base):
    code = models.CharField('Codigo', max_length=20, unique=True)
    name = models.CharField('Descrição', max_length=50, unique=True)
    complement = models.TextField('Complemento', blank=True, null=True)
    value = models.DecimalField('Valor', max_digits=10, decimal_places=4, null=True)
    class Meta:
        abstract = True

class Country(Type):
    currency = models.ForeignKey('Currency', verbose_name='Moeda', on_delete=models.PROTECT, blank=True, null=True)
    idd_code = models.CharField('DDI', max_length=5, blank=True, null=True)
    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        ordering = ['name']
    def __str__(self):
        return self.name

class State(Type):
    abbreviation = models.CharField('Sigla', max_length=2, unique=True)
    country = models.ForeignKey('Country', verbose_name='País', on_delete=models.PROTECT, blank=True, null=True)
    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = ['name']
    def __str__(self):
        return self.name

class City(Type):
    ddd_code = models.CharField('DDD', max_length=5, blank=True, null=True)
    state = models.ForeignKey('State', verbose_name='Estado', on_delete=models.PROTECT, blank=True, null=True)
    ibge_code = models.CharField('IBGE', max_length=7, blank=True, null=True)
    start_postal_code = models.CharField('CEP Inicial', max_length=10, blank=True, null=True)
    end_postal_code = models.CharField('CEP Final', max_length=10, blank=True, null=True)
    population = models.IntegerField('População', blank=True, null=True)
    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'
        ordering = ['name']
    def __str__(self):
        return self.name
    
class AddressType(Type):
    class Meta:
        verbose_name = 'Tipo de Endereço'
        verbose_name_plural = 'Tipos de Endereço'
        ordering = ['name']

    def __str__(self):
        return self.name

class Address(Base):
    street = models.CharField('Rua', max_length=100)
    number = models.CharField('Número', max_length=10)
    complement = models.CharField('Complemento', max_length=100, blank=True, null=True)
    neighborhood = models.CharField('Bairro', max_length=100)
    city = models.ForeignKey('City', verbose_name='Cidade', on_delete=models.PROTECT)
    zip_code = models.CharField('CEP', max_length=10)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['street', 'number']

    def __str__(self):
        return f'{self.street}, {self.number} - {self.city}/{self.city.state.abbreviation}'

class Currency(Type):
    symbol_before_value = models.CharField('Simbolo', max_length=10, blank=True, null=True)
    code_Web_service_BCB_sale = models.IntegerField('Código BCB - venda', blank=True, null=True)
    code_Web_service_BCB_buy = models.IntegerField('Código BCB - compra', blank=True, null=True)
    class Meta:
        verbose_name = 'Moeda'
        verbose_name_plural = 'Moedas'
        ordering = ['name']
    def __str__(self):
        return self.name
    
class ISIC(Type):

    class Meta:
        verbose_name = 'CNAE'
        verbose_name_plural = 'CNAEs'
        ordering = ['code']

    def __str__(self):
        return self.code

class UnitMeasurement(Type):
    class Meta:
        verbose_name = 'Unidade Medida'
        verbose_name_plural = 'Unidades de Medida'
        ordering = ['name']
    def __str__(self):
        return self.name

class PhoneType(Type):
    class Meta:
        verbose_name = 'Tipo de Telefone'
        verbose_name_plural = 'Tipos de Telefone'
        ordering = ['name']

    def __str__(self):
        return self.name

class Calendar(Base):
    company = models.ForeignKey('Company', verbose_name='Empresa', on_delete=models.PROTECT, blank=True, null=True)
    date = models.DateField('Data', unique=True)
    is_work_day = models.BooleanField('Dia útil', default=True)
    notes = models.TextField('Observações', blank=True, null=True) # Ex: dia de todos os santos

    class Meta:
        verbose_name = 'Calendário'
        verbose_name_plural = 'Calendários'
        ordering = ['date']

    def __str__(self):
        return f'{self.date} - {"Útil" if self.is_working_day else "Não útil"}'

class Event(Base):
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição', blank=True, null=True)
    start_datetime = models.DateTimeField('Início')
    end_datetime = models.DateTimeField('Fim')
    location = models.CharField('Local', max_length=255, blank=True, null=True)

    participants = models.ManyToManyField(
        'Person',
        verbose_name='Participantes',
        blank=True,
        related_name='events'
    )

    company = models.ForeignKey(
        'Company',
        verbose_name='Empresa',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    all_day = models.BooleanField('Dia inteiro', default=False)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['start_datetime']

    def __str__(self):
        return f'{self.title} ({self.start_datetime:%d/%m/%Y %H:%M})'

class Person(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Nome', max_length=100)
    alias = models.CharField('Nome curto', max_length=50, unique=True)
    email = models.EmailField('E-mail', unique=True)
    phone = models.CharField('Telefone', max_length=15, blank=True, null=True)
    phone_type = models.ForeignKey('PhoneType', verbose_name='Tipo de Telefone', on_delete=models.PROTECT, blank=True, null=True)
    address = models.ManyToManyField('Address', verbose_name='Endereço', blank=True)
    address_type = models.ForeignKey('AddressType', verbose_name='Tipo de Endereço', on_delete=models.PROTECT, blank=True, null=True)
    home_directory = models.CharField('Diretório base', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ['name']

    def __str__(self):
        return self.name

class Company(Person):
    cnpj = models.CharField('CNPJ', max_length=14, unique=True, validators=[validate_cnpj])
    start_date = models.DateField('Data de abertura', blank=True, null=True)
    tax_regime = models.CharField('Regime tributário', max_length=50, blank=True, null=True)
    legal_nature = models.CharField('Natureza jurídica', max_length=100, blank=True, null=True)
    end_consumer = models.BooleanField('Consumidor final', default=False)
    subject_protest = models.BooleanField('Sujeito a protesto', default=False)
    logo = StdImageField('Logo', upload_to='company_logos/', blank=True, null=True, variations={'thumbnail': {'width': 200, 'height': 200}})
    isic = models.ManyToManyField('ISIC', verbose_name='CNAE', blank=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['name']

    def __str__(self):
        return self.name

class NaturalPerson(Person):
    cpf = models.CharField('CPF', max_length=11, unique=True)
    birth_date = models.DateField('Data de nascimento', blank=True, null=True)
    photo = StdImageField('Foto', upload_to='natural_person_photos/', blank=True, null=True, variations={'thumbnail': {'width': 200, 'height': 200}})
    father_name = models.CharField('Nome do pai', max_length=100, blank=True, null=True)
    mother_name = models.CharField('Nome da mãe', max_length=100, blank=True, null=True)
    sex = models.CharField('Sexo', max_length=10, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('I', 'Indefinido')], blank=True, null=True)
    nationality = models.CharField('Nacionalidade', max_length=100, blank=True, null=True)
    marital_status = models.CharField('Estado civil', max_length=50, blank=True, null=True)
    profession = models.CharField('Profissão', max_length=100, blank=True, null=True)
    rg = models.CharField('RG', max_length=12, unique=True, blank=True, null=True)
    issuing_agency = models.CharField('Órgão emissor', max_length=100, blank=True, null=True)
    voter_registration = models.CharField('Título de eleitor', max_length=12, unique=True, blank=True, null=True)
    reservist_certificate = models.CharField('Certificado de reservista', max_length=12, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Pessoa Física'
        verbose_name_plural = 'Pessoas Físicas'
        unique_together = ['cpf', 'rg', 'voter_registration', 'reservist_certificate']
        indexes = [
            models.Index(fields=['cpf']),
            models.Index(fields=['rg']),
            models.Index(fields=['voter_registration']),
            models.Index(fields=['reservist_certificate']),
        ]

    def __str__(self):
        return self.name
