from django.urls import path
from apps.home import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('termos-de-uso', views.TermsOfUse.as_view(), name='terms_of_use'),
    path('politica-de-privacidade', views.PrivacyPolicy.as_view(), name='privacy_policy'),
]
