from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Connection


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for the custom User model."""
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'headline', 'is_staff', 'date_joined',
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'headline']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']

    # Add custom fields to the admin form
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Conectio Profile', {
            'fields': ('bio', 'avatar', 'headline', 'website',
                       'followers_count', 'following_count', 'posts_count'),
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Conectio Profile', {
            'fields': ('email', 'first_name', 'last_name', 'headline'),
        }),
    )


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    search_fields = ['follower__username', 'following__username']
