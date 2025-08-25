import requests
from urllib.parse import urlencode, urljoin
from django.conf import settings


class AsaasBase:

    def __init__(self):
        self.API_KEY = settings.ASAAS_API_KEY
        self.BASE_URL = settings.ASAAS_BASE_URL

    def send_request(self, path, method="GET", query_params={}, body={}):
        url = self.mount_url(path, query_params)
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "access_token": self.API_KEY,
        }

        match method.upper():
            case "GET":
                response = requests.get(url=url, headers=headers)
            case "POST":
                response = requests.post(url=url, headers=headers, json=body)
            case "PUT":
                response = requests.put(url=url, headers=headers, json=body)
            case "DELETE":
                response = requests.delete(url=url, headers=headers)

        response.raise_for_status()
        return response.json()

    def mount_url(self, path, query_params={}):
        parameters = urlencode(query_params)

        url = urljoin(self.BASE_URL, path)
        if parameters:
            url += "?" + parameters

        return url


class AsaasCustomer(AsaasBase):

    def get_customer(self, customer_id):
        """ https://docs.asaas.com/reference/recuperar-um-unico-cliente """
        return self.send_request(
            path=f"customers/{customer_id}",
            method="GET",
        )

    def create_customer(self, name, cpf_cnpj, email=None, mobile_phone=None, postal_code=None, address_number=None):
        """ https://docs.asaas.com/reference/criar-novo-cliente """
        return self.send_request(
            path="customers",
            method="POST",
            body={
                "name": name,
                "cpfCnpj": cpf_cnpj,
                "email": email,
                "mobilePhone": mobile_phone,
                "postalCode": postal_code,
                "addressNumber": address_number,
            },
        )

    def update_customer(self, customer_id, name, cpf_cnpj, email=None, mobile_phone=None, postal_code=None, address_number=None):
        """ https://docs.asaas.com/reference/atualizar-cliente-existente """
        body = {
            "name": name,
            "cpfCnpj": cpf_cnpj,
            "email": email,
            "mobilePhone": mobile_phone,
            "postalCode": postal_code,
            "addressNumber": address_number,
        }
        body = {key: value for key, value in body.items() if value not in [None, "", [], {}]}

        return self.send_request(
            path=f"customers/{customer_id}",
            method="PUT",
            body=body,
        )

    def delete_customer(self, customer_id):
        """ https://docs.asaas.com/reference/remover-cliente """
        return self.send_request(
            path=f"customers/{customer_id}",
            method="DELETE",
        )


class AsaasSubscription(AsaasBase):

    def get_subscription(self, subscription_id):
        """ https://docs.asaas.com/reference/recuperar-uma-unica-assinatura """
        return self.send_request(
            path=f"subscriptions/{subscription_id}",
            method="GET",
        )

    def create_subscription(self, customer_id, billingType, cycle, value, next_due_date, description, credit_card, credit_card_holder_info):
        """ https://docs.asaas.com/reference/criar-assinatura-com-cartao-de-credito """
        return self.send_request(
            path="subscriptions",
            method="POST",
            body={
                "customer": customer_id,
                "billingType": billingType,
                "cycle": cycle,
                "value": value,
                "nextDueDate": next_due_date,
                "description": description,
                "creditCard": credit_card,
                "creditCardHolderInfo": credit_card_holder_info,
            },
        )

    def update_subscription(self, subscription_id, status=None, value=None, nextDueDate=None, cycle=None, description=None):
        """ https://docs.asaas.com/reference/atualizar-assinatura-existente """
        body = {
            "status": status,
            "cycle": cycle,
            "value": value,
            "nextDueDate": nextDueDate,
            "description": description,
        }
        body = {key: value for key, value in body.items() if value not in [None, "", [], {}]}

        return self.send_request(
            path=f"subscriptions/{subscription_id}",
            method="PUT",
            body=body,
        )

    def delete_subscription(self, subscription_id):
        """ https://docs.asaas.com/reference/remover-assinatura """
        return self.send_request(
            path=f"subscriptions/{subscription_id}",
            method="DELETE",
        )


class AsaasPayment(AsaasBase):

    def get_payments(self):
        """ https://docs.asaas.com/reference/listar-cobrancas """
        return self.send_request(
            path=f"payments",
            method="GET",
        )

    def delete_payment(self, payment_id):
        """ https://docs.asaas.com/reference/excluir-cobranca """
        return self.send_request(
            path=f"payments/{payment_id}",
            method="DELETE",
        )
