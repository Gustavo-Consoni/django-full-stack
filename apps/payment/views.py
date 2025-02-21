import stripe
from datetime import datetime
from django.views import View
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect, get_object_or_404
from apps.account.models import User
from apps.payment.models import Plan, Subscription


class CreateCheckoutSession(View):

    def get(self, request, name):
        plan = get_object_or_404(Plan, name=name)

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": plan.stripe_price_id,
                    "quantity": 1,
                },
            ],
            phone_number_collection={
                "enabled": True,
            },
            metadata={
                "plan_id": plan.id,
            },
            mode="subscription",
            payment_method_types=["card"],
            billing_address_collection="required",
            success_url=request.build_absolute_uri(reverse("subscription_success")),
            cancel_url=request.build_absolute_uri(reverse("home")),
        )

        return redirect(checkout_session.url)


class SubscriptionSuccess(View):

    def get(self, request):
        return render(request, "pages/payment/subscription_success.html")


class ManageSubscription(View):

    def get(self, request):
        subscription = get_object_or_404(Subscription, user=request.user)

        portal_session = stripe.billing_portal.Session.create(
            customer=subscription.stripe_customer_id,
            return_url=request.build_absolute_uri(reverse("workouts_template")),
        )

        return redirect(portal_session.url)


class StripeWebhook(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_KEY)
            session = event["data"]["object"]
        except ValueError:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            user, created = User.objects.get_or_create(email=session["customer_details"]["email"])
            if created:
                first_name, *last_name = [word.capitalize() if word not in ["de", "da", "do", "das", "dos"] else word for word in session["customer_details"]["name"].lower().split()]
                user.first_name = first_name
                user.last_name = " ".join(last_name)
                user.phone_number = session["customer_details"]["phone"]
                user.save()

            try:
                plan = Plan.objects.get(id=session["metadata"]["plan_id"])
                stripe_subscription = stripe.Subscription.retrieve(session["subscription"])
                status = stripe_subscription["status"]
                start_date = datetime.fromtimestamp(stripe_subscription["current_period_start"])
                end_date = datetime.fromtimestamp(stripe_subscription["current_period_end"])

                Subscription.objects.update_or_create(
                    user=user,
                    defaults={
                        "plan": plan,
                        "stripe_subscription_id": session["subscription"],
                        "stripe_customer_id": session["customer"],
                        "status": status,
                        "start_date": start_date,
                        "end_date": end_date,
                    }
                )
            except Plan.DoesNotExist:
                print(f"Plano com ID {session['metadata']['plan_id']} não encontrado.")

            form = PasswordResetForm({"email": user.email})
            if form.is_valid():
                form.save(
                    email_template_name="pages/account/password_reset_email.html",
                    request=request,
                )

        elif event["type"] == "customer.subscription.updated":
            try:
                subscription = Subscription.objects.get(stripe_subscription_id=session["id"])
                subscription.status = session["status"]
                subscription.plan = Plan.objects.get(stripe_price_id=session["plan"]["id"])
                subscription.save()
            except Subscription.DoesNotExist:
                print(f"Assinatura com ID {session['id']} não encontrada.")
            except Plan.DoesNotExist:
                print(f"Plano com ID {session['plan']['id']} não encontrado.")

        elif event["type"] == "customer.subscription.deleted":
            try:
                subscription = Subscription.objects.get(stripe_subscription_id=session["id"])
                subscription.status = "canceled"
                subscription.save()
            except Subscription.DoesNotExist:
                print(f"Assinatura com ID {session['id']} não encontrada.")

        return HttpResponse(status=200)
