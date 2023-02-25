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
        if self.action in ['list', 'retrieve']:
            return serializers.EventListSerializer
        return serializers.EventSerializer
    
    def get_queryset(self):
        queryset = Event.objects.all()
        category = self.request.query_params.get('main_category', None)
        side_category1 = self.request.query_params.get('side_category1', None)
        side_category2 = self.request.query_params.get('side_category2', None)
        side_category3 = self.request.query_params.get('side_category3', None)
        if category is not None:
            queryset = queryset.filter(main_category__name=category)
        if side_category1 is not None:
            queryset = queryset.filter(side_category1__name=side_category1)
        if side_category2 is not None:
            queryset = queryset.filter(side_category2__name=side_category2)
        if side_category3 is not None:
            queryset = queryset.filter(side_category3__name=side_category3)
        return queryset

    