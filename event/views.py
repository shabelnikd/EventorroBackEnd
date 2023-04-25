from rest_framework.viewsets import GenericViewSet
from . import serializers
from .paginator import EventPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EventFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAuthor
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Event, EventDate, Favorite
from rest_framework import status, mixins
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q



class EventViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Event.objects.all().order_by('-event_dates__date_time')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilter
    pagination_class = EventPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.EventListSerializer
        return serializers.EventSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action in ['update_event', 'delete_event']:
            return [IsAuthor()]
        else:
            return [IsAuthenticated()]


    def get_queryset(self):
        queryset = Event.objects.all()
        audience = self.request.query_params.get('audience')
        age_limits = self.request.query_params.get('age_limits')
        type_of_location = self.request.query_params.get('type_of_location')
        type_of_location2 = self.request.query_params.get('type_of_location2')
        price_from = self.request.query_params.get('price_from')
        price_to = self.request.query_params.get('price_to')

        # Use select_related to optimize related object queries
        queryset = queryset.select_related('author')

        # Use Q object to combine multiple filters
        filters = Q()
        category_ids = self.request.query_params.getlist('category', [])
        if category_ids:
            filters &= Q(categories__id__in=category_ids)
        if audience:
            filters &= Q(audience=audience)
        if age_limits:
            if age_limits[0:-1].isdigit():
                age_limits += '+'
                age_limits = "".join(age_limits.split())
            filters &= Q(age_limits=age_limits)
        if type_of_location:
            filters &= Q(type_of_location=type_of_location)
        if type_of_location2:
            filters &= Q(type_of_location2=type_of_location2)
        if price_from and price_to:
            filters &= Q(price__range=(price_from, price_to))
        elif price_from:
            filters &= Q(price__range=(price_from, 1000_000))
        elif price_to:
            filters &= Q(price__range=(0, price_to))

        # Apply filters to queryset
        queryset = queryset.filter(filters)
        return queryset
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('category', openapi.IN_QUERY, description='Description of audience', type=openapi.TYPE_STRING),
        openapi.Parameter('audience', openapi.IN_QUERY, description='Description of audience', type=openapi.TYPE_STRING),
        openapi.Parameter('age_limits', openapi.IN_QUERY, description='Description of age_limits', type=openapi.TYPE_STRING),
        openapi.Parameter('type_of_location', openapi.IN_QUERY, description='Description of type_of_location', type=openapi.TYPE_STRING),
        openapi.Parameter('type_of_location2', openapi.IN_QUERY, description='Description of type_of_location2', type=openapi.TYPE_STRING),
        openapi.Parameter('price_from' and 'price_to', openapi.IN_QUERY, description='Description of price_from and price_to', type=openapi.TYPE_STRING),

    ])
    def list(self, request, *args, **kwargs):
        queryset = sorted(self.get_queryset(), 
            key=lambda x: x.event_dates.filter(
            id__in=EventDate.objects.filter(status=False)
            ).first().date_time)
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(request_body=serializers.EventSerializer())
    def create_event(self, request):
        name = request.data.get('name')
        author = request.user.id
        description = request.data.get('description')
        price = request.data.get('price')
        video = request.data.get('video')
        image1 = request.data.get('image1')
        image2 = request.data.get('image2')
        image3 = request.data.get('image3')
        image4 = request.data.get('image4')
        image5 = request.data.get('image5')
        location_link = request.data.get('location_link')
        age_limits = request.data.get('age_limits')
        audience = request.data.get('audience')
        type_of_location = request.data.get('type_of_location')
        type_of_location2 = request.data.get('type_of_location2')
        poster = request.data.get('poster')

        event = Event.objects.create(name=name, description=description, price=price, video=video, location_link=location_link, age_limits=age_limits,  audience=audience, author_id=author, poster=poster, image1=image1, image2=image2, image3=image3, image4=image4, image5=image5, type_of_location=type_of_location, type_of_location2=type_of_location2)

        if request.POST.getlist('categories[]'):
            categories = request.POST.getlist('categories[]')
            for cat in categories:
                event.categories.add(cat)

        # Create EventDate objects
        if request.POST.getlist('event_dates[]'): #[{"date_time": "2020-05"}]
            event_dates = request.POST.getlist('event_dates[]')
            for event_date in event_dates:
                event.event_dates.create(date_time=event_date, status=bool(False))
        else:
            return Response({"error": "dates are must"}, status=404)
    
        return Response(serializers.EventListSerializer(event).data, status=201)
        

    @action(detail=True, methods=['put'])
    def update_event(self, request, pk=None):
        self.check_object_permissions(request, self.get_object())
        try:
            event = self.get_queryset().get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name')
        description = request.data.get('description')
        price = request.data.get('price')
        video = request.data.get('video')
        image1 = request.data.get('image1')
        image2 = request.data.get('image2')
        image3 = request.data.get('image3')
        image4 = request.data.get('image4')
        image5 = request.data.get('image5')
        location_link = request.data.get('location_link')
        age_limits = request.data.get('age_limits')
        audience = request.data.get('audience')
        type_of_location = request.data.get('type_of_location')
        type_of_location2 = request.data.get('type_of_location2')
        poster = request.data.get('poster')
        tickets_count = request.data.get('tickets_count')

        event.name = name
        event.description = description
        event.price = price
        event.video = video
        event.location_link = location_link
        event.age_limits = age_limits
        event.audience = audience
        event.type_of_location = type_of_location
        event.type_of_location2 = type_of_location2
        event.poster = poster
        event.image1 = image1
        event.image2 = image2
        event.image3 = image3
        event.image4 = image4
        event.image5 = image5
        event.tickets_number = tickets_count
        event.save()

        # Update EventDates objects
        if request.POST.getlist('event_dates[]'):
            event_dates = request.POST.getlist('event_dates[]')
            event.event_dates.all().delete()
            for event_date in event_dates:
                event.event_dates.get_or_create(date_time=event_date, status=bool(False))

        if request.POST.getlist('categories[]'):
            categories = request.POST.getlist('categories[]')
            event.categories.all().delete()
            for cat in categories:
                event.categories.add(cat)

        # serializer = self.get_serializer(event)
        return Response(serializers.EventListSerializer(event).data)

    @action(detail=True, methods=['delete'])
    def delete_event(self, request, pk=None):
        self.check_object_permissions(request, self.get_object())
        try:
            event = self.get_queryset().get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        event.delete()
        return Response({'success': 'Event deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['GET'])
    def add_favorite(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=401)
        event = get_object_or_404(Event, id=pk)
        if Favorite.objects.filter(user=request.user, event=event).exists():
            Favorite.objects.filter(user=request.user, event=event).delete()
            return Response('удалено')
        else:
            Favorite.objects.create(user=request.user, event=event)
        return Response('сохранено', status=201)