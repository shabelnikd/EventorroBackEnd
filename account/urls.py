from django.urls import path

from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('activate/<str:activation_code>/', views.ActivationView.as_view()),
    path('login/', views.LoginView.as_view(), name="signin"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', views.DetailsUserView.as_view()),
    path('reset_password/', views.ResetPasswordView.as_view()),
    path('reset_password_complete/', views.ResetPasswordCompleteView.as_view()),
    path('change_password/', views.ChangePasswordView.as_view()),
    path('events_by/<str:email>/', views.UserEventsView.as_view()),
]
