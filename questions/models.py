from django.db import models
from django.conf import settings

# Create your models here.

class Question(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="questions",
        null=True
    )
    
    company = models.ManyToManyField(
        "taxonomy.Company",
        related_name="questions"
    )
    
    job_role = models.ForeignKey(
        "taxonomy.JobRole",
        on_delete=models.SET_NULL,
        related_name="questions",
        null=True
    )
    
    tag = models.ManyToManyField(
        "taxonomy.Tag",
        related_name="questions",
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
    description = models.TextField()

    class QuestionStatus(models.TextChoices):
        PENDING_REVIEW = "pending_review", "Pending_Review"
        PUBLISHED = "published", "Published"
        REMOVED = "removed", "Removed"

    status = models.CharField(
        max_length=20,
        choices=QuestionStatus.choices,
        default=QuestionStatus.PUBLISHED
    )
    
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
class UserQuestionStatus(models.Model):
    class StatusChoices(models.TextChoices):
        UNSOLVED = "unsolved", "Unsolved"
        ATTEMPTED = "attempted", "Attempted"
        SOLVED = "solved", "Solved"
    
    status = models.CharField(
        max_length=20,
        choices = StatusChoices.choices,
        default = StatusChoices.UNSOLVED, 
    )
    
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="questions_progress_status"
    )
    
    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        related_name = "progress_status"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'question'],
                name = "unique_together_validator"
            )
        ]