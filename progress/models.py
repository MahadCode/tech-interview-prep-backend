from django.db import models
from django.conf import settings

# Create your models here.
class PreparationGoal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE 
    )
    
    class GoalMetric(models.TextChoices):
        QUESTION_COUNT = "question_count", "Question_Count"
        TOPIC_MASTERY = "topic_mastery", "Topic_Mastery"
        COMPANY_TARGET = "company_target", "Company_Target"
        
    metric = models.CharField(
        max_length=20,
        choices=GoalMetric.choices,
        default=GoalMetric.QUESTION_COUNT
    )

    target_company = models.ForeignKey(
        "taxonomy.Company",
        on_delete=models.CASCADE
    )
    
    target_value = models.IntegerField()
    current_progress = models.IntegerField()
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class ProgressRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE 
    )
    question = models.ForeignKey(
        "questions.Question",
        on_delete=models.SET_NULL,
        null=True
    )
    class ProgressStatus(models.TextChoices):
        UNSOLVED = "unsolved", "Unsolved"
        ATTEMPTED = "attempted", "Attempted"
        SOLVED = "solved", "Solved"
    
    status = models.CharField(
        max_length=20,
        choices=ProgressStatus.choices,
        default=ProgressStatus.UNSOLVED,
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    