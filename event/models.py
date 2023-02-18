from django.db import models
from category.models import Category


class HashTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    main_category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='main_events', null=True)
    side_category1 = models.ForeignKey(Category,on_delete=models.SET_NULL, related_name='side_events1', blank=True, null=True)
    side_category2 = models.ForeignKey(Category,on_delete=models.SET_NULL, related_name='side_events2', blank=True, null=True)
    side_category3 = models.ForeignKey(Category,on_delete=models.SET_NULL, related_name='side_events3', blank=True, null=True)
    for_kids = models.BooleanField(default=False, blank=True, null=True)
    for_adults = models.BooleanField(default=False, blank=True, null=True)
    free = models.BooleanField(default=False, blank=True, null=True)
    hashtag = models.ManyToManyField(HashTag, related_name='events')
    description = models.TextField()
    location = models.CharField(max_length=200)
    location_link = models.CharField(max_length=200)
    contacts = models.CharField(max_length=50)


    def __str__(self) -> str:
        return self.name


class EventDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_dates')
    date_time = models.DateTimeField()


class EventImages(models.Model):
    image = models.CharField(max_length=500)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')


class EventVideos(models.Model):
    video = models.CharField(max_length=500)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='videos')