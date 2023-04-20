from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
import jwt

class UserManager(BaseUserManager):
    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email cannot be blank')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.create_activation_code()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)
    is_host = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, blank=True)
    telegram = models.CharField(max_length=50, blank=True, null=True)
    whatsapp = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to='media/', blank=True, null=True)
    poster = models.ImageField(upload_to='media/', blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(8, '0123456789')
        self.activation_code = code
        self.save()

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def send_activation_mail(self):
        activation_url = f'{settings.LINK}/api/v1/accounts/activate/{self.activation_code}'
        message = f"""
            Вы успешно зарегестрировались!
            Активируйте ваш аккаунт {activation_url}
        """
        send_mail('Активация аккаунта',
            message,
            'eventorro@gmail.com',
            [self.email, ]
        )


    @property
    def token(self):
        return self._generate_jwt_token()


    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
