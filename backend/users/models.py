from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model for Conectio with profile fields built in."""
    bio = models.TextField(blank=True, max_length=300)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    headline = models.CharField(max_length=120, blank=True)
    website = models.URLField(blank=True)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class Connection(models.Model):
    """Follower/following relationship between users."""
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following_set'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers_set'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"
