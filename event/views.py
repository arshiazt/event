from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.exceptions import PermissionDenied
from event.models import Event,Attribute,EventAttributeValue
from event.serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from event.permissions import IsOrganizerAndEventOwner

# Create your views here.

class EventCreateView(CreateAPIView):
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        if not user.organizer:
            raise PermissionDenied('Only organizers can create events')

        serializer.save()

class EventListView(ListAPIView):
    serializer_class = EventListSerializer
    permission_classes  = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.organizer:
            raise PermissionDenied('Only organizers can view their events')
        
        queryset = Event.objects.filter(owner=user)

        for event in queryset:
            event.update_status()

        return queryset
    
class EventDetailView(RetrieveAPIView):
    serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user

        if not user.organizer:
            raise PermissionDenied('Only organizers can view event details')

        return Event.objects.filter(owner=user)
    
    def get_object(self):
        event = super().get_object()
        event.update_status()
        
        return event
    
@method_decorator(csrf_exempt,name='dispatch')
class EventUpdateView(UpdateAPIView):
    serializer_class = EventUpdateSerializer
    permission_classes  = [IsAuthenticated]
    lookup_field = 'id'
    http_method_names = ['patch']

    def get_queryset(self):
        user = self.request.user

        if not user.organizer:
            raise PermissionDenied('Only organizers can update events')

        return Event.objects.filter(owner=user)

@method_decorator(csrf_exempt,name='dispatch')
class EventDeleteView(DestroyAPIView):
    serializer_class = EventDeleteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user

        if not user.organizer:
            raise PermissionDenied('Only organizers can delete events')

        return Event.objects.filter(owner=user)
    
class AttributeCreateView(CreateAPIView):
    serializer_class = AttributeSerializer
    queryset = Attribute.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        if not user.organizer:
            raise PermissionDenied('Only organizers can create attributes')

        serializer.save()

class AttributeListView(ListAPIView):
    serializer_class = AttributeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.organizer:
            raise PermissionDenied('Only organizers can view attributes')

        return Attribute.objects.all()