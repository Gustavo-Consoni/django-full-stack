from django.urls import path
from apps.account import views


urlpatterns = [
    path('entrar', views.Login.as_view(), name='login'),
    path('registrar', views.Register.as_view(), name='register'),
    path('sair', views.Logout.as_view(), name='logout'),
    path('redefinir-senha', views.PasswordReset.as_view(), name='password_reset'),
    path('redefinir-senha-concluir', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('redefinir-senha-confirmar/<uidb64>/<token>', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('ativar-conta/<uidb64>/<token>', views.ActiveAccount.as_view(), name='active_account'),
]
