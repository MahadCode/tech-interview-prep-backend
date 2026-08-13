from django.db import models
from django.conf import settings
# Create your models here.

class Question(models.Model):
    author_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="questions",
    )
    company = models.ManyToManyField(
        "taxonomy.Company",
        related_name="questions"
    )
    job_role = models.ForeignKey(
        "taxonomy.JobRole",
        on_delete=models.SET_NULL,
        related_name="questions"
    )
    class DifficultyLevel(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"

    difficulty_level = models.CharField(
        max_length=20,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.EASY,
    )

    title = models.CharField()
    body = models.TextField()

    class QuestionStatus(models.TextChoices):
        PENDING_REVIEW = "pending_review", "Pending_Review"
        PUBLISHED = "published", "Published"
        REMOVED = "removed", "Removed"

    status = models.CharField(
        max_length=20,
        choices=QuestionStatus.choices,
        default=QuestionStatus.PENDING_REVIEW
    )

    is_active = models.BooleanField(default=True)
    created_at = models.BigAutoField(auto_now_add=True)