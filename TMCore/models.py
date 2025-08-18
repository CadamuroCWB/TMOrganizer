from django.db import models

class base(models.Model):
    current_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class tm_unit_measurement(base):
    code = models.CharField('Codigo', max_length=20, unique=True)
    name = models.CharField(max_length=50, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=4)
    class Meta:
        verbose_name = 'Unidade Medida'
        verbose_name_plural = 'Unidades de Medida'
        ordering = ['name']
    def __str__(self):
        return self.name
    
class tm_currency(base):
    code = models.CharField('Codigo', max_length=20, unique=True)
    name = models.CharField(max_length=50, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=4)
    SymbolBeforeValue = models.CharField(max_length=10, blank=True, null=True)
    CodeWebServiceBCB_Sale = models.IntegerField(blank=True, null=True)
    CodeWebServiceBCB_Buy = models.IntegerField(blank=True, null=True)
    class Meta:
        verbose_name = 'Moeda'
        verbose_name_plural = 'Moedas'
        ordering = ['name']
    def __str__(self):
        return self.name

class company(base):
    name = models.CharField(max_length=100, unique=True)
    cnpj = models.CharField(max_length=14, unique=True)
    alias = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    homedirectory = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['name']
    def __str__(self):
        return self.name
