from django.db import models

class _item_unit_measurement(models.Model):
    name = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=10)
    current_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Unidade Medida'
        verbose_name_plural = 'Unidades de Medida'
        ordering = ['name']
    def __str__(self):
        return self.name

class Item(models.Model):
    item_code = models.CharField('Codigo', max_length=20)
    name = models.CharField(max_length=60)
    ncm = models.CharField(max_length=10, blank=True, null=True)
    ncm_excess = models.BooleanField(default=False)
    cest = models.CharField(max_length=10, blank=True, null=True)
    unit_measurement = models.ForeignKey(_item_unit_measurement, on_delete=models.CASCADE, blank=True, null=True)
    net_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    number_expiration_days = models.IntegerField(default=0)
    use_decimal_quantity = models.BooleanField(default=False)
    use_stock_control = models.BooleanField(default=False)
    use_serial_number = models.BooleanField(default=False)
    use_batch_expiration = models.BooleanField(default=False)
    use_controlled_product = models.BooleanField(default=False)
    description = models.TextField()
    tags = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    box_height = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    box_width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    box_length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    box_weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    box_quantity = models.IntegerField(default=0)
    current_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['name']
    def __str__(self):
        return self.name