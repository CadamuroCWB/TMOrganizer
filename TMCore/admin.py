from django.contrib import admin

from .models import tm_currency, tm_unit_measurement, company

@admin.register(tm_currency)
class tm_currencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'SymbolBeforeValue', 'CodeWebServiceBCB_Sale', 'CodeWebServiceBCB_Buy', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)

@admin.register(tm_unit_measurement)
class tm_unit_measurementAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'complement', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)

@admin.register(company)
class companyAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnpj', 'alias', 'phone', 'email', 'current_status', 'created_at', 'updated_at')
    search_fields = ('name', 'cnpj', 'alias')
    list_filter = ('current_status',)
    ordering = ('name',)
