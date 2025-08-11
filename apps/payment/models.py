from django.db import models
from apps.account.models import User


class Plan(models.Model):

    class Cycle(models.TextChoices):
        WEEKLY       = "WEEKLY",       "Semanal"
        BIWEEKLY     = "BIWEEKLY",     "Quinzenal"
        MONTHLY      = "MONTHLY",      "Mensal"
        BIMONTHLY    = "BIMONTHLY",    "Bimestral"
        QUARTERLY    = "QUARTERLY",    "Trimestral"
        SEMIANNUALLY = "SEMIANNUALLY", "Semestral"
        YEARLY       = "YEARLY",       "Anual"

    class BillingType(models.TextChoices):
        UNDEFINED   = "UNDEFINED",   "Indefinido"
        BOLETO      = "BOLETO",      "Boleto"
        CREDIT_CARD = "CREDIT_CARD", "Cartão de Crédito"
        PIX         = "PIX",         "Pix"

    name          = models.CharField(max_length=50, verbose_name="Nome")
    value         = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Valor")
    cycle         = models.CharField(max_length=15, choices=Cycle.choices, default=Cycle.MONTHLY, verbose_name="Ciclo")
    billing_type  = models.CharField(max_length=15, choices=BillingType.choices, default=BillingType.CREDIT_CARD, verbose_name="Tipo de Cobrança")
    active        = models.BooleanField(default=False, verbose_name="Ativo")
    free_period   = models.PositiveSmallIntegerField(default=0, verbose_name="Período Gratuito")
    refund_period = models.PositiveSmallIntegerField(default=7, verbose_name="Período de Reembolso")
    created_at    = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "plano"
        verbose_name_plural = "planos"


class Coupon(models.Model):

    class DiscountType(models.TextChoices):
        PERCENTAGE = "PERCENTAGE", "Porcentagem"
        FIXED      = "FIXED",      "Fixo"

    code              = models.CharField(max_length=20, unique=True, verbose_name="Código do Cupom")
    discount          = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Desconto")
    discount_type     = models.CharField(max_length=15, choices=DiscountType.choices, verbose_name="Tipo de desconto")
    maximum_uses      = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Máximo de Usos")
    active            = models.BooleanField(default=False, verbose_name="Ativo")
    activation_date   = models.DateField(null=True, blank=True, verbose_name="Data de ativação")
    deactivation_date = models.DateField(null=True, blank=True, verbose_name="Data de desativação")
    created_at        = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "cupom"
        verbose_name_plural = "cupons"


class Customer(models.Model):
    customer_id       = models.CharField(max_length=30, unique=True, verbose_name="Código do Cliente")
    user              = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer", verbose_name="Usuário")
    created_at        = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    def __str__(self):
        return self.customer_id

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"


class Subscription(models.Model):

    class SubscriptionStatus(models.TextChoices):
        ACTIVE   = "ACTIVE",   "Ativa"
        INACTIVE = "INACTIVE", "Inativa"
        EXPIRED  = "EXPIRED",  "Expirada"

    subscription_id = models.CharField(max_length=30, unique=True, verbose_name="Código da Assinatura")
    customer        = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Código do Cliente")
    plan            = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="subscriptions", verbose_name="Plano")
    coupon          = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL, related_name="subscriptions", verbose_name="Cupom")
    status          = models.CharField(max_length=15, choices=SubscriptionStatus.choices, default=SubscriptionStatus.INACTIVE, verbose_name="Status da Assinatura")
    next_due        = models.DateField(verbose_name="Próximo Vencimento")
    created_at      = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    def __str__(self):
        return self.subscription_id

    class Meta:
        verbose_name = "assinatura"
        verbose_name_plural = "assinaturas"


class Payment(models.Model):

    class PaymentStatus(models.TextChoices):
        CONFIRMED = "CONFIRMED", "Confirmado"
        PENDING   = "PENDING",   "Pendente"
        OVERDUE   = "OVERDUE",   "Vencido"
        REFUNDED  = "REFUNDED",  "Reembolsado"

    payment_id   = models.CharField(max_length=30, unique=True, verbose_name="Código da Cobrança")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="payments", verbose_name="Código da Assinatura")
    status       = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.PENDING, verbose_name="Status da Cobrança")
    value        = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Valor")
    due_date     = models.DateField(verbose_name="Data de Vencimento")
    created_at   = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    def __str__(self):
        return self.payment_id

    class Meta:
        verbose_name = "cobrança"
        verbose_name_plural = "cobranças"


class Webhook(models.Model):
    event_id   = models.CharField(max_length=50, unique=True, verbose_name="Código do Evento")
    payload    = models.JSONField(verbose_name="Payload do Evento")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")

    def __str__(self):
        return self.event_id

    class Meta:
        verbose_name = "webhook"
        verbose_name_plural = "webhooks"
