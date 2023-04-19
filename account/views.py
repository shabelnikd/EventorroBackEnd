from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import RegisterSerializer, ForgotPasswordSerializer, \
    CreateNewPasswordSerializer, ChangePasswordSerializer, LoginSerializer, UserDetailsSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .permissions import IsAuthor
from django.shortcuts import get_object_or_404
from .models import User
from django.conf import settings
from .models import Profile


class RegistrarionView(APIView):
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
        return Response({'redirect': f"{settings.DOMAIN}/api/v1/accounts/login/"}, status=302)

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny, ]
    serializer_class = LoginSerializer


class ResetPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer())
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_reset_email()
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
        return Response(UserDetailsSerializer(user).data)

    def put(self, request, email=None):
        if email is None:
            email = request.user.email
        user = get_object_or_404(User, email=email)
        serializer = UserDetailsSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class ProfileViewSet(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthor]
#     lookup_field = 'user__email'
#     lookup_url_kwarg = 'user__email'

    
#     def patch(self, request, *args, **kwargs):
#         user_data = ('first_name', 'last_name', 'is_guest', 'is_host')
#         user = User.objects.get(email=kwargs['user__email'])
#         for data in user_data:
#             if data in request.data:
#                 setattr(user, data, request.data[data])
#             elif data in request.data.get('user', {}):
#                 setattr(user, data, request.data['user'][data])
#         user.save()
#         return super().patch(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.patch(request, *args, **kwargs)