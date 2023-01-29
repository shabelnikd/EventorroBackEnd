from django.urls import path
from account.views import (RegistrationView, ActivationView, LoginView)
urlpatterns = [
    path('register/', RegistrationView.as_view(), name="registration"),
    path('activate/', ActivationView.as_view(), name="activation"),
    path('login/', LoginView.as_view(), name="signin"),
]
