from rest_framework import serializers
from django.db.models import Count
from .models import PreparationGoal
from questions.models import Question, UserQuestionStatus


class PreparationGoalSerializer(serializers.ModelSerializer):

    target_tag_name = serializers.CharField(source="target_tag.name", read_only=True)

    target_company_name = serializers.CharField(
        source="target_company.name", read_only=True
    )

    total_questions = serializers.SerializerMethodField()
    solved_questions = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()

    class Meta:
        model = PreparationGoal

        fields = [
            "id",
            "metric",
            "target_value",
            "target_tag",
            "target_tag_name",
            "target_company",
            "target_company_name",
            "total_questions",
            "solved_questions",
            "progress_percentage",
            "deadline",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "target_tag_name",
            "target_company_name",
            "total_questions",
            "solved_questions",
            "progress_percentage",
            "created_at",
        ]

    def validate(self, attrs):
        metric = attrs.get("metric", getattr(self.instance, "metric", None))

        target_value = attrs.get(
            "target_value", getattr(self.instance, "target_value", None)
        )

        target_tag = attrs.get("target_tag", getattr(self.instance, "target_tag", None))

        target_company = attrs.get(
            "target_company", getattr(self.instance, "target_company", None)
        )

        if metric == PreparationGoal.GoalMetric.QUESTION_COUNT:

            if target_value is None:
                raise serializers.ValidationError(
                    {
                        "target_value": "Target value is required for question count goals."
                    }
                )

            if target_value <= 0:
                raise serializers.ValidationError(
                    {"target_value": "Target value must be greater than 0."}
                )

            if target_tag is not None:
                raise serializers.ValidationError(
                    {"target_tag": "Tag must not be provided for question count goals."}
                )

            if target_company is not None:
                raise serializers.ValidationError(
                    {
                        "target_company": "Company must not be provided for question count goals."
                    }
                )

        elif metric == PreparationGoal.GoalMetric.TOPIC_MASTERY:

            if target_tag is None:
                raise serializers.ValidationError(
                    {"target_tag": "Tag is required for topic mastery goals."}
                )

            if target_value is not None:
                raise serializers.ValidationError(
                    {
                        "target_value": "Target value must not be provided for topic mastery goals."
                    }
                )

            if target_company is not None:
                raise serializers.ValidationError(
                    {
                        "target_company": "Company must not be provided for topic mastery goals."
                    }
                )

        elif metric == PreparationGoal.GoalMetric.COMPANY_TARGET:

            if target_company is None:
                raise serializers.ValidationError(
                    {"target_company": "Company is required for company goals."}
                )

            if target_value is not None:
                raise serializers.ValidationError(
                    {
                        "target_value": "Target value must not be provided for company goals."
                    }
                )

            if target_tag is not None:
                raise serializers.ValidationError(
                    {"target_tag": "Tag must not be provided for company goals."}
                )

        return attrs

    def _get_question_queryset(self, goal):
        queryset = Question.objects.filter(
            status=Question.QuestionStatus.PUBLISHED, is_deleted=False
        )

        if goal.metric == PreparationGoal.GoalMetric.TOPIC_MASTERY:
            queryset = queryset.filter(tag=goal.target_tag)

        elif goal.metric == PreparationGoal.GoalMetric.COMPANY_TARGET:
            queryset = queryset.filter(company=goal.target_company)

        return queryset

    def get_total_questions(self, obj):
        if obj.metric == PreparationGoal.GoalMetric.QUESTION_COUNT:
            return obj.target_value

        return self._get_question_queryset(obj).count()

    def get_solved_questions(self, obj):
        queryset = UserQuestionStatus.objects.filter(
            user=obj.user,
            status=UserQuestionStatus.StatusChoices.SOLVED,
            question__status=Question.QuestionStatus.PUBLISHED,
            question__is_deleted=False,
        )

        if obj.metric == PreparationGoal.GoalMetric.TOPIC_MASTERY:
            queryset = queryset.filter(question__tag=obj.target_tag)

        elif obj.metric == PreparationGoal.GoalMetric.COMPANY_TARGET:
            queryset = queryset.filter(question__company=obj.target_company)

        return queryset.count()

    def get_progress_percentage(self, obj):
        total_questions = self.get_total_questions(obj)
        solved_questions = self.get_solved_questions(obj)

        if total_questions == 0:
            return 0

        percentage = (solved_questions / total_questions) * 100

        return min(round(percentage, 2), 100)


class PreparationStatisticsSerializer(serializers.Serializer):

    total_solved = serializers.SerializerMethodField()
    difficulty_breakdown = serializers.SerializerMethodField()
    topic_breakdown = serializers.SerializerMethodField()
    company_breakdown = serializers.SerializerMethodField()

    def get_solved_queryset(self, obj):

        solved_questions = UserQuestionStatus.objects.filter(
            user=obj,
            status=UserQuestionStatus.StatusChoices.SOLVED,
            question__status=Question.QuestionStatus.PUBLISHED,
            question__is_deleted=False,
        )
        
        return solved_questions

    def get_total_solved(self, obj):
        solved_questions = self.get_solved_queryset(obj)
        return solved_questions.count()

    def get_difficulty_breakdown(self, obj):
        solved_questions = self.get_solved_queryset(obj)

        difficulty_data = solved_questions.values(
            "question__difficulty_level"
        ).annotate(solved_count=Count("question"))

        result = []

        for item in difficulty_data:
            result.append(
                {
                    "difficulty": item["question__difficulty_level"],
                    "solved": item["solved_count"],
                }
            )

        return result

    def get_topic_breakdown(self, obj):
        solved_questions = self.get_solved_queryset(obj)

        topic_data = (
            solved_questions.filter(question__tag__isnull=False)
            .values("question__tag_id", "question__tag__name")
            .annotate(solved_count=Count("question"))
        )

        result = []

        for item in topic_data:
            result.append(
                {
                    "tag_id": item["question__tag_id"],
                    "tag_name": item["question__tag__name"],
                    "solved": item["solved_count"],
                }
            )

        return result

    def get_company_breakdown(self, obj):
        solved_questions = self.get_solved_queryset(obj)

        company_data = solved_questions.values(
            "question__company__id", "question__company__name"
        ).annotate(solved_count=Count("question"))

        result = []

        for item in company_data:
            result.append(
                {
                    "company_id": item["question__company__id"],
                    "company_name": item["question__company__name"],
                    "solved": item["solved_count"],
                }
            )

        return result
