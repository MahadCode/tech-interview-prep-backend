from django.db import models
from django.conf import settings

# Create your models here.
from django.db import models
from django.conf import settings


class PreparationGoal(models.Model):

    class GoalMetric(models.TextChoices):
        QUESTION_COUNT = "question_count", "Question Count"
        TOPIC_MASTERY = "topic_mastery", "Topic Mastery"
        COMPANY_TARGET = "company_target", "Company Target"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="preparation_goals"
    )

    metric = models.CharField(
        max_length=20,
        choices=GoalMetric.choices,
    )

    target_tag = models.ForeignKey(
        "taxonomy.Tag",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="preparation_goals"
    )

    target_company = models.ForeignKey(
        "taxonomy.Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="preparation_goals"
    )

    target_value = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    deadline = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    

    def __str__(self):
        return f"{self.user} - {self.metric}"
    