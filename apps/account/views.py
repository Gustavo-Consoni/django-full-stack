from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout, views
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from apps.account.models import User
from apps.account.forms import AuthForm


class Login(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, 'pages/account/login.html')
    
    def post(self, request):
        form = AuthForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
        else:
            return render(request, 'pages/account/login.html', {'form': form})
        
        user = authenticate(request, username=email, password=password)
        if not user:
            messages.error(request, 'Email ou senha incorretos')
            return render(request, 'pages/account/login.html')
        
        if user.is_active:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ative sua conta pelo email')
            return redirect('login')


class Register(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        return render(request, 'pages/account/register.html')

    def post(self, request):
        form = AuthForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
        else:
            return render(request, 'pages/account/register.html', {'form': form})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já existe')
            return render(request, 'pages/account/register.html')

        user = User.objects.create_user(email=email, password=password, is_active=False)

        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('pages/account/activate_account_email.html', {
            'user': user,
            'protocol': 'https' if request.is_secure() else 'http',
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()
        return render(request, 'pages/account/activate_account.html')


class ActiveAccount(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Conta ativada')
        else:
            messages.error(request, 'Codigo de ativação inválido')
        return redirect('login')


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('/')


class PasswordReset(views.PasswordResetView):
    template_name = 'pages/account/password_reset_form.html'
    email_template_name = 'pages/account/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDone(views.PasswordResetDoneView):
    template_name = 'pages/account/password_reset_done.html'


class PasswordResetConfirm(views.PasswordResetConfirmView):
    template_name = 'pages/account/password_reset_confirm.html'
    success_url = reverse_lazy('login')
