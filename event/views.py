from rest_framework.viewsets import GenericViewSet
from . import serializers
from .paginator import EventPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EventFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAuthor
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event, EventDate, Category
from rest_framework import status, mixins



class EventViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
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
        print(self.action)
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action in ['update_event', 'delete_event']:
            print('this one worked but shit not correct!')
            print(IsAuthor())
            return [IsAuthor()]
        else:
            return [IsAuthenticated()]
    
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

    def list(self, request, *args, **kwargs):
        queryset = sorted(self.get_queryset(), 
            key=lambda x: x.event_dates.filter(
            id__in=EventDate.objects.filter(status=False)
            ).first().date_time)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['post'])
    def create_event(self, request):
        name = request.data.get('name')
        author = request.user.id
        description = request.data.get('description')
        price = request.data.get('price')
        video = request.data.get('video')
        location = request.data.get('location')
        location_link = request.data.get('location_link')
        age_limits = request.data.get('age_limits')
        category_id = request.data.get('main_category')
        side_category1_id = request.data.get('side_category1')
        side_category2_id = request.data.get('side_category2')
        try:
            main_category = Category.objects.get(id=category_id)
        except:
            main_category = None
        try:
            side_category1 = Category.objects.get(id=side_category1_id)
        except:
            side_category1 = None
        try:
            side_category2 = Category.objects.get(id=side_category2_id)
        except:
            side_category2 = None
        contacts = request.data.get('contacts')
        audience = request.data.get('audience')

        event = Event.objects.create(name=name, description=description, price=price, video=video, location=location, location_link=location_link, age_limits=age_limits, main_category=main_category, side_category1=side_category1, side_category2=side_category2, contacts=contacts, audience=audience, author_id=author)
        
        # Create EventDate objects 1 type
        # event = Event.objects.create(name=name)
        # event_dates = request.data.get('event_dates')
        # for pair in event_dates:
        #         event_dates = event.event_dates.create(date_time=datetime.strptime(pair.get('date_time'), '%Y-%m-%dT%H:%M:%S.%fZ'), status=bool(False))

        # Create EventDate objects 2 type
        if not request.POST.getlist('event_dates'): #[{"date_time": "2020-05"}]
            return Response({"error": "dates are must"}, status=404)
        event_dates = request.POST.getlist('event_dates')
        date_times = []
        for event_date in event_dates:
            event.event_dates.create(date_time=event_date, status=bool(False))
    

        # Create EventImages objects
        for index, file in enumerate(request.FILES.getlist('images')):
            event_images = event.images.create(
                image=file
            )

        serializer = self.get_serializer(event)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def update_event(self, request, pk=None):
        try:
            event = self.get_queryset().get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name', event.name)
        description = request.data.get('description', event.description)
        price = request.data.get('price', event.price)
        video = request.data.get('video', event.video)
        location = request.data.get('location', event.location)
        location_link = request.data.get('location_link', event.location_link)
        age_limits = request.data.get('age_limits', event.age_limits)
        category_id = request.data.get('main_category', event.main_category.id if event.main_category else None)
        side_category1_id = request.data.get('side_category1', event.side_category1.id if event.side_category1 else None)
        side_category2_id = request.data.get('side_category2', event.side_category2.id if event.side_category2 else None)
        try:
            main_category = Category.objects.get(id=category_id)
        except:
            main_category = None
        try:
            side_category1 = Category.objects.get(id=side_category1_id)
        except:
            side_category1 = None
        try:
            side_category2 = Category.objects.get(id=side_category2_id)
        except:
            side_category2 = None
        contacts = request.data.get('contacts', event.contacts)
        audience = request.data.get('audience', event.audience)

        event.name = name
        event.description = description
        event.price = price
        event.video = video
        event.location = location
        event.location_link = location_link
        event.age_limits = age_limits
        event.main_category = main_category
        event.side_category1 = side_category1
        event.side_category2 = side_category2
        event.contacts = contacts
        event.audience = audience
        event.save()

        # Update EventDates objects
        if not request.POST.getlist('event_dates'):
            return Response({"error": "dates are must"}, status=404)
        event_dates = request.POST.getlist('event_dates')
        event.event_dates.all().delete()
        date_times = []
        for event_date in event_dates:
            event.event_dates.create(date_time=event_date, status=bool(False))
        print(date_times)
        # Update EventImages objects
        if request.FILES.getlist('images'):
            event.images.all().delete()
            for index, file in enumerate(request.FILES.getlist('images')):
                event.images.create(image=file)

        serializer = self.get_serializer(event)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def delete_event(self, request, pk=None):
        try:
            event = self.get_queryset().get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        event.delete()
        return Response({'success': 'Event deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
