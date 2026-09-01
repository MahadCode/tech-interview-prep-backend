from .models import Solution, Comment, Report
from rest_framework import serializers
from accounts.serializers import UserSerializer


class SolutionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Solution
        fields = "__all__"
        read_only_fields = ["id", "question", "created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, attrs):
        question = attrs.get("question")
        solution = attrs.get("solution")
        reply_to = attrs.get("reply_to")
        if self.instance is None:
            if question and solution:
                raise serializers.ValidationError(
                    "A comment cannot belong to both a question and a solution"
                )

            if question and reply_to:
                raise serializers.ValidationError(
                    "A comment cannot belong to both a question and a comment"
                )

            if solution and reply_to:
                raise serializers.ValidationError(
                    "A comment cannot belong to both a comment and a solution"
                )

            if not solution and not question and not reply_to:
                raise serializers.ValidationError(
                    "A comment must belong to either a question or a solution or a comment"
                )
        else:
            if "question" in attrs or "solution" in attrs or "reply_to" in attrs:
                raise serializers.ValidationError(
                    "Can't Change the Reference Object while editing the comment"
                )

        return attrs

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "reporter", "question", "solution", "comment", "reviewed_by", "reason", "status", "created_at", "resolved_at" ]
        read_only_fields = ["id", "reporter", "reviewed_by", "status", "created_at", "resolved_at"]
    
    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        request = self.context.get("request")

        if request and request.method == "PATCH":
            for field in ["question", "solution", "comment"]:
                extra_kwargs[field] = {"read_only": True}

        return extra_kwargs
    
    def validate(self, attrs):
        request = self.context.get("request")
        if request and request.method == "PATCH":
            return attrs
        
        question = attrs.get("question")
        solution = attrs.get("solution")
        comment = attrs.get("comment")

        targets = [question, solution, comment]

        if sum(target is not None for target in targets) != 1:
            raise serializers.ValidationError(
                "A report must belong to exactly one of a question, solution, or comment."
            )

        return attrs


class QuestionCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "author",
            "reply_to",
            "replies",
            "created_at",
            "updated_at",
        ]

    def get_replies(self, obj):
        return QuestionCommentSerializer(
            obj.replies.all(),
            many=True
        ).data
