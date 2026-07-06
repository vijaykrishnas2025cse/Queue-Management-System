from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'reward_points', 'completed_bookings', 'is_admin_user', 'created_at')
    list_filter = ('is_admin_user', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at', 'get_priority_score')
    fieldsets = (
        ('User Info', {'fields': ('user', 'phone_number', 'is_admin_user')}),
        ('Reward Info', {'fields': ('reward_points', 'completed_bookings', 'get_priority_score')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
