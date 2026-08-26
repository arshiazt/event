from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

User = get_user_model()

class Event(models.Model):

    class Status(models.TextChoices):
       DRAFT = "draft", "Draft"
       PUBLISHED = "published", "Published"
       CLOSED = "closed", "Closed"
       FINISHED = "finished", "Finished" 

    # important fields
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='events')
    title = models.CharField(max_length=255,unique=True)
    description = models.TextField(blank=True,null=True)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    published_date = models.DateTimeField(help_text='Datetime when event will be published automatically')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.DRAFT)
    # optional fields
    coach = models.CharField(max_length=255,blank=True,null=True)
    speaker = models.CharField(max_length=255,blank=True,null=True)
    judge = models.CharField(max_length=255,blank=True,null=True)
    # multi stage
    can_be_prerequisite = models.BooleanField(default=False)
    prerequisite_event = models.OneToOneField('self',on_delete=models.SET_NULL,blank=True,null=True,related_name='next_event')
    require_prerequisite_registration = models.BooleanField(default=False,help_text='If true, users must be registered in the prerequisite event to register in this event')

    created_date= models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)    

    def update_status(self,save=True):

        now = timezone.now()
        new_status = self.status

        if self.status ==  self.Status.DRAFT and now >= self.published_date:
            new_status = self.Status.PUBLISHED
        
        if self.status == self.Status.PUBLISHED and now >= self.start_date:
            new_status = self.Status.CLOSED

        if self.status == self.Status.CLOSED and now >= self.end_date:
            new_status = self.Status.FINISHED
        
        if self.status != new_status:
            self.status = new_status
            if save:
                self.save(update_fields=['status'])
    
    def clean(self):
            
        now = timezone.now()
        
        if self.start_date >= self.end_date:
            raise ValidationError('Start date must be before end date')
        
        if self.published_date >= self.start_date:
            raise ValidationError('Publish date must be before start date')
        
        if self.status == self.Status.DRAFT and self.published_date < now:
            raise ValidationError('Publish date cannot be in the past')
        
        if self.prerequisite_event:
            if self.prerequisite_event.owner != self.owner:
                raise ValidationError('Prerequisite event must have the same owner')
            
            if not self.prerequisite_event.can_be_prerequisite:
                raise ValidationError('This event cannot be used as a prerequisite')
            
            if self.prerequisite_event.end_date >= self.start_date:
                raise ValidationError('Prerequisite event must end before this event starts')
        
        if self.pk:
            old_status = Event.objects.get(pk=self.pk).status

            allowed_transitions = {
                self.Status.DRAFT: [self.Status.PUBLISHED],
                self.Status.PUBLISHED: [self.Status.CLOSED],
                self.Status.CLOSED: [self.Status.FINISHED],
                self.Status.FINISHED: [],
            }

            if self.status != old_status:
                if self.status not in allowed_transitions.get(old_status,[]):
                    raise ValidationError(f'Invalid status transition: {old_status} → {self.status}')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Attribute(models.Model):

    class ValueType(models.TextChoices):
        STRING = "string", "String"
        INTEGER = "integer", "Integer"
        BOOLEAN = "boolean", "Boolean"
        FLOAT = "float", "Float"

    name = models.CharField(max_length=255)
    value_type = models.CharField(max_length=20,choices=ValueType.choices)

    def __str__(self):
        return f'{self.name} ---> {self.value_type}'
    
class EventAttributeValue(models.Model):

    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='attribute_values')
    attribute = models.ForeignKey(Attribute,on_delete=models.CASCADE,related_name='event_values')

    value_string = models.CharField(max_length=255, blank=True, null=True)
    value_integer = models.IntegerField(blank=True, null=True)
    value_boolean = models.BooleanField(blank=True, null=True)
    value_float = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ("event", "attribute")

    def clean(self):
        values = {
            "string": self.value_string,
            "integer": self.value_integer,
            "boolean": self.value_boolean,
            "float": self.value_float,
        }

        for key,val in values.items():
            if key == self.attribute.value_type:
                if val is None:
                    raise ValidationError(f'Value for {self.attribute.value_type} must be provided')
            else:
                if val is not None:
                    raise ValidationError(f'Only value_{self.attribute.value_type} can be set')
            
    def __str__(self):
        return f'{self.event.title} - {self.attribute.name}'