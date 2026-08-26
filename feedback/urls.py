from django.urls import path

from feedback.views import *
urlpatterns = [
    # --- Participant actions ---
    path("events/<int:event_id>/comment/",CommentCreateView.as_view(),name="event-comment-create"),
    path("events/<int:event_id>/rate/",RatingCreateView.as_view(),name="event-rate-upsert"),
    
    # --- Organizer views ---
    path("events/<int:event_id>/comments/",OrganizerCommentListView.as_view(),name="event-comments-list"),
    path("events/<int:event_id>/ratings/",OrganizerRatingListView.as_view(), name="event-ratings-list"),
    
    # --- Public results ---
    path("events/<int:event_id>/results/",EventResultsView.as_view(),name="event-results"),
]
