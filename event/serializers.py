from rest_framework import serializers
from .models import Event, EventDate, EventImages


LINK = 'http://localhost:8000/'

class AudienceField(serializers.ChoiceField):
    def to_representation(self, value):
        # Find the label for the given value
        label = dict(self.choices)[value]
        # Return the label as the representation
        return label


class EventListSerializer(serializers.ModelSerializer):
    audience = AudienceField(choices=Event.AUDIENCE_CHOICES)

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
        print(instance.event_dates)
        repr['event_dates'] = EventDateListSerializer(instance.event_dates.exclude(status=True).order_by('date_time'), many=True).data
        repr['images'] = EventImageSerializer(instance.images, many=True).data
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
        repr['image'] = f"{LINK}media/{instance.image}"
        return repr


class EventSerializer(serializers.ModelSerializer):
    event_dates = EventDateSerializer(many=True)
    images = EventImageSerializer(many=True, required=True)
    
    class Meta:
        model = Event
        fields = '__all__'















#     def create(self, validated_data):
#         event_dates_data = validated_data.pop('event_dates')
#         images = validated_data.pop('images')
#         event = Event.objects.create(**validated_data)
#         for event_date_data in event_dates_data:
#             EventDate.objects.create(event=event, **event_date_data)
#         for image in images:
#             image.update({'event_id': event.id})
#             img, created = EventImages.objects.get_or_create(**image)
#             event.images.add(img)
#         return event

#     def update(self, instance, validated_data):
#         images_data = validated_data.pop('images', [])
#         for image_data in images_data:
#             instance.images.create(**image_data)
#         return super().update(instance, validated_data)
    


# """
# Write an update function
# """