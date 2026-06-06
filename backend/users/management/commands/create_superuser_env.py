"""
Create a superuser from environment variables (for Render free tier).
Usage: python manage.py create_superuser_env
Reads SUPERUSER_USERNAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD from env.
"""

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create superuser from environment variables (SUPERUSER_USERNAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD)'

    def handle(self, *args, **options):
        username = os.environ.get('SUPERUSER_USERNAME', '')
        email = os.environ.get('SUPERUSER_EMAIL', '')
        password = os.environ.get('SUPERUSER_PASSWORD', '')

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                'Skipping superuser creation: SUPERUSER_USERNAME or SUPERUSER_PASSWORD not set.'
            ))
            return

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            if email:
                user.email = email
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" updated with new password.'))
            return

        User.objects.create_superuser(
            username=username,
            email=email or f'{username}@conectio.com',
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
