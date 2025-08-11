import json
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from apps.payment.models import Subscription, Payment, Webhook


@method_decorator(csrf_exempt, name="dispatch")
class AsaasWebhook(APIView):

    def post(self, request):
        if request.headers.get("asaas-access-token") != settings.ASAAS_ACCESS_TOKEN:
            return Response(status=status.HTTP_200_OK)

        try:
            payload = json.loads(request.body.decode())
            event = payload.get("event")

            with transaction.atomic():
                webhook, created = Webhook.objects.get_or_create(
                    event_id=payload.get("id"),
                    defaults={
                        "payload": payload,
                    },
                )
                if not created:
                    return Response(status=status.HTTP_200_OK)

                event = payload.get("event")

                if event in ["SUBSCRIPTION_CREATED", "SUBSCRIPTION_UPDATED", "SUBSCRIPTION_INACTIVATED"]:
                    data = payload.get("subscription")
                    Subscription.objects.update_or_create(
                        subscription_id=data.get("id"),
                        defaults={
                            "status": data.get("status"),
                            "next_due": datetime.strptime(data.get("nextDueDate"), "%d/%m/%Y").date(),
                        },
                    )

                elif event == "SUBSCRIPTION_DELETED":
                    data = payload.get("subscription")
                    if subscription := Subscription.objects.filter(subscription_id=data.get("id")).first():
                        subscription.delete()

                elif event in ["PAYMENT_CREATED", "PAYMENT_UPDATED", "PAYMENT_CONFIRMED", "PAYMENT_OVERDUE", "PAYMENT_REFUNDED"]:
                    data = payload.get("payment")
                    Payment.objects.update_or_create(
                        payment_id=data.get("id"),
                        defaults={
                            "subscription": Subscription.objects.get(subscription_id=data.get("subscription")),
                            "status": data.get("status"),
                            "value": data.get("value"),
                            "due_date": data.get("dueDate"),
                        },
                    )

                elif event == "PAYMENT_DELETED":
                    data = payload.get("payment")
                    if payment := Payment.objects.filter(payment_id=data.get("id")).first():
                        payment.delete()
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)
