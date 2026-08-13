from django.db import models
from django.conf import settings

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    class NotificationType(models.TextChoices):
        NEW_REPLY = "new_reply", "New_Reply"
        NEW_SOLUTION = "new_solution", "New_Solution"
        CONTENT_MODERATED = "content_moderated", "Content_Moderated"
        GOAL_PROGRESS = "goal_progress", "Goal_Progress"
    
    type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.NEW_REPLY
    )
    
    reference_type = models.TextField()
    reference_id = models.PositiveIntegerField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)