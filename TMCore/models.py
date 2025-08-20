from django.db import models

class base(models.Model):
    current_status = models.BooleanField('Situação', default=True)
    created_at = models.DateTimeField('Data inclusão', auto_now_add=True)
    updated_at = models.DateTimeField('Data alteração', auto_now=True)
    class Meta:
        abstract = True

class tm_type(base):
    code = models.CharField('Codigo', max_length=20, unique=True)
    name = models.CharField('Descrição', max_length=50, unique=True)
    complement = models.TextField('Complemento', blank=True, null=True)
    value = models.DecimalField('Valor', max_digits=10, decimal_places=4, null=True)
    class Meta:
        abstract = True

class tm_unit_measurement(tm_type):
    class Meta:
        verbose_name = 'Unidade Medida'
        verbose_name_plural = 'Unidades de Medida'
        ordering = ['name']
    def __str__(self):
        return self.name
    
class tm_currency(tm_type):
    symbol_before_value = models.CharField('Simbolo', max_length=10, blank=True, null=True)
    codeWeb_service_BCB_sale = models.IntegerField('Código BCB - venda', blank=True, null=True)
    codeWeb_service_BCB_buy = models.IntegerField('Código BCB - compra', blank=True, null=True)
    class Meta:
        verbose_name = 'Moeda'
        verbose_name_plural = 'Moedas'
        ordering = ['name']
    def __str__(self):
        return self.name

class company(base):
    name = models.CharField('Razão social', max_length=100, unique=True)
    cnpj = models.CharField('CNPJ', max_length=14, unique=True)
    alias = models.CharField('Fantasia', max_length=50, unique=True)
    phone = models.CharField('Telefone', max_length=15, blank=True, null=True)
    email = models.EmailField('e-mail', blank=True, null=True)
    logo = models.ImageField('Logo', upload_to='company_logos/', blank=True, null=True)
    homedirectory = models.CharField('Diretório base', max_length=255, blank=True, null=True)
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['name']
    def __str__(self):
        return self.name
