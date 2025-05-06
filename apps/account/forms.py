from django import forms
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from apps.account.models import User


class CustomUserCreationForm(AdminUserCreationForm):

    class Meta:
        model = User
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = "__all__"


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8)


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8)

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado")

        return email
