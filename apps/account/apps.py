import sys
from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.account"
    verbose_name = "Contas"

    def ready(self):
        if "runserver" in sys.argv:
            from apps.account.models import User
            if not User.objects.filter(email="admin@admin.com").exists():
                User.objects.create_superuser(email="admin@admin.com", password="admin123")
