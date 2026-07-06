from django.contrib import admin
from .models import Token, Booking, Notification, Reward

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('token_number', 'user', 'queue', 'status', 'created_at')
    list_filter = ('status', 'queue', 'created_at')
    search_fields = ('user__username', 'queue__service_name', 'token_number')
    readonly_fields = ('unique_id', 'created_at', 'updated_at', 'qr_code')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'queue', 'token', 'created_at')
    list_filter = ('queue', 'created_at')
    search_fields = ('user__username', 'queue__service_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('token', 'notification_type', 'is_sent', 'created_at')
    list_filter = ('notification_type', 'is_sent', 'created_at')
    search_fields = ('token__token_number', 'message')
    readonly_fields = ('created_at',)


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('user', 'points_earned', 'reason', 'created_at')
    list_filter = ('reason', 'created_at')
    search_fields = ('user__username', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('User Info', {'fields': ('user', 'token')}),
        ('Reward Details', {'fields': ('points_earned', 'reason', 'description')}),
        ('Timestamps', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
