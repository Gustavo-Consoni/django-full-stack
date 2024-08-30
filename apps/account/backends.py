from django.contrib.auth.backends import ModelBackend, UserModel


class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(email__iexact=username)
        except UserModel.DoesNotExist:
            return

        if user.check_password(password):
            return user
