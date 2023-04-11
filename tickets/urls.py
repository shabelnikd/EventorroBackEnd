from django.urls import path

from event.views import EventViewSet
from .views import (
    TicketCreateView,
    TicketDeleteView,
)


urlpatterns = [
    path('events/<int:event_id>/tickets/create/', TicketCreateView.as_view(), name='ticket-create'),
    path('events/<int:event_id>/tickets/<int:ticket_id>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
]
