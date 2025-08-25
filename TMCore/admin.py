from django.contrib import admin

from .models import Currency, UnitMeasurement, Company

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol_before_value', 'codeWeb_service_BCB_sale', 'codeWeb_service_BCB_buy', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)

@admin.register(UnitMeasurement)
class UnitMeasurementAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'complement', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)

@admin.register(Company)
class companyAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'alias', 'phone', 'email', 'current_status', 'created_at', 'updated_at')
    search_fields = ('name', 'cnpj', 'alias')
    list_filter = ('current_status',)
    ordering = ('name',)
