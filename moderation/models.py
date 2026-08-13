from django.db import models
from django.conf import settings

# Create your models here.

class ModeratorActions(models.Model):
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE     
    )
    
    target_type = models.CharField()
    target_id = models.CharField()
    action = models.CharField()
    reason = models.TextField()
    created_at = models.DateTimeField()