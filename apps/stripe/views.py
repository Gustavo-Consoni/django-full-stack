import stripe
from django.views import View
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class StripeCheckout(View):

    def post(self, request):
        line_items = []

        products = sorted(request.data['products'], key=lambda x: x['id'])
        products_id = [product['id'] for product in products]
        products_volume = [product['volume'] for product in products]

        # Aqui eu preciso conferir se os produtos existem
        # products = Product.objects.filter(id__in=products_id)
        for index, product in enumerate(products):
            line_items.append(
                {
                    'price_data': {
                        'currency': 'BRL',
                        'unit_amount': int(product.price),
                        'product_data': {
                            'name': product.name,
                            'images': [request.build_absolute_uri(product.image.url)],
                        }
                    },
                    'quantity': products_volume[index],
                },
            )

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            payment_method_types=[
                'card',
                'boleto',
            ],
            metadata={
                'products_id': products_id,
            },
            mode='payment',
            success_url=request.build_absolute_uri(reverse('home')),
            cancel_url=request.build_absolute_uri(reverse('home')),
        )

        return JsonResponse({'id': checkout_session.id})


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhook(View):

    def post(self, request):
        event = None
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.STRIPE_WEBHOOK_KEY
        print(payload)

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                endpoint_secret,
            )
        except ValueError as e:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse(status=400)
        return HttpResponse(status=200)
