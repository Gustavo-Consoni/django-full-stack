from django.urls import path
from apps.account import views


urlpatterns = [
    path('entrar', views.Login.as_view(), name='login'),
    path('registrar', views.Register.as_view(), name='register'),
    path('sair', views.Logout.as_view(), name='logout'),
    path('redefinir_senha', views.PasswordReset.as_view(), name='password_reset'),
    path('redefinir_senha_concluir', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('redefinir_senha_confirmar/<uidb64>/<token>', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('ativar_conta/<uidb64>/<token>', views.ActiveAccount.as_view(), name="active_account"),
]
