from rest_framework import serializers
from .models import ModerationReport


class ModerationReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModerationReport
        fields = [
            "id",
            "report",
            "moderator",
            "action",
            "created_at",
            "reviewed_at",
        ]

        read_only_fields = [
            "id",
            "report",
            "moderator",
            "created_at",
            "reviewed_at",
        ]

class ModerationActionSerializer(serializers.Serializer):

    action = serializers.ChoiceField(
        choices=ModerationReport.Action.choices
    )
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    content = serializers.CharField(required=False)

class QuestionModerationSerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        choices=["publish", "remove"]
    )