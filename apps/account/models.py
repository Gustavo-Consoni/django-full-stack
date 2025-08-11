from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        if not password:
            raise ValueError("The password must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email          = models.EmailField(unique=True)
    username       = models.CharField(max_length=50, null=True, blank=True)
    phone_number   = models.CharField(max_length=15, null=True, blank=True, verbose_name="Telefone")
    date_birth     = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    postal_code    = models.CharField(max_length=8, null=True, blank=True, verbose_name="Cep")
    state          = models.CharField(max_length=2, null=True, blank=True, verbose_name="Estado")
    city           = models.CharField(max_length=100, null=True, blank=True, verbose_name="Cidade")
    district       = models.CharField(max_length=100, null=True, blank=True, verbose_name="Bairro")
    street         = models.CharField(max_length=100, null=True, blank=True, verbose_name="Rua")
    address_number = models.CharField(max_length=10, null=True, blank=True, verbose_name="Número")
    complement     = models.CharField(max_length=100, null=True, blank=True, verbose_name="Complemento")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
