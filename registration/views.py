from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from registration.models import Registration
from registration.serializers import *
from event.models import Event

# Create your views here.

class ParticipantRegistrationCreateView(CreateAPIView):
    serializer_class = ParticipantRegistrationCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        if not user.participant:
            raise PermissionDenied("Only participants can register for events.")

        serializer.save()

class ParticipantRegistrationListView(ListAPIView):
    serializer_class = ParticipantRegistrationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.participant:
            raise PermissionDenied("Only participants can view their registrations.")

        return Registration.objects.filter(user=user)

class ParticipantRegistrationCancelView(UpdateAPIView):
    serializer_class = ParticipantRegistrationCancelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user

        if not user.participant:
            raise PermissionDenied("Only participants can cancel registrations.")

        return Registration.objects.filter(user=user)

class EventRegistrationListForOrganizerView(ListAPIView):
    serializer_class = EventRegistrationListForOrganizerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        event_id = self.kwargs.get("event_id")

        if not user.organizer:
            raise PermissionDenied("Only organizers can view registrations.")

        try:
            event = Event.objects.get(id=event_id, owner=user)
        except Event.DoesNotExist:
            raise PermissionDenied("You do not own this event.")

        return Registration.objects.filter(event=event)