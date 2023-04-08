from django.contrib import admin
from .models import Event, EventImages, EventDate
# Register your models here.

# admin.site.register(Event)
class EventImagesInLine(admin.StackedInline):
    model = EventImages
    display = ('image')

class EventDateInLine(admin.StackedInline):
    model = EventDate
    display = ('date')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    display = '__all__'
    inlines = [
        EventImagesInLine,
        EventDateInLine,
    ]



