from rest_framework import generics, status
from rest_framework.response import Response
from .models import Event, Ticket
from .serializers import TicketSerializer


class TicketCreateView(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        name = request.data.get('name')
        last_name = request.data.get('last_name')
        event_id = self.kwargs.get('event_id')
        event = Event.objects.get(pk=event_id)
        quantity = self.kwargs.get('quantity', 1)
        if event.tickets_number < quantity:
            return Response({'error': 'Not enough tickets available.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['event'] = event
        self.perform_create(serializer)
        data = serializer.data
        data['message']=f"""
        Спасибо за регистрацию!

        Вы только что зарегистрировались на событие {event.name} организации {event.author.name}. 
        Подтверждаем, что Ваша регистрация прошла успешно.*

        *Просим обратить внимание, что данное пригласительное не является правом на бесплатный вход, если организаторы решат сделать событие платным. Так же оно не гарантирует вход на мероприятие быстрее живой очереди.

        Информация о заказчике
        Имя:
        {name} {last_name}
        E-mail:
        {email}
        """
        # decrease tickets_number by quantity
        event.tickets_number -= serializer.validated_data.get('quantity', 1)
        event.save()
        headers = self.get_success_headers(serializer.data)
        Ticket.send_ticket_mail(email, event.author.name, event.name, name, last_name)
        return Response(data, status=201, headers=headers)
    

class TicketDeleteView(generics.DestroyAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def delete(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        ticket_id = kwargs.get('ticket_id')
        try:
            ticket = Ticket.objects.get(id=ticket_id, event_id=event_id)
        except Ticket.DoesNotExist:
            return Response("You don't seem to have a ticket", status=status.HTTP_404_NOT_FOUND)

        # increase the number of available tickets
        event = Event.objects.get(id=event_id)
        event.tickets_number += ticket.quantity
        event.save()

        # delete the ticket
        ticket.delete()

        return Response("You have cancelled the ticket purchase", status=status.HTTP_204_NO_CONTENT)