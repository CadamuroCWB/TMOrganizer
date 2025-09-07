from django.db import models
from django.db.models import signals # signals
from django.template.defaultfilters import slugify # url

from stdimage.models import StdImageField # images

from TMCore.models import Base, UnitMeasurement # unit of measurement

class Type(Base):
    code = models.CharField('Codigo', max_length=20, unique=True)
    name = models.CharField('Descrição', max_length=50, unique=True)
    complement = models.TextField('Complemento', blank=True, null=True)
    value = models.DecimalField('Valor', max_digits=10, decimal_places=4, null=True)
    class Meta:
        abstract = True

class RiskNumber(Type):
    class Meta:
        verbose_name = 'Numero de Risco'
        verbose_name_plural = 'Numeros de Risco'
        ordering = ['name']
    def __str__(self):
        return self.name

class RiskClassification(Type):
    class Meta:
        verbose_name = 'Classificacao de Risco'
        verbose_name_plural = 'Classificacoes de Risco'
        ordering = ['name']
    def __str__(self):
        return self.name

class Category(Type):
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']
        def __str__(self):
            return self.name

class Origin(Type): # Origem do produto - Tabela A - ORIGEM DO PRODUTO
    class Meta:
        verbose_name = 'Origem'
        verbose_name_plural = 'Origens'
        ordering = ['name'] 
    def __str__(self):
        return self.name

class CST(Type): # Código de Situação Tributária - Tabela B - TRIBUTAÇÃO PELO ICMS
    class Meta:
        verbose_name = 'CST'
        verbose_name_plural = 'CSTs'
        ordering = ['name']
    def __str__(self):
        return self.name

class ONU(Type):
    class Meta:
        verbose_name = 'ONU'
        verbose_name_plural = 'ONUs'
        ordering = ['name']
    def __str__(self):
        return self.name

class Item(Base):
    code = models.CharField('Codigo', max_length=20)
    name = models.CharField('Nome', max_length=60)
#    ncm = models.CharField(max_length=10, blank=True, null=True)
    ncm_excess = models.BooleanField('NCM Exceção', default=False)
#    cest = models.CharField(max_length=10, blank=True, null=True)
    unit_measurement = models.ForeignKey(UnitMeasurement, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    cst = models.ForeignKey(CST, on_delete=models.CASCADE, blank=True, null=True)
    onu = models.ForeignKey(ONU, on_delete=models.CASCADE, blank=True, null=True)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE, blank=True, null=True)
    risk_number = models.ForeignKey(RiskNumber, on_delete=models.CASCADE, blank=True, null=True)
    risk_classification = models.ForeignKey(RiskClassification, on_delete=models.CASCADE, blank=True, null=True)
    net_weight = models.DecimalField('Peso liquido', max_digits=10, decimal_places=2, blank=True, null=True)
    gross_weight = models.DecimalField('Peso bruto', max_digits=10, decimal_places=2, blank=True, null=True)
    number_expiration_days = models.IntegerField('Qtde dias validade', default=0)
    use_decimal_quantity = models.BooleanField('Usa decimal na quantidade', default=False)
    use_stock_control = models.BooleanField('Usa controle de estoque', default=False)
    use_serial_number = models.BooleanField('Usa número de série', default=False)
    use_batch_expiration = models.BooleanField('Usa lote e validade', default=False)
    use_controlled_product = models.BooleanField('Uso controlado', default=False)
    description = models.TextField('Complemento', blank=True, null=True)
    tags = models.CharField(max_length=100, blank=True, null=True)
    image = StdImageField('Imagem', upload_to='items/', variations={'thumb': (124, 124)}, blank=True, null=True)
    slug = models.SlugField(max_length=100, blank=True, null=True, editable=False)
    box_height = models.DecimalField('Altura da caixa', max_digits=10, decimal_places=2, blank=True, null=True)
    box_width = models.DecimalField('Largura da caixa', max_digits=10, decimal_places=2, blank=True, null=True)
    box_length = models.DecimalField('Comprimento da caixa', max_digits=10, decimal_places=2, blank=True, null=True)
    box_weight = models.DecimalField('Peso da caixa', max_digits=10, decimal_places=2, blank=True, null=True)
    box_quantity = models.IntegerField('Quantidade na caixa', default=0)
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'
        ordering = ['name']
    def __str__(self):
        return self.name

def item_pre_save(signal, instance, sender, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.code)
        
signals.pre_save.connect(item_pre_save, sender=Item)
