from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()

        phone = "8102780474"
        password = "12345"
        email = "admin@example.com"

        if not User.objects.filter(phone=phone).exists():
            User.objects.create_superuser(
                phone=phone,
                password=password,
                email=email
            )
            print("🔥 Superuser created successfully!")
        else:
            print("✔ Superuser already exists. Skipping...")
