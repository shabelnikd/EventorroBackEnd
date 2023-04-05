from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, ActivationSerializer, ForgotPasswordSerializer, \
    CreateNewPasswordSerializer, ChangePasswordSerializer, LoginSerializer, UserDetailsSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .permissions import IsAuthor
from django.shortcuts import get_object_or_404
from .models import User

'''
1. Регистрация 
2. Активация
3. Логин
4. Восстановление пароля
5. Смена пароля
6. Профиль пользователя
'''


class RegistrarionView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Your account successfully registered', status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    @swagger_auto_schema(request_body=ActivationSerializer())
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return Response('Your account is successfully activated', status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny, ]
    serializer_class = LoginSerializer


class ResetPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer())
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_reset_email()
            return Response('Code for password restore was sent to your email', status=status.HTTP_200_OK)


class ResetPasswordCompleteView(APIView):
    @swagger_auto_schema(request_body=CreateNewPasswordSerializer())
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create_pass()
            return Response('Password was restored successfully', status=status.HTTP_200_OK)


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
        return Response(UserDetailsSerializer(user).data)