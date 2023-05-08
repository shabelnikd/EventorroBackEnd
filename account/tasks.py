from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

@shared_task
def send_activation_mail(email, activation_code):
    activation_url = f'{settings.LINK}/api/v1/accounts/activate/{activation_code}'
    message = f"""
        Вы успешно зарегистрировались!
        Активируйте ваш аккаунт {activation_url}
    """
    send_mail('Активация аккаунта',
        message,
        'eventorro@gmail.com',
        [email, ]
    )


@shared_task
def send_reset_email(email):
    from .models import User
    user = User.objects.get(email=email)
    user.create_activation_code()
    message = f"Код для восстановления пароля {user.activation_code}"
    send_mail(
        'Восстановление пароля',
        message,
        'eventorro@gmail.com',
        [email]
    )