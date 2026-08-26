from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from registration.models import Registration
from registration.serializers import *

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
