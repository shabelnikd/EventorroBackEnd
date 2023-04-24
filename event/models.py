from django.db import models
from category.models import Category
from account.models import User


class Event(models.Model):
    PLACES = (
        ('Бар', 'Бар'),
        ('Ресторан', 'Ресторан'),
        ('Кофейня', 'Кофейня'),
        ('Ночной клуб', 'Ночной клуб'),
        ('Концертный зал', 'Концертный зал'),
        ('Театр', 'Театр'),
        ('Музей', 'Музей'),
        ('На улице', 'На улице'),
        ('Учебное заведение', 'Учебное заведение'),
        ('Торговый центр', 'Торговый центр'),
        ('Кинотеатр', 'Кинотеатр' ),
        ('Отель', 'Отель'),
        ('Коворкинг', 'Коворкинг'),
        ('Караоке', 'Караоке' ),
        ('Кальянная', 'Кальянная'),
        ('Магазин', 'Магазин'),
        ('Конференц-зал', 'Конференц-зал'),
        ('Спортивный зал', 'Спортивный зал'),
        ('Салон красоты', 'Салон красоты'),
        ('Спа Центр', 'Спа Центр'),
        ('Тойкана', 'Тойкана'),
    )

    AUDIENCE_CHOICES = (
        ('Для всех', 'Для всех'),
        ('Для детей', 'Для детей'),
        ('Для женщин', 'Для женщин'),
        ('Для мужчин', 'Для мужчин'),
    )
    AGE = (
        ('Без ограничений', 'Без ограничений'),
        ('16+', '16+'),
        ('18+', '18+'),
        ('21+', '21+'),
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
    image1 = models.ImageField(upload_to='media/', null=True, blank=True)
    image2 = models.ImageField(upload_to='media/', null=True, blank=True)
    image3 = models.ImageField(upload_to='media/', null=True, blank=True)
    image4 = models.ImageField(upload_to='media/', null=True, blank=True)
    image5 = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class EventDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_dates')
    date_time = models.DateTimeField()
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.date_time}"


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='favorites', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email} -> {self.event.name}'