from django.core.mail import send_mail
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from django.contrib.auth.hashers import make_password
from event.serializers import EventListSerializer
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
            raise serializers.ValidationError("This User is already registered!")
        return email

    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match!')
        if not attrs['password'].isalnum():
            raise serializers.ValidationError('Password field must contain'
                                              'alpha symbols and numbers!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        user.send_activation_mail()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist')
        return email
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password')
        user =  User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid password')
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
            raise serializers.ValidationError()
        return email

    def send_reset_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        message = f"Code for restoring your password {user.activation_code}"
        send_mail(
            'Password restore',
            message,
            'test@gmail.com',
            [email]
        )


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
    

class ChangePasswordSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=4, required=True)

    class Meta:
        model = User
        fields = ('password', 'password_confirm')
    
    def validate(self, attrs):
        pass1 = attrs.get("password")
        pass2 = attrs.pop("password_confirm")
        if pass1 != pass2:
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def set_new_password(self):
        user = self.instance
        user.set_password(self.validated_data['password'])
        user.save()


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'last_name')
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['events_by_user'] = 'working on it'
        return rep