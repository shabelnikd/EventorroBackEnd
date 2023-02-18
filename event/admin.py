from django.contrib import admin
from .models import Event, HashTag, EventImages, EventVideos, EventDate
# Register your models here.

# admin.site.register(Event)
admin.site.register(HashTag)
class EventImagesInLine(admin.StackedInline):
    model = EventImages
    display = ('image')

class EventVideosInLine(admin.StackedInline):
    model = EventVideos
    display = ('video')

class EventDateInLine(admin.StackedInline):
    model = EventDate
    display = ('date')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    display = '__all__'
    inlines = [
        EventImagesInLine,
        EventVideosInLine,
        EventDateInLine,
    ]
