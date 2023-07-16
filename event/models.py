from django.db import models
from category.models import Category
from account.models import User
    

class AgeLimit(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Audience(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.name

class Event(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='media/')
    categories = models.ManyToManyField(Category, related_name='events')
    audience = models.ForeignKey(Audience, on_delete=models.CASCADE, related_name='audiences')
    age_limits = models.ForeignKey(AgeLimit, on_delete=models.CASCADE, related_name='age_limit')
    price_from = models.IntegerField(null=True, blank=True)
    price_to = models.IntegerField(null=True, blank=True)
    video = models.CharField(max_length=200)
    description = models.TextField()
    type_of_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='types_of_location')
    tickets_number = models.IntegerField(null=True, blank=True)
    location_link = models.CharField(max_length=300)
    location_name = models.CharField(max_length=300)
    event_card_image = models.ImageField(upload_to='media/', null=True, blank=True)
    image1 = models.ImageField(upload_to='media/', null=True, blank=True)
    image2 = models.ImageField(upload_to='media/', null=True, blank=True)
    image3 = models.ImageField(upload_to='media/', null=True, blank=True)
    image4 = models.ImageField(upload_to='media/', null=True, blank=True)
    image5 = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    def get_image_url(self, field_name):
        image_field = getattr(self, field_name)
        return image_field.url


class EventDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_dates')
    date_time = models.DateTimeField()
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.date_time}"


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='favorites', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.email} -> {self.event.name}'


class Ticket(models.Model):
    user = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='tickets', on_delete=models.CASCADE)

    def __str__(self) -> str:
        if self.user:
            return f'{self.user.email} -> {self.event.name}'
        else:
            return 'deleted event or user tickets'
