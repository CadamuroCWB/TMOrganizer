from django.contrib import admin

from .models import tm_risk_number, tm_risk_classification, tm_category, tm_cst, tm_onu, tm_origin, item

@admin.register(tm_risk_number)
class tm_risk_numberAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'value', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)
@admin.register(tm_risk_classification)
class tm_risk_classificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'value', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)
@admin.register(tm_category)
class tm_categoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'value', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)
@admin.register(tm_cst)
class tm_cstAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'value', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)
@admin.register(tm_onu)
class tm_onuAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'value', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)
@admin.register(tm_origin)
class tm_originAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'value', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)
@admin.register(item)
class itemAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'risk_number', 'risk_classification', 'cst', 'onu', 'origin', 'current_status', 'created_at', 'updated_at')
    search_fields = ('item_code', 'name')
    list_filter = ('category', 'risk_number', 'risk_classification', 'cst', 'onu', 'origin', 'current_status')
    ordering = ('name',)
