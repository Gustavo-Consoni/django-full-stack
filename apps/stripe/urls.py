from django.urls import path
from apps.stripe import views


urlpatterns = [
    path('stripe-checkout', views.StripeCheckout.as_view(), name='stripe_checkout'),
    path('stripe-webhook', views.StripeWebhook.as_view(), name='stripe_webhook'),
]
