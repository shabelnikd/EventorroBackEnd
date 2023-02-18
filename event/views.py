from rest_framework.viewsets import ModelViewSet
from .models import Event
from . import serializers
from .paginator import EventPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EventFilter

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all().order_by('-event_dates__date_time')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilter
    pagination_class = EventPagination



    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.EventListSerializer
        return serializers.EventSerializer
    