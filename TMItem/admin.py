from django.contrib import admin

from .models import RiskNumber, RiskClassification, Category, CST, ONU, Origin, Item

@admin.register(RiskNumber)
class RiskNumberAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'value', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)
@admin.register(RiskClassification)
class RiskClassificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'value', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'value', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)
@admin.register(CST)
class CSTAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'value', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)
@admin.register(ONU)
class ONUAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'value', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)
@admin.register(Origin)
class OriginAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'value', 'current_status', 'created_at', 'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('current_status',)
    ordering = ('name',)
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'risk_number', 'risk_classification', 'cst', 'onu', 'origin', 'current_status', 'created_at', 'updated_at')
    search_fields = ('item_code', 'name')
    list_filter = ('category', 'risk_number', 'risk_classification', 'cst', 'onu', 'origin', 'current_status')
    ordering = ('name',)
