from django.urls import path
from account.views import (RegistrationView, ActivationView, LoginView, ResetPasswordView, ResetPasswordCompleteView)
urlpatterns = [
    path('register/', RegistrationView.as_view(), name="registration"),
    path('activate/', ActivationView.as_view(), name="activation"),
    path('login/', LoginView.as_view(), name="signin"),
    path('reset_password/', ResetPasswordView.as_view()),
    path('reset_password_complete/', ResetPasswordCompleteView.as_view()),
]
