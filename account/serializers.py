from django.core.mail import send_mail
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from event.serializers import EventListSerializer
from .models import Profile
from django.conf import settings


LINK = settings.LINK
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)
    is_guest = serializers.BooleanField(default=False)
    is_host = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'name', 'last_name', 'is_guest', 'is_host')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с этой почтой уже существует!")
        return email

    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        user.send_activation_mail()
        profile = Profile.objects.create(user=user)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Такого пользователя нет')
        return email
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password')
        user =  User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError('Неверный пароль')
        if not user.is_active:
            raise serializers.ValidationError('Активируйте свою учетную запись через email')
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        attrs['is_guest'] = user.is_guest
        attrs['is_host'] = user.is_host
        attrs['events'] = EventListSerializer(user.events, many=True).data
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Такого пользователя не существует')
        return email

    def send_reset_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        message = f"Код для восстановления пароля {user.activation_code}"
        send_mail(
            'Восстановление пароля',
            message,
            'eventorro@gmail.com',
            [email]
        )


class CreateNewPasswordSerializer(serializers.Serializer):
    activation_code = serializers.CharField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    def validate_activation_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Активационный код введен неверно')
        return code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create_pass(self):
        code = self.validated_data.get('activation_code')
        password = self.validated_data.get('password')
        user = User.objects.get(activation_code=code)
        user.set_password(password)
        user.save()
    

class ChangePasswordSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=4, required=True)

    class Meta:
        model = User
        fields = ('password', 'password_confirm')
    
    def validate(self, attrs):
        pass1 = attrs.get("password")
        pass2 = attrs.pop("password_confirm")
        if pass1 != pass2:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs
    
    def set_new_password(self):
        user = self.instance
        user.set_password(self.validated_data['password'])
        user.save()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.email
        rep['avatar'] = f"{LINK}/media/{instance.avatar}"
        rep['is_guest'] = instance.user.is_guest
        rep['is_host'] = instance.user.is_host
        print(instance.avatar)
        if instance.user.is_host == True:
            rep['events_by_user'] = EventListSerializer(instance.user.events, many=True).data
        else:
            try:
                rep.pop('telegram')
                rep.pop('whatsapp')
                rep.pop('instagram')
                rep.pop('phone_number')
            except:
                return rep
        return rep