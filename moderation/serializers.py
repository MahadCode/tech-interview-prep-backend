from rest_framework import serializers
from .models import ModerationReport
from discussions.serializers import ReportSerializer
from questions.serializers import QuestionSerializer
from accounts.serializers import UserSerializer


class ModerationReportSerializer(serializers.ModelSerializer):
    report = ReportSerializer(read_only=True)
    question = QuestionSerializer(source="report.question", read_only=True)
    reporter = UserSerializer(source="report.reporter", read_only=True)
    class Meta:
        model = ModerationReport
        fields = [
            "id",
            "report",
            "question",
            "reporter",
            "moderator",
            "action",
            "created_at",
            "reviewed_at",
        ]

        read_only_fields = [
            "id",
            "moderator",
            "created_at",
            "reviewed_at",
        ]


class ModerationActionSerializer(serializers.Serializer):

    action = serializers.ChoiceField(choices=ModerationReport.Action.choices)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    content = serializers.CharField(required=False)


class QuestionModerationSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["publish", "remove"])
