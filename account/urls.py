from django.urls import path

from . import views
from rest_framework_simplejwt.views import TokenRefreshView,  TokenObtainPairView

urlpatterns = [
    path('register/', views.RegistrarionView.as_view()),
    path('activation/', views.ActivationView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name="signin"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('reset_password/', views.ResetPasswordView.as_view()),
    path('reset_password_complete/', views.ResetPasswordCompleteView.as_view()),
    path('change_password/', views.ChangePasswordView.as_view()),
]
