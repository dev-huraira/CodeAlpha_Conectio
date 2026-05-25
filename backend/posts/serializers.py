from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Post, Like, Comment
from users.serializers import UserMinimalSerializer


def get_time_ago(created_at):
    """Return a human-readable relative time string."""
    if not created_at:
        return ''
    now = timezone.now()
    diff = now - created_at
    seconds = int(diff.total_seconds())

    if seconds < 60:
        return 'Just now'
    elif seconds < 3600:
        mins = seconds // 60
        return f'{mins}m ago'
    elif seconds < 86400:
        hours = seconds // 3600
        return f'{hours}h ago'
    elif seconds < 604800:
        days = seconds // 86400
        return f'{days}d ago'
    elif seconds < 2592000:
        weeks = seconds // 604800
        return f'{weeks}w ago'
    elif seconds < 31536000:
        months = seconds // 2592000
        return f'{months}mo ago'
    else:
        years = seconds // 31536000
        return f'{years}y ago'


class CommentSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    time_ago = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at', 'time_ago']
        read_only_fields = ['author']

    def get_time_ago(self, obj):
        return get_time_ago(obj.created_at)


class PostSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'content', 'image',
            'likes_count', 'comments_count', 'is_liked',
            'created_at', 'updated_at', 'time_ago',
        ]
        read_only_fields = ['author']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_time_ago(self, obj):
        return get_time_ago(obj.created_at)


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'image']
