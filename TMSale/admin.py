from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Client, Contact


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # Campos exibidos na lista
    list_display = [
        'name', 'cnpj', 'email', 'phone', 'end_consumer', 'subject_protest', 'logo_preview'
    ]
    
    # Campos para busca
    search_fields = ['name', 'cnpj', 'alias', 'email']
    
    # Filtros laterais
    list_filter = [
        'end_consumer', 'subject_protest', 'tax_regime', 'legal_nature', 'start_date'
    ]
    
    # Campos editáveis diretamente na lista
    list_editable = ['end_consumer', 'subject_protest']
    
    # Ordenação padrão
    ordering = ['name']
    
    # Paginação
    list_per_page = 25
    
    # Organização dos campos no formulário
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'alias', 'cnpj')
        }),
        ('Contato', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Informações Empresariais', {
            'fields': ('start_date', 'tax_regime', 'legal_nature', 'isic')
        }),
        ('Configurações', {
            'fields': ('end_consumer', 'subject_protest', 'home_directory')
        }),
        ('Logo', {
            'fields': ('logo',),
            'classes': ('collapse',)
        })
    )
    
    # Campos somente leitura
    readonly_fields = ['created_at', 'updated_at']
    
    # Filtro de data
    date_hierarchy = 'start_date'
    
    # Ações personalizadas
    actions = ['mark_as_end_consumer', 'mark_as_not_end_consumer']
    
    def logo_preview(self, obj):
        """Exibe preview da logo na lista"""
        if obj.logo:
            return format_html(
                '<img src="{}" width="30" height="30" style="border-radius: 50%;" />',
                obj.logo.thumbnail.url if hasattr(obj.logo, 'thumbnail') else obj.logo.url
            )
        return "Sem logo"
    logo_preview.short_description = "Logo"
    
    def mark_as_end_consumer(self, request, queryset):
        """Ação para marcar como consumidor final"""
        updated = queryset.update(end_consumer=True)
        self.message_user(request, f'{updated} clientes marcados como consumidor final.')
    mark_as_end_consumer.short_description = "Marcar como consumidor final"
    
    def mark_as_not_end_consumer(self, request, queryset):
        """Ação para desmarcar como consumidor final"""
        updated = queryset.update(end_consumer=False)
        self.message_user(request, f'{updated} clientes desmarcados como consumidor final.')
    mark_as_not_end_consumer.short_description = "Desmarcar como consumidor final"
    
    # Configurações avançadas
    save_on_top = True
    preserve_filters = True


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'cpf', 'email', 'phone', 'alias']
    search_fields = ['name', 'cpf', 'email', 'phone']
    list_filter = ['created_at']
    ordering = ['name']