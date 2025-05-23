from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from apps.account.models import User


@receiver(post_migrate)
def verify_dev_superuser(sender, **kwargs):
    if not settings.DEBUG:
        return

    if not User.objects.filter(email="admin@admin.com").exists():
        User.objects.create_superuser(
            email="admin@admin.com",
            password="admin123",
        )
