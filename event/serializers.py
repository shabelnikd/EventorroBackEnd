from rest_framework import serializers
from .models import Event, EventDate, EventImages
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
        if repr['main_category']:
            repr['main_category'] = instance.main_category.name
        if repr['side_category1']:
            repr['side_category1'] = instance.side_category1.name
        if repr['side_category2']:
            repr['side_category2'] = instance.side_category2.name
        repr['event_dates'] = EventDateListSerializer(instance.event_dates.exclude(status=True).order_by('date_time'), many=True).data
        repr['images'] = EventImageSerializer(instance.images, many=True).data
        repr['author'] = instance.author.email
        repr['tickets_count'] = instance.tickets_number
        repr['ticket_users'] = TicketSerializer(instance.tickets, many=True).data
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


class EventImageSerializer(serializers.ModelSerializer):
    event = serializers.ReadOnlyField(source='event.id')

    class Meta:
        model = EventImages
        fields = ('image', 'event', 'id')
    
    def to_representation(self, instance):
        
        repr = super().to_representation(instance)
        repr['image'] = f"{link}/media/{instance.image}"
        return repr


class EventSerializer(serializers.ModelSerializer):
    event_dates = EventDateSerializer(many=True, required=True)
    images = EventImageSerializer(many=True, required=True)
    
    class Meta:
        model = Event
        fields = '__all__'
    
