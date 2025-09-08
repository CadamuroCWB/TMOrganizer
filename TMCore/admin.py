from django.contrib import admin

from .models import Currency, UnitMeasurement, Company, Person, Calendar, Event

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

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'alias', 'email', 'phone', 'current_status', 'created_at', 'updated_at')
    search_fields = ('name', 'alias', 'email')
    list_filter = ('current_status',)
    ordering = ('name',)

