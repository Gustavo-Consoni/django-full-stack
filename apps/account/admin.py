from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from apps.account.models import User
from apps.account.forms import UserChangeForm, UserCreationForm


@admin.register(User)
class UsersAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
