from django.db import models
from category.models import Category


class HashTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    AUDIENCE_CHOICES = (
        ('1', 'Для мужчин'),
        ('2', 'Для женщин'),
        ('3', 'Для всех'),
    )
    AGE = (
        ('1', '21+'),
        ('2', '18+'),
        ('3', '16+'),
        ('4', 'Без ограничений'),
    ) 

    name = models.CharField(max_length=200)
    main_category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='main_events', null=True)
    side_category1 = models.ForeignKey(Category,on_delete=models.SET_NULL, related_name='side_events1', blank=True, null=True)
    side_category2 = models.ForeignKey(Category,on_delete=models.SET_NULL, related_name='side_events2', blank=True, null=True)
    side_category3 = models.ForeignKey(Category,on_delete=models.SET_NULL, related_name='side_events3', blank=True, null=True)
    hashtag = models.ManyToManyField(HashTag, related_name='events')
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
