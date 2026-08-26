from rest_framework import serializers
from django.utils import timezone
from event.models import Event,Attribute,EventAttributeValue
from django.core.exceptions import ValidationError

class EventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            "title",
            "description",
            "capacity",
            "price",
            "published_date",
            "start_date",
            "end_date",
            "coach",
            "speaker",
            "judge",
            "can_be_prerequisite",
            "prerequisite_event",
            "require_prerequisite_registration",
        )

    def validate(self, attrs):
        
        now = timezone.now()
        published_date = attrs.get('published_date')
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        prerequisite_event = attrs.get('prerequisite_event')

        if published_date < now:
            raise serializers.ValidationError({'published_date':'Publish date cannot be in the past'})

        if published_date >= start_date:
            raise serializers.ValidationError({'published_date':'Publish date must be before start date'})
    
        if start_date >= end_date:
            raise serializers.ValidationError({'end_date':'End date must be after start date'})

        if prerequisite_event:
            
            request = self.context.get('request')
            owner = request.user

            if prerequisite_event.owner != owner:
                raise serializers.ValidationError('Prerequisite event must have the same owner')
            
            if not prerequisite_event.can_be_prerequisite:
                raise serializers.ValidationError('This event cannot be used as a prerequisite')
            
            if prerequisite_event.end_date >= start_date:
                raise serializers.ValidationError('Prerequisite event must end before this event starts')

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        event = Event.objects.create(owner=request.user,status=Event.Status.DRAFT,**validated_data)

        return event  
    
class EventListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "status",
            "capacity",
            "price",
            "published_date",
            "start_date",
            "end_date",
        )
        read_only_fields = fields

class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = ('id','name','value_type')
        read_only_fields = ('id',)

    def validate_name(self,value):
        
        if Attribute.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError('This attribute already exists. Please use the existing one')

        return value