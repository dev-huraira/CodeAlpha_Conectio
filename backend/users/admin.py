from django.contrib import admin
from .models import Profile, Connection


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'headline', 'location', 'created_at']
    search_fields = ['user__username', 'user__email', 'headline']


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    search_fields = ['follower__username', 'following__username']
