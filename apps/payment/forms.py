import re
from django import forms
from apps.account.models import User
from apps.payment.models import Plan


class SubscriptionCheckoutForm(forms.Form):
    plan           = forms.CharField(max_length=50)
    full_name      = forms.CharField(max_length=100)
    email          = forms.EmailField(max_length=100)
    phone_number   = forms.CharField(max_length=15)
    date_birth     = forms.DateField(input_formats=["%d/%m/%Y"])
    password       = forms.CharField(min_length=8, max_length=32)

    postal_code    = forms.CharField(max_length=9)
    address_number = forms.CharField(max_length=6)

    cpf_cnpj       = forms.CharField(max_length=14)
    holder_name    = forms.CharField(max_length=100)
    number         = forms.CharField(max_length=19)
    expiry_date    = forms.CharField(max_length=5)
    ccv            = forms.CharField(max_length=4)

    def clean_plan(self):
        try:
            return Plan.objects.get(name__iexact=self.cleaned_data.get("plan"), active=True)
        except Plan.DoesNotExist:
            raise forms.ValidationError("Esse plano não existe ou está inativo no momento")

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado")

        return email

    def clean_phone_number(self):
        phone_number = re.sub(r"\D", "", self.cleaned_data["phone_number"])

        if len(phone_number) != 11:
            raise forms.ValidationError("Número de telefone inválido")

        return phone_number

    def clean_postal_code(self):
        return re.sub(r"\D", "", self.cleaned_data["postal_code"])

    def clean_cpf_cnpj(self):
        cpf_cnpj = re.sub(r"\D", "", self.cleaned_data["cpf_cnpj"])

        if len(cpf_cnpj) != 11:
            raise forms.ValidationError("Número de cpf inválido")

        return cpf_cnpj

    def clean_number(self):
        return re.sub(r"\D", "", self.cleaned_data["number"])

    def clean_expiry_date(self):
        try:
            expiry_date = [number for number in self.cleaned_data["expiry_date"].split("/")]
            if not (1 <= int(expiry_date[0]) <= 12):
                raise forms.ValidationError("Mês inválido")
            if not (24 <= int(expiry_date[1]) <= 99):
                raise forms.ValidationError("Ano inválido")
        except (IndexError, ValueError):
            raise forms.ValidationError("Data em formato incorreto")
        return expiry_date
