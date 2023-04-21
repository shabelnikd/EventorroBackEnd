from rest_framework import serializers
from .models import Event, EventDate
from category.models import Category
from django.conf import settings
from tickets.serializers import TicketSerializer

link = settings.LINK

class ChoiceListField(serializers.ChoiceField):
    def to_representation(self, value):
        # Find the label for the given value
        label = dict(self.choices)[value]
        # Return the label as the representation
        return label


class EventListSerializer(serializers.ModelSerializer):
    audience = ChoiceListField(choices=Event.AUDIENCE_CHOICES)
    age_limits = ChoiceListField(choices=Event.AGE)
    type_of_location = ChoiceListField(choices=Event.PLACES)
    type_of_location2 = ChoiceListField(choices=Event.PLACES)

    class Meta:
        model = Event
        fields = '__all__'
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        for i in range(1,6):
            repr.pop(f"image{i}")
        images = []
        if instance.image1:
            images.append({"image": f"{link}/media/{instance.image1}"})
        if instance.image2:
            images.append({"image": f"{link}/media/{instance.image2}"})
        if instance.image3:
            images.append({"image": f"{link}/media/{instance.image3}"})
        if instance.image4:
            images.append({"image": f"{link}/media/{instance.image4}"})
        if instance.image5:
            images.append({"image": f"{link}/media/{instance.image5}"})
        repr['images'] = images
        repr['categories'] = EventCategorySerializer(instance.categories, many=True).data
        repr['event_dates'] = EventDateListSerializer(instance.event_dates.exclude(status=True).order_by('date_time'), many=True).data
        repr['author'] = instance.author.email
        repr['tickets_count'] = instance.tickets_number
        repr['ticket_users'] = TicketSerializer(instance.tickets, many=True).data
        repr['poster'] = f"{link}/media/{instance.poster}"
        return repr


class EventDateSerializer(serializers.ModelSerializer):
    event = serializers.ReadOnlyField(source='event.id')

    class Meta:
        model = EventDate
        fields = ('date_time', "event")



class EventDateListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EventDate
        fields = ('date_time', )


class EventCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', )

class EventSerializer(serializers.ModelSerializer):
    event_dates = EventDateSerializer(many=True, required=True)
    categories = EventCategorySerializer(many=True, required=True)

    class Meta:
        model = Event
        fields = '__all__'

    
    
