from django.db import models
from event.models import Event
from django.core.mail import send_mail
from django.conf import settings

class Ticket(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')

    @staticmethod
    def send_ticket_mail(email, author, event, name, last_name):
        message = f"""
        Спасибо за регистрацию!

        Вы только что зарегистрировались на событие {event} организации {author}. 
        Подтверждаем, что Ваша регистрация прошла успешно.*

        *Просим обратить внимание, что данное пригласительное не является правом на бесплатный вход, если организаторы решат сделать событие платным. Так же оно не гарантирует вход на мероприятие быстрее живой очереди.

        Информация о заказчике
        Имя:
        {name} {last_name}
        E-mail:
        {email}
        """
        send_mail('Регистрация на событие',
            message,
            'eventorro@gmail.com',
            [email, ]
        )

    def __str__(self):
        return self.email

