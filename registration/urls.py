from django.urls import path
from registration.views import *

urlpatterns = [
    path('register/',ParticipantRegistrationCreateView.as_view(),name='register'),
    path('list/',ParticipantRegistrationListView.as_view(),name='list'),
    path('cancel/<int:id>',ParticipantRegistrationCancelView.as_view(),name='cancel'),
    path('list-registrations/<int:event_id>',EventRegistrationListForOrganizerView.as_view(),name='list-r')
]
