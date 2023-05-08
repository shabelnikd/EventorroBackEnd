from django.core.mail import send_mail
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from event.serializers import EventListSerializer, TicketSerializer
from event.models import Favorite, Event, Ticket
from django.conf import settings
from .tasks import send_activation_mail


LINK = settings.LINK
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)
    is_guest = serializers.BooleanField(default=False)
    is_host = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'name', 'last_name', 'is_guest', 'is_host', 'organization_name')

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
        send_activation_mail(user.email, user.activation_code)
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
        attrs['last_name'] = user.last_name
        attrs['name'] = user.name
        if user.is_host:
            attrs['events'] = EventListSerializer(user.events, many=True).data
            attrs['organization_name'] = user.organization_name
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Такого пользователя не существует')
        return email


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
        user.activation_code = ''
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


class FavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('event', )
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['event'] = EventListSerializer(Event.objects.get(id=instance.event_id)).data
        return rep


class UserHostDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'last_name', 'is_host', 'is_guest', 'organization_name', 'phone', 'avatar', 'bio', 'poster')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['events_by_user'] = EventListSerializer(instance.events.all(), many=True).data
        rep['phone'] = instance.phone
        if instance.avatar:
            rep['avatar'] = f"{LINK}/media/{instance.avatar}"
        else:
            rep['avatar'] = ""
        if instance.poster:
            rep['poster'] = f"{LINK}/media/{instance.poster}"
        else:
            rep['poster'] = ""
        rep['bio'] = instance.bio
        rep['saved'] = FavoriteListSerializer(instance.favorites.all(), many=True).data
        rep['tickets'] = TicketSerializer(instance.tickets.all(), many=True).data
        return rep


class UserGuestDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'last_name', 'is_host', 'is_guest', 'avatar', 'phone', 'organization_name')


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        try:
            rep.pop('organization_name')
        except:
            pass
        if instance.avatar:
            rep['avatar'] = f"{LINK}/media/{instance.avatar}"
        else:
            rep['avatar'] = ""
        rep['saved'] = FavoriteListSerializer(instance.favorites.all(), many=True).data
        rep['tickets'] = TicketSerializer(instance.tickets.all(), many=True).data
        return rep
