from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from registration.models import Registration

User = get_user_model()


class ParticipantRegistrationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = ("event",)

    def create(self, validated_data):

        user = self.context["request"].user
        registration = Registration(user=user,event=validated_data["event"])
        try:
            registration.full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        registration.save()

        return registration