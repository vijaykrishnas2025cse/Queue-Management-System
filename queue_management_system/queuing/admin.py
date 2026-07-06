from django.contrib import admin
from .models import QueueService

@admin.register(QueueService)
class QueueServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'service_type', 'admin', 'is_active', 'created_at')
    list_filter = ('service_type', 'is_active', 'created_at')
    search_fields = ('service_name', 'admin__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Service Information', {
            'fields': ('admin', 'service_name', 'service_type', 'description')
        }),
        ('Settings', {
            'fields': ('is_active', 'estimated_service_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
