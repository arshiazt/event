from rest_framework.permissions import BasePermission

class IsOrganize(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.organizer)

class IsOrganizerAndEventOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            request.user.organizer and
            obj.event.owner == request.user
        )
