from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, ForgotPasswordSerializer, \
    CreateNewPasswordSerializer, ChangePasswordSerializer, LoginSerializer,\
        UserHostDetailsSerializer, UserGuestDetailsSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .permissions import IsAuthor
from django.shortcuts import get_object_or_404, redirect
from .models import User
from .tasks import send_reset_email

class RegistrationView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Ваш аккаунт успешно зарегестрирован', status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return redirect('https://eventorro.live/')

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny, ]
    serializer_class = LoginSerializer


class ResetPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer())
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            send_reset_email(email)
            return Response('Код для восстановления пароля был выслан вам на почту', status=status.HTTP_200_OK)


class ResetPasswordCompleteView(APIView):
    @swagger_auto_schema(request_body=CreateNewPasswordSerializer())
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create_pass()
            return Response('Пароль восстановлен успешно', status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, IsAuthor]

    @swagger_auto_schema(request_body=ChangePasswordSerializer())
    def patch(self, request):
        serializer = ChangePasswordSerializer(request.user, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response(status=201)



class DetailsUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, email=None):
        if email is None:
            email = request.user.email
        user = get_object_or_404(User, email=email)
        if user.is_host:
            return Response(UserHostDetailsSerializer(user).data)
        return Response(UserGuestDetailsSerializer(user).data)

    def put(self, request, email=None):
        if email is None:
            email = request.user.email
        user = get_object_or_404(User, email=email)
        if user.is_host:
            serializer = UserHostDetailsSerializer(user, data=request.data, partial=True)
        else:
            serializer = UserGuestDetailsSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserEventsView(APIView):
    def get(self, request, email):
        email = self.kwargs.get('email')
        user = get_object_or_404(User, email=email)
        return Response(UserHostDetailsSerializer(user).data)