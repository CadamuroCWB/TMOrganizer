from django.contrib import admin

from .models import Currency, UnitMeasurement, Company, Person, Calendar, Event

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

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'alias', 'email', 'phone', 'current_status', 'created_at', 'updated_at')
    search_fields = ('name', 'alias', 'email')
    list_filter = ('current_status',)
    ordering = ('name',)

@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ('date', 'is_working_day', 'company')
    search_fields = ('date',)
    list_filter = ('is_working_day', 'company')
    ordering = ('date',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_datetime', 'end_datetime', 'company')
    list_filter = ('company', 'start_datetime')
    search_fields = ('title', 'description')

