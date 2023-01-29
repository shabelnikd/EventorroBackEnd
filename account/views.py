from rest_framework.views import APIView
from rest_framework.response import Response
from account.serializers import (RegistrationSerializer, ActivationSerializer, LoginSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = """
            Вы успешно зарегистрировались! 
            Вам отправлено письмо с кодом активации.
            """
            return Response(message)

class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return Response('Вы успешно активированы')

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer