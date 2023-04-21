from django.db import models
from category.models import Category
from account.models import User


class Event(models.Model):
    PLACES = (
        ('1', 'Бар'),
        ('2', 'Ресторан'),
        ('3', 'Кофейня'),
        ('4', 'Ночной клуб'),
        ('5', 'Концертный зал'),
        ('6', 'Театр'),
        ('7', 'Музей'),
        ('8', 'На улице'),
        ('9', 'Учебное заведение'),
        ('10', 'Торговый центр'),
        ('11', 'Кинотеатр' ),
        ('12', 'Отель'),
        ('13', 'Коворкинг'),
        ('14', 'Караоке' ),
        ('15', 'Кальянная'),
        ('16', 'Магазин'),
        ('17', 'Конференц-зал'),
        ('18', 'Спортивный зал'),
        ('19', 'Салон красоты'),
        ('20', 'Спа Центр'),
        ('21', 'Тойкана'),
    )

    AUDIENCE_CHOICES = (
        ('1', 'Для всех'),
        ('2', 'Для детей'),
        ('3', 'Для женщин'),
        ('4', 'Для мужчин'),
    )
    AGE = (
        ('1', 'Без ограничений'),
        ('2', '16+'),
        ('3', '18+'),
        ('4', '21+'),
    ) 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='media/')
    categories = models.ManyToManyField(Category, related_name='events')
    audience = models.CharField(max_length=50, choices=AUDIENCE_CHOICES)
    age_limits = models.CharField(max_length=50, choices=AGE)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    video = models.CharField(max_length=200)
    description = models.TextField()
    type_of_location = models.CharField(max_length=200, choices=PLACES)
    type_of_location2 = models.CharField(max_length=200, choices=PLACES, null=True, blank=True)
    tickets_number = models.IntegerField(null=True, blank=True)
    location_link = models.CharField(max_length=200)


    def __str__(self) -> str:
        return self.name


class EventDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_dates')
    date_time = models.DateTimeField()
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.date_time}"

class EventImages(models.Model):
    image = models.FileField(upload_to='media/')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')


