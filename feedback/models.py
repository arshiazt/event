from django.db import models
from event.models import Event
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class EventComment(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="event_comments"
    )

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):

        if self.event.status != self.event.Status.FINISHED:
            raise ValidationError("You can comment only on finished events.")

        if not self.event.registrations.filter(user=self.user).exists():
            raise ValidationError("You must be registered in this event to comment.")


    def __str__(self):
        return f"Comment by {self.user} on {self.event}"