from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.db import models

from django.core.mail import send_mail


class UserManager(BaseUserManager):
    def _create(self, phone, password, name, last_name, **extra_fields):
        if not phone:
            raise ValueError('Телефон не может быть пустым')
        user = self.model(phone=phone, name=name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, phone, password, name, last_name, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        return self._create(phone, password, name, last_name, **extra_fields)

    def create_superuser(self, phone, password, name, last_name, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self._create(phone, password, name, last_name, **extra_fields)


class User(AbstractBaseUser):
    phone = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)
    is_host = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', 'last_name']

    def __str__(self):
        return self.phone

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj):
        return self.is_staff

    @staticmethod
    def generate_activation_code():
        from django.utils.crypto import get_random_string
        code = get_random_string(6, '0123456789')
        return code
    def set_activation_code(self):
        code = self.generate_activation_code()
        if User.objects.filter(activation_code=code).exists():
            self.set_activation_code()
        else:
            self.activation_code = code
            self.save()

    def send_activation_sms(self):
        from django.conf import settings
        from twilio.rest import Client
        message = f'{self.activation_code}'
        print(message)

        client = Client(settings.TWILIO_SID,
                        settings.TWILIO_AUTH_TOKEN)

        # client.messages.create(body=message,from_=settings.TWILIO_NUMBER,to=self.phone)
        print('DDDOOOOOOOOOOOOOOOOOOOOONEEEEEEEEEEE')
                            #    from_=settings.TWILIO_NUMBER,
                               
                            #    to=self.phone)
        
    # def send_activation_mail(self):
    #     message = f"""
    #     Здравствуйте! Спасибо за регистрацию на нашем сайте!
    #     Ваш код активации: {self.activation_code}
    #     """
    #     send_mail(
    #         "Подтверждение аккаунта",
    #         message,
    #         "test@gmail.com",
    #         [self.phone]
    #     )