from django.db import models
from apps.account.models import User


class Plan(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    stripe_product_id = models.CharField(max_length=40, verbose_name="Stripe Product ID")
    stripe_price_id = models.CharField(max_length=40, verbose_name="Stripe Price ID")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "plano"
        verbose_name_plural = "planos"


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Usuário")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="subscriptions", verbose_name="Plano")
    stripe_subscription_id = models.CharField(max_length=40, verbose_name="Stripe Subscription ID")
    stripe_customer_id = models.CharField(max_length=40, verbose_name="Stripe Customer ID")
    status = models.CharField(max_length=20, verbose_name="Status")
    start_date = models.DateTimeField(verbose_name="Data de início")
    end_date = models.DateTimeField(verbose_name="Data de término")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")

    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name = "assinatura"
        verbose_name_plural = "assinaturas"
