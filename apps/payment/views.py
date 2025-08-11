from django.views import View
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.account.models import User
from apps.payment.forms import SubscriptionCheckoutForm
from apps.payment.models import Customer, Subscription, Payment
from apps.payment.asaas import AsaasCustomer, AsaasSubscription, AsaasPayment


class SubscriptionCheckout(View):

    def get(self, request):
        return render(request, "pages/payment/subscription_checkout.html")

    def post(self, request):
        form = SubscriptionCheckoutForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        else:
            return render(request, "pages/payment/subscription_checkout.html", {"form": form})

        try:
            asaas_customer = AsaasCustomer().create_customer(
                name=data["full_name"],
                cpf_cnpj=data["cpf_cnpj"],
                email=data["email"],
                mobile_phone=data["phone_number"],
                postal_code=data["postal_code"],
                address_number=data["address_number"],
            )
        except Exception as e:
            print(e)
            messages.error(request, "Endereço de cobrança inválido")
            return redirect("subscription_checkout")

        try:
            asaas_subscription = AsaasSubscription().create_subscription(
                customer_id=asaas_customer["id"],
                description=data["plan"].name,
                billingType=data["plan"].billing_type,
                cycle=data["plan"].cycle,
                value=float(data["plan"].value),
                next_due_date=timezone.localdate().isoformat(),
                credit_card={
                    "holderName": data["holder_name"],
                    "number": data["number"],
                    "expiryMonth": data["expiry_date"][0],
                    "expiryYear": data["expiry_date"][1],
                    "ccv": data["ccv"],
                },
                credit_card_holder_info={
                    "name": data["full_name"],
                    "email": data["email"],
                    "mobilePhone": data["phone_number"],
                    "cpfCnpj": data["cpf_cnpj"],
                    "postalCode": data["postal_code"],
                    "addressNumber": data["address_number"],
                },
            )
        except Exception as e:
            print(e)
            AsaasCustomer().delete_customer(customer_id=asaas_customer["id"])
            messages.error(request, "Cartão de crédito inválido")
            return redirect("subscription_checkout")

        first_name, separator, last_name = data["full_name"].partition(" ")
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=data["email"],
            password=data["password"],
            phone_number=data["phone_number"],
            date_birth=data["date_birth"],
            postal_code=asaas_customer["postalCode"],
            state=asaas_customer["state"],
            city=asaas_customer["cityName"],
            district=asaas_customer["province"],
            street=asaas_customer["address"],
            address_number=asaas_customer["addressNumber"],
            complement=asaas_customer["complement"],
        )

        customer = Customer.objects.create(
            user=user,
            customer_id=asaas_customer["id"],
        )

        Subscription.objects.create(
            customer=customer,
            plan=data["plan"],
            subscription_id=asaas_subscription["id"],
            next_due=asaas_subscription["nextDueDate"],
        )

        return redirect("subscription_success")


class SubscriptionSuccess(View):

    def get(self, request):
        return render(request, "pages/payment/subscription_success.html")


class SubscriptionCancel(LoginRequiredMixin, View):

    def post(self, request):
        if subscription := Subscription.objects.filter(customer__user=request.user, status="ACTIVE").first():
            AsaasSubscription().update_subscription(
                subscription_id=subscription.subscription_id,
                status="INACTIVE",
            )

            if payment := Payment.objects.filter(subscription__customer__user=request.user, status="PENDING").first():
                AsaasPayment().delete_payment(
                    payment_id=payment.payment_id,
                )

            messages.success(request, "Assinatura cancelada")
        else:
            messages.error(request, "Nenhuma assinatura ativa encontrada")

        return redirect("home")


class SubscriptionRenew(LoginRequiredMixin, View):

    def post(self, request):
        return redirect("home")
