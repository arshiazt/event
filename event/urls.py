from django.urls import path
from event.views import *

urlpatterns = [

    # Events 
    path("create/", EventCreateView.as_view(), name="event-create"),
    path("list/", EventListView.as_view(), name="event-list"),
    path("<int:id>/", EventDetailView.as_view(), name="event-detail"),
    path("<int:id>/update/", EventUpdateView.as_view(), name="event-update"),
    path("<int:id>/delete/", EventDeleteView.as_view(), name="event-delete"),

    # Attributes
    path("attributes/create/", AttributeCreateView.as_view(), name="attribute-create"),
    path("attributes/", AttributeListView.as_view(), name="attribute-list"),
    
    # Event Attribute Values 
    path("<int:event_id>/attributes/add/", EventAttributeValueCreateView.as_view(), name="event-attribute-add"),
    path("event-attribute/<int:id>/update/", EventAttributeValueUpdateView.as_view(), name="event-attribute-update"),
    path("event-attribute/<int:id>/delete/", EventAttributeValueDeleteView.as_view(), name="event-attribute-delete"),
    
    # Public Event
    path("event-list/", PublicEventListView.as_view(), name="public-event-list"),
    path("event-detail/<int:id>/", PublicEventDetailView.as_view(), name="public-event-detail"),
]
