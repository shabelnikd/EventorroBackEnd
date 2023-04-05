from django.db import models
from category.models import Category
from account.models import User


class Event(models.Model):
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
    main_category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='main_events', null=True)
    side_category1 = models.ForeignKey(Category,on_delete=models.SET_NULL, related_name='side_events1', blank=True, null=True)
    side_category2 = models.ForeignKey(Category,on_delete=models.SET_NULL, related_name='side_events2', blank=True, null=True)
    audience = models.CharField(max_length=6, choices=AUDIENCE_CHOICES)
    age_limits = models.CharField(max_length=6, choices=AGE)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    video = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    location_link = models.CharField(max_length=200)
    contacts = models.CharField(max_length=50)


    def __str__(self) -> str:
        return self.name


class EventDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_dates')
    date_time = models.DateTimeField()
    status = models.BooleanField(default=False)

class EventImages(models.Model):
    image = models.FileField(upload_to='media/')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
