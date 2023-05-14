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
from .models import Event, EventDate, Favorite, Ticket, Audience, Location, AgeLimit
from rest_framework.generics import ListAPIView
from rest_framework import status, mixins
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from .extra import send_mails



class EventViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Event.objects.all().order_by('-event_dates__date_time')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilter
    pagination_class = EventPagination
    # lookup_url_kwarg = 'event_name'

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
        queryset = Event.objects.filter(event_dates__status=False)
        audience = self.request.query_params.get('audience')
        age_limits = self.request.query_params.get('age_limits')
        type_of_location = self.request.query_params.get('type_of_location')
        price_from = self.request.query_params.get('price_from')
        price_to = self.request.query_params.get('price_to')
        date = self.request.query_params.get('date')

        if date:
            # Filter events that have an EventDate with the specified date
            queryset = queryset.filter(
                Q(event_dates__date_time__date=date)
            ).distinct()
        # Use select_related to optimize related object queries
        queryset = queryset.select_related('author')

        # Use Q object to combine multiple filters
        filters = Q()
        category_ids = self.request.query_params.getlist('category', [])
        if category_ids:
            filters &= Q(categories__id__in=category_ids)
        if audience:
            filters &= Q(audience__name=audience)
        if age_limits:
            if age_limits.isdigit():
                age_limits += '+'
            filters &= Q(age_limits__name=age_limits)
        if type_of_location:
            filters &= Q(type_of_location__name=type_of_location)
        if price_from and price_to:
            filters &= Q(price_from__lte=price_from, price_to__lte=price_to)
        elif price_from:
            filters &= Q(price_from__lte=price_from)
        elif price_to:
            filters &= Q(price_to__lte=price_to)

        # Apply filters to queryset
        queryset = queryset.filter(filters)
        return queryset
    
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('category', openapi.IN_QUERY, description='Filter value of audience', type=openapi.TYPE_STRING),
        openapi.Parameter('audience', openapi.IN_QUERY, description='Filter value of audience', type=openapi.TYPE_STRING),
        openapi.Parameter('age_limits', openapi.IN_QUERY, description='Filter value of age_limits', type=openapi.TYPE_STRING),
        openapi.Parameter('type_of_location', openapi.IN_QUERY, description='Filter value of type_of_location', type=openapi.TYPE_STRING),
        openapi.Parameter('price_from', openapi.IN_QUERY, description='Filter value of price_from', type=openapi.TYPE_STRING),
        openapi.Parameter('price_to', openapi.IN_QUERY, description='Filter value of price_to', type=openapi.TYPE_STRING),
        openapi.Parameter('date', openapi.IN_QUERY, description='Filter value of date', type=openapi.TYPE_STRING),
    

    ])
    def list(self, request, *args, **kwargs):
        queryset = sorted(list(set(self.get_queryset())), key=lambda x: (
            x.event_dates.filter(id__in=EventDate.objects.filter(status=False))
            .earliest('date_time').date_time))
        # page = self.paginate_queryset(queryset)
        # if page:
            # serializer = self.get_serializer(page, many=True)
            # return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    # def retrieve(self):
    #     obj = Event.objects.get(id=self.kwargs.get('pk'))
    #     return obj
    def retrieve(self, request, *args, **kwargs):
        try:
            obj = Event.objects.get(id=kwargs.get('pk'))
            print(obj)
            return Response(serializers.EventListSerializer(obj).data)
        except:
            return Response('Not Found', status=404)


    @action(detail=False, methods=['post'])
    @swagger_auto_schema(request_body=serializers.EventSerializer())
    def create_event(self, request):
        name = request.data.get('name')
        author = request.user.id
        description = request.data.get('description')
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
        poster = request.data.get('poster')
        tickets_number = request.data.get('tickets_number')
        price_from = request.data.get('price_from') 
        price_to = request.data.get('price_to')
        location_name = request.data.get('location_name')

        event = Event.objects.create(name=name, description=description, video=video, location_link=location_link, age_limits=get_object_or_404(AgeLimit, name=age_limits),  audience=get_object_or_404(Audience, name=audience), author_id=author, poster=poster, image1=image1, image2=image2, image3=image3, image4=image4, image5=image5,location_name=location_name, type_of_location=get_object_or_404(Location, name=type_of_location), tickets_number=tickets_number, price_from=price_from, price_to=price_to, )

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
        poster = request.data.get('poster')
        tickets_number = request.data.get('tickets_number')
        price_from = request.data.get('price_from') 
        price_to = request.data.get('price_to')
        location_name = request.data.get('location_name')

        if name:
            event.name = name
        if description:
            event.description = description
        if video:
            event.video = video
        if location_link:
            event.location_link = location_link
        if location_name:
            event.location_name = location_name
        event.age_limits = get_object_or_404(AgeLimit, name=age_limits)
        event.audience = get_object_or_404(Audience, name=audience)
        event.type_of_location = get_object_or_404(Location, name=type_of_location)
        if poster:
            event.poster = poster
        if image1:
            event.image1 = image1
        if image2:
            event.image2 = image2
        if image3:
            event.image3 = image3
        if image4:
            event.image4 = image4
        if image5:        
            event.image5 = image5
        event.tickets_number = tickets_number
        if price_from:
            event.price_from = price_from
        if price_to:
            event.price_to = price_to
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
        return Response(serializers.EventListSerializer(event).data)

    @action(detail=True, methods=['delete'])
    def delete_event(self, request, pk=None):
        self.check_object_permissions(request, self.get_object())
        try:
            event = self.get_queryset().get(pk=pk)
            event.delete()
            return Response({'success': 'Event deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            return Response({'error': 'Event does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
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

    @action(detail=True, methods=['GET'])
    def get_ticket(self, request, pk):
        if not request.user.is_authenticated:
            return Response(status=401)
        user = self.request.user
        event = get_object_or_404(Event, id=pk)
        if Ticket.objects.filter(user=request.user, event=event).exists():
            Ticket.objects.filter(user=request.user, event=event).delete()
            event.tickets_number += 1
            event.save()
            return Response('Удалено')
        else:
            if event.tickets_number != None and event.tickets_number!=0:
                if event.tickets_number >= 1:
                    Ticket.objects.create(user=request.user, event=event)
                    event.tickets_number -= 1
                    event.save()
            else:
                return Response('Билетов не осталось')
        send_mails.send_guest_mail(user=user, event=event)
        send_mails.send_host_mail(user, event)
        return Response('Сохранено', status=201)

class AudienceListView(ListAPIView):
    queryset = Audience.objects.all()
    serializer_class = serializers.AudienceSerializer


class AgeLimitsListView(ListAPIView):
    queryset = AgeLimit.objects.all()
    serializer_class = serializers.AgeLimitsSerializer


class LocationListView(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer
