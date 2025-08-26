from unfold.admin import ModelAdmin
from django.contrib import admin
from apps.payment import models


@admin.register(models.Plan)
class PlanAdmin(ModelAdmin):
    list_per_page = 20
    list_display = ["name", "value", "cycle", "billing_type", "active", "free_period", "refund_period", "created_at"]
    search_fields = ["name"]


@admin.register(models.Coupon)
class CouponAdmin(ModelAdmin):
    list_per_page = 20
    list_display = ["code", "discount", "maximum_uses", "active", "activation_date", "deactivation_date", "created_at"]
    search_fields = ["code"]


@admin.register(models.Customer)
class CustomerAdmin(ModelAdmin):
    list_per_page = 20
    list_display = ["user", "created_at"]
    search_fields = ["user__email", "customer_id"]


@admin.register(models.Subscription)
class SubscriptionAdmin(ModelAdmin):
    list_per_page = 20
    list_display = ["get_user", "plan", "coupon", "status", "next_due", "created_at"]
    search_fields = ["customer__user__email", "customer__customer_id", "subscription_id"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("customer__user", "plan", "coupon")

    def get_user(self, obj):
        return obj.customer.user.email

    get_user.short_description = "Usuário"
    get_user.admin_order_field = "customer__user__email"


@admin.register(models.Payment)
class PaymentAdmin(ModelAdmin):
    list_per_page = 20
    list_display = ["get_user","status", "value", "due_date", "created_at"]
    search_fields = ["subscription__customer__user__email", "subscription__customer__customer_id", "subscription__subscription_id", "payment_id"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("subscription__customer__user")

    def get_user(self, obj):
        return obj.subscription.customer.user.email

    get_user.short_description = "Usuário"
    get_user.admin_order_field = "subscription__customer__user__email"


@admin.register(models.Webhook)
class WebhookAdmin(ModelAdmin):
    list_per_page = 20
    list_display = ["event_id", "created_at"]
    search_fields = ["event_id"]
