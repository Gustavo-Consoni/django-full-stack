from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from apps.account.models import User
from apps.account.forms import UserChangeForm, UserCreationForm


@admin.register(User)
class UsersAdmin(auth_admin.UserAdmin):
    list_display = ["email", "first_name", "last_name", "is_staff"]
    form = UserChangeForm
    add_form = UserCreationForm
    model = User

    def get_list_display_links(self, request, list_display):
        return ["email"]
