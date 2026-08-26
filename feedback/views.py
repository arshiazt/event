from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from event.models import Event
from feedback.models import EventComment, EventRating
from feedback.serializers import *

# Create your views here.

class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        serializer = CommentCreateSerializer(
            data=request.data,
            context={
                "request": request,
                "event": event
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Comment submitted successfully."},
            status=status.HTTP_201_CREATED
        )
    
class RatingCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingCreateSerializer
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        serializer = RatingCreateSerializer(
            data=request.data,
            context={
                "request": request,
                "event": event
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Rating saved successfully."},
            status=status.HTTP_201_CREATED
        )
    
class OrganizerCommentListView(ListAPIView):

    serializer_class = CommentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event = get_object_or_404(Event, id=self.kwargs["event_id"])

        if event.owner != self.request.user:
            raise PermissionDenied("You do not own this event.")

        return EventComment.objects.filter(event=event)

class OrganizerRatingListView(ListAPIView):
    
    serializer_class = RatingListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event = get_object_or_404(Event, id=self.kwargs["event_id"])

        if event.owner != self.request.user:
            raise PermissionDenied("You do not own this event.")

        return EventRating.objects.filter(event=event)