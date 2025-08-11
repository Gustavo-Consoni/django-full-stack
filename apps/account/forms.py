from django import forms
from apps.account.models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8, max_length=32)


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8, max_length=32)

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado")

        return email
