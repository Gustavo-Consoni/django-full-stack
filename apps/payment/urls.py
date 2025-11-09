from django.urls import path
from apps.payment import views, api


urlpatterns = [
    path("assinar", views.SubscriptionCheckout.as_view(), name="subscription_checkout"),
    path("assinatura-finalizada", views.SubscriptionCompleted.as_view(), name="subscription_completed"),
    path("cancelar-assinatura", views.SubscriptionCancel.as_view(), name="subscription_cancel"),

    path("api/asaas-webhook", api.AsaasWebhook.as_view(), name="asaas_webhook"),
]
