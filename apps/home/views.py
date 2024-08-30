from django.views import View
from django.shortcuts import render


class Home(View):
    
    def get(self, request):
        return render(request, 'pages/home/index.html')
    

class TermsOfUse(View):

    def get(self, request):
        return render(request, 'pages/home/terms_of_use.html')
    

class PrivacyPolicy(View):

    def get(self, request):
        return render(request, 'pages/home/privacy_policy.html')
