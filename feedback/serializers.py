from rest_framework import serializers
from feedback.models import EventComment, EventRating

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventComment
        fields = ("id", "text")
        read_only_fields = ("id",)

    def validate(self, attrs):
        event = self.context["event"]
        user = self.context["request"].user

        if event.status != event.Status.FINISHED:
            raise serializers.ValidationError(
                "You can comment only on finished events."
            )

        if not event.registrations.filter(user=user).exists():
            raise serializers.ValidationError(
                "You must be registered in this event to comment."
            )

        return attrs

    def create(self, validated_data):
        return EventComment.objects.create(
            event=self.context["event"],
            user=self.context["request"].user,
            **validated_data
        )
    
class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = EventComment
        fields = (
            "id",
            "user",
            "text",
            "created_at",
        )