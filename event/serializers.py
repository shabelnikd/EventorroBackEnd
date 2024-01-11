from rest_framework import serializers
from .models import Event, EventDate, Ticket, AgeLimit, Audience, Location
from category.models import Category
from django.conf import settings

link = settings.LINK


class EventListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        for i in range(1,6):
            repr.pop(f"image{i}")
        images = []
        for i in range(1, 6):
            image_field = getattr(instance, f"image{i}", None)
            if image_field:
                image_url = instance.get_image_url(f"image{i}")
                images.append({"image": f"{settings.LINK}{image_url}"})
        repr['images'] = images
        repr['categories'] = EventCategorySerializer(instance.categories, many=True).data
        repr['event_dates'] = EventDateListSerializer(instance.event_dates.exclude(status=True).order_by('date_time'), many=True).data
        repr['audience'] = instance.audience.name
        repr['type_of_location'] = instance.type_of_location.name
        repr['age_limits'] = instance.age_limits.name
        repr['author'] = instance.author.email
        repr['tickets_number'] = instance.tickets_number
        repr['ticket_users'] = TicketSerializer(instance.tickets, many=True).data
        repr['poster'] = f"{settings.LINK}{instance.get_image_url('poster')}"
        repr['event_language'] = instance.event_language	
        if instance.event_card_image:
            repr['event_card_image'] = f"{settings.LINK}{instance.get_image_url('event_card_image')}"    
        return repr

    
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        exclude = ('event', 'user')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['event'] = instance.event.name
        if instance.event.author.organization_name:
            rep['organization'] = instance.event.author.organization_name
        rep['user_id'] = instance.user.id
        rep['name'] = instance.user.name
        rep['last_name'] = instance.user.last_name
        rep['email'] = instance.user.email
        return rep
    

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


    
class AgeLimitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeLimit
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AudienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audience
        fields = '__all__'
