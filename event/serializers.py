from rest_framework import serializers
from .models import Event, HashTag, EventDate, EventImages, EventVideos


class HashTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = HashTag
        fields = ('name', )


class EventListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['main_category'] = instance.main_category.name
        if repr['side_category1']:
            repr['side_category1'] = instance.side_category1.name
        if repr['side_category2']:
            repr['side_category2'] = instance.side_category2.name
        if repr['side_category3']:
            repr['side_category3'] = instance.side_category3.name
        repr['hashtag'] = HashTagSerializer(instance.hashtag.values(), many=True).data
        repr['date_time'] = EventDateListSerializer(instance.event_dates, many=True).data
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
        fields = ('image', 'event')


class EventVideoSerializer(serializers.ModelSerializer):
    event = serializers.ReadOnlyField(source='event.id')

    class Meta:
        model = EventVideos
        fields = ('video', 'event')


class EventSerializer(serializers.ModelSerializer):
    event_dates = EventDateSerializer(many=True)
    hashtag = HashTagSerializer(many=True)
    images = EventImageSerializer(many=True, required=True)
    videos = EventVideoSerializer(many=True, required=True)
    
    class Meta:
        model = Event
        fields = '__all__'
        # ordering = ['event_dates__date_time']
    
    def create(self, validated_data):
        tags_data = validated_data.pop('hashtag')
        event_dates_data = validated_data.pop('event_dates')
        images = validated_data.pop('images')
        videos = validated_data.pop('videos')
        event = Event.objects.create(**validated_data)
        for event_date_data in event_dates_data:
            EventDate.objects.create(event=event, **event_date_data)
        for tag_data in tags_data:
            tag, created = HashTag.objects.get_or_create(**tag_data)
            event.hashtag.add(tag)
        for image in images:
            img, created = EventImages.objects.get_or_create(**image)
            event.images.add(img)
        for video in videos:
            vid, created = EventVideos.objects.get_or_create(**video)
            event.videos.add(vid)
        return event