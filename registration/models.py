from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Registration(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        CANCELED = "canceled", "Canceled"

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='registration')
    event = models.ForeignKey('event.Event',on_delete=models.CASCADE,related_name='registrations')
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    canceled_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("user", "event")
        ordering = ("-created_at",)

    def clean(self):
        now = timezone.now()

        if self.event.status != self.event.Status.PUBLISHED:
            raise ValidationError("Registration is allowed only for published events.")

        if now >= self.event.start_date:
            raise ValidationError("Registration is closed after the event has started.")
        
        active_count = self.event.registrations.filter(status=self.Status.ACTIVE).exclude(pk=self.pk).count()

        if active_count >= self.event.capacity:
            raise ValidationError("Event capacity is full.")
        
        if self.pk:
            old_status = Registration.objects.get(pk=self.pk).status

            if old_status == self.Status.ACTIVE and self.status == self.Status.CANCELED:
                if self.event.status != self.event.Status.PUBLISHED:
                    raise ValidationError("You can cancel registration only while the event is published.")
    
    def cancel(self):
        if self.status == self.Status.CANCELED:
            return

        self.status = self.Status.CANCELED
        self.canceled_at = timezone.now()
        self.full_clean()
        self.save(update_fields=["status", "canceled_at"])

    def __str__(self):
        return f"{self.user} → {self.event} ({self.status})"
