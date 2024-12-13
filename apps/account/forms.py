from django import forms
from django.contrib.auth import forms as auth_forms
from apps.account.models import User


class UserChangeForm(auth_forms.UserChangeForm):

    class Meta(auth_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(auth_forms.UserCreationForm):

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8)
