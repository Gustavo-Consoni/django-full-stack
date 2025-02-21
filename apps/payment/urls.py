from django.urls import path
from apps.payment import views


urlpatterns = [
    path("create-checkout-session/<str:name>", views.CreateCheckoutSession.as_view(), name="create_checkout_session"),
    path("assinatura-finalizada", views.SubscriptionSuccess.as_view(), name="subscription_success"),
    path("gerenciar-assinatura", views.ManageSubscription.as_view(), name="manage_subscription"),
    path("stripe-webhook", views.StripeWebhook.as_view(), name="stripe_webhook"),
]
