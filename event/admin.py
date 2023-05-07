from django.contrib import admin
from .models import Event, EventDate, Favorite, Ticket, Audience, Location, AgeLimit

class EventDateInLine(admin.StackedInline):
    model = EventDate
    display = ('date')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    display = '__all__'
    inlines = [
        EventDateInLine,
    ]



admin.site.register(Favorite)
admin.site.register(Ticket)
admin.site.register(AgeLimit)
admin.site.register(Location)
admin.site.register(Audience)

