from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from twilio.rest import Client
from django.conf import settings
from twilio.rest import Client
User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20,
                                  required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)
    name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_guest = serializers.BooleanField(default=False)
    is_host = serializers.BooleanField(default=False)

    def validate_phone(self, phone):
        import re
        phone = re.sub('[^0-9]', '', phone)
        if phone.startswith('0'):
            phone = f'996{phone[1:]}'
        phone = f'+{phone}'
        if len(phone) != 13 and not phone.startswith('+996'):
            raise serializers.ValidationError('Неверный формат номера')
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('Номер уже занят')
        return phone

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.pop('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def save(self):
        data = self.validated_data
        user = User.objects.create_user(**data)
        user.set_activation_code()
        user.send_activation_sms()


class ActivationSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    activation_code = serializers.CharField(max_length=6,
                                            min_length=6)

    def validate(self, attrs):
        phone = attrs.get('phone')
        activation_code = attrs.get('activation_code')

        if not User.objects.filter(phone=phone,
                                   activation_code=activation_code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return attrs

    def activate(self):
        phone = self.validated_data.get('phone')
        user = User.objects.get(phone=phone)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(TokenObtainPairSerializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(min_length=6, required=True)


    def validate_phone(self, phone):
        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return phone

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.pop('password')
        user = User.objects.get(phone=phone)
        if not user.check_password(password):
            raise serializers.ValidationError('Неверный пароль')
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)

    def validate_phone(self, phone):
        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError('Пользователь с этим номером не зарегестрирован')
        print('PHONE IS VALIDATED')
        return phone

    def send_reset_sms(self):
        phone = self.validated_data.get('phone')
        user = User.objects.get(phone=phone)
        user.set_activation_code()
        message = f"Code for restoring your password {user.activation_code}"
        client = Client(settings.TWILIO_SID,
                        settings.TWILIO_AUTH_TOKEN)

        # client.messages.create(body=message,from_=settings.TWILIO_NUMBER,to=user.phone)


class CreateNewPasswordSerializer(serializers.Serializer):
    activation_code = serializers.CharField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    def validate_activation_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Activation code seems to be incorrect')
        return code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def create_pass(self):
        code = self.validated_data.get('activation_code')
        password = self.validated_data.get('password')
        user = User.objects.get(activation_code=code)
        user.set_password(password)
        user.save()