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

class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRating
        fields = ("value",)

    def validate_value(self, value):
        if not (0 <= value <= 5):
            raise serializers.ValidationError(
                "Rating must be between 0 and 5."
            )
        return value

    def validate(self, attrs):
        event = self.context["event"]
        user = self.context["request"].user

        if event.status != event.Status.FINISHED:
            raise serializers.ValidationError(
                "You can rate only finished events."
            )

        if not event.registrations.filter(user=user).exists():
            raise serializers.ValidationError(
                "You must be registered in this event to rate."
            )

        return attrs

    def create(self, validated_data):
        event = self.context["event"]
        user = self.context["request"].user

        rating, _ = EventRating.objects.update_or_create(
            event=event,
            user=user,
            defaults={"value": validated_data["value"]}
        )

        return rating
    
class RatingListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = EventRating
        fields = (
            "user",
            "value",
            "updated_at",
        )

class EventResultsSerializer(serializers.Serializer):
    
    average_rating = serializers.FloatField()
    ratings_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()
    comments = CommentListSerializer(many=True)